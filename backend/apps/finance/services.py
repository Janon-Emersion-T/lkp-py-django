from datetime import timedelta
from decimal import Decimal
from typing import Any

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .calculations import (
    money,
    refresh_account_balance,
    validate_balanced_entries,
)
from .models import (
    Account,
    Expense,
    ExpenseStatus,
    Invoice,
    InvoiceItem,
    InvoiceStatus,
    LedgerEntry,
    Payment,
    PaymentStatus,
    Transaction,
    TransactionType,
)


class FinanceService:
    @staticmethod
    def generate_number(
        *,
        model,
        field_name: str,
        prefix: str,
    ) -> str:
        year = timezone.localdate().year
        full_prefix = f"{prefix}-{year}-"

        latest = (
            model.all_objects.filter(
                **{
                    f"{field_name}__startswith": full_prefix,
                },
            )
            .order_by(f"-{field_name}")
            .values_list(field_name, flat=True)
            .first()
        )

        if latest:
            try:
                sequence = int(
                    latest.rsplit("-", 1)[1]
                ) + 1
            except ValueError:
                sequence = (
                    model.all_objects.filter(
                        **{
                            f"{field_name}__startswith": (
                                full_prefix
                            ),
                        },
                    ).count()
                    + 1
                )
        else:
            sequence = 1

        return f"{full_prefix}{sequence:05d}"

    @staticmethod
    @transaction.atomic
    def create_account(
        *,
        request,
        values: dict[str, Any],
    ) -> Account:
        values["currency"] = values.get(
            "currency",
            "LKR",
        ).upper()

        account = Account.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        account.current_balance = account.opening_balance
        account.save(
            update_fields=[
                "current_balance",
                "updated_at",
            ],
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="finance",
            message="Finance account created.",
            target_type="finance.Account",
            target_id=str(account.pk),
            after={
                "account_code": account.account_code,
                "name": account.name,
                "account_type": account.account_type,
                "opening_balance": str(
                    account.opening_balance
                ),
                "currency": account.currency,
            },
        )

        return account

    @staticmethod
    @transaction.atomic
    def post_transaction(
        *,
        request,
        transaction_type: str,
        transaction_date,
        description: str,
        entries: list[dict[str, Any]],
        reference: str = "",
    ) -> Transaction:
        validate_balanced_entries(entries)

        total_amount = sum(
            (
                Decimal(str(entry.get("debit", "0.00")))
                for entry in entries
            ),
            Decimal("0.00"),
        )

        finance_transaction = Transaction.objects.create(
            transaction_number=FinanceService.generate_number(
                model=Transaction,
                field_name="transaction_number",
                prefix="LKP-TXN",
            ),
            transaction_type=transaction_type,
            transaction_date=transaction_date,
            description=description,
            reference=reference,
            total_amount=money(total_amount),
            created_by=request.auth,
            updated_by=request.auth,
        )

        affected_accounts: set[Account] = set()

        for entry in entries:
            account = entry["account"]

            LedgerEntry.objects.create(
                transaction=finance_transaction,
                account=account,
                debit=money(
                    Decimal(
                        str(entry.get("debit", "0.00"))
                    )
                ),
                credit=money(
                    Decimal(
                        str(entry.get("credit", "0.00"))
                    )
                ),
                narration=entry.get("narration", ""),
                created_by=request.auth,
                updated_by=request.auth,
            )

            affected_accounts.add(account)

        for account in affected_accounts:
            refresh_account_balance(account)

        log_activity(
            request=request,
            actor=request.auth,
            action="finance_transaction_posted",
            module="finance",
            description="Finance transaction posted.",
            entity_type="finance.Transaction",
            entity_id=str(finance_transaction.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="finance",
            message="Finance transaction posted.",
            target_type="finance.Transaction",
            target_id=str(finance_transaction.pk),
            after={
                "transaction_number": (
                    finance_transaction.transaction_number
                ),
                "transaction_type": transaction_type,
                "total_amount": str(
                    finance_transaction.total_amount
                ),
                "entry_count": len(entries),
            },
        )

        return finance_transaction

    @staticmethod
    def calculate_invoice_item(
        values: dict[str, Any],
    ) -> dict[str, Any]:
        quantity = Decimal(str(values["quantity"]))
        unit_price = Decimal(str(values["unit_price"]))
        discount = Decimal(
            str(values.get("discount_amount", "0.00"))
        )
        tax_rate = Decimal(
            str(values.get("tax_rate", "0.00"))
        )

        gross = money(quantity * unit_price)
        discount = money(
            min(
                max(discount, Decimal("0.00")),
                gross,
            )
        )
        subtotal = money(gross - discount)
        tax_amount = money(
            subtotal * max(
                tax_rate,
                Decimal("0.00"),
            )
            / Decimal("100")
        )

        values["quantity"] = quantity
        values["unit_price"] = unit_price
        values["discount_amount"] = discount
        values["tax_rate"] = tax_rate
        values["subtotal"] = subtotal
        values["tax_amount"] = tax_amount
        values["total_amount"] = money(
            subtotal + tax_amount
        )

        return values

    @staticmethod
    @transaction.atomic
    def create_invoice(
        *,
        request,
        values: dict[str, Any],
        items: list[dict[str, Any]],
    ) -> Invoice:
        values.setdefault(
            "invoice_number",
            FinanceService.generate_number(
                model=Invoice,
                field_name="invoice_number",
                prefix="LKP-INV",
            ),
        )

        values.setdefault(
            "issue_date",
            timezone.localdate(),
        )

        values.setdefault(
            "due_date",
            timezone.localdate() + timedelta(days=14),
        )

        values["currency"] = values.get(
            "currency",
            "LKR",
        ).upper()

        invoice = Invoice.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        for index, item_values in enumerate(items):
            calculated = FinanceService.calculate_invoice_item(
                {
                    **item_values,
                    "sort_order": item_values.get(
                        "sort_order",
                        index,
                    ),
                }
            )

            InvoiceItem.objects.create(
                invoice=invoice,
                created_by=request.auth,
                updated_by=request.auth,
                **calculated,
            )

        totals = invoice.items.aggregate(
            subtotal=Sum("subtotal"),
            tax=Sum("tax_amount"),
            total=Sum("total_amount"),
        )

        invoice.subtotal = totals["subtotal"] or Decimal(
            "0.00"
        )
        invoice.tax_amount = totals["tax"] or Decimal(
            "0.00"
        )

        invoice.discount_amount = money(
            min(
                max(
                    invoice.discount_amount,
                    Decimal("0.00"),
                ),
                invoice.subtotal,
            )
        )

        invoice.total_amount = money(
            (totals["total"] or Decimal("0.00"))
            - invoice.discount_amount
        )
        invoice.balance_due = invoice.total_amount

        invoice.save(
            update_fields=[
                "subtotal",
                "tax_amount",
                "discount_amount",
                "total_amount",
                "balance_due",
                "updated_at",
            ],
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="finance",
            message="Invoice created.",
            target_type="finance.Invoice",
            target_id=str(invoice.pk),
            after={
                "invoice_number": invoice.invoice_number,
                "client_id": str(invoice.client_id),
                "total_amount": str(
                    invoice.total_amount
                ),
                "currency": invoice.currency,
            },
        )

        return invoice

    @staticmethod
    @transaction.atomic
    def record_payment(
        *,
        request,
        invoice: Invoice,
        account: Account,
        income_account: Account,
        payment_date,
        amount: Decimal,
        method: str,
        reference: str = "",
        notes: str = "",
    ) -> Payment:
        amount = money(amount)

        if amount <= Decimal("0.00"):
            raise ValueError(
                "Payment amount must be greater than zero."
            )

        if invoice.status == InvoiceStatus.CANCELLED:
            raise ValueError(
                "A cancelled invoice cannot receive payments."
            )

        if amount > invoice.balance_due:
            raise ValueError(
                "Payment exceeds the invoice balance."
            )

        finance_transaction = (
            FinanceService.post_transaction(
                request=request,
                transaction_type=TransactionType.INCOME,
                transaction_date=payment_date,
                description=(
                    f"Payment for invoice "
                    f"{invoice.invoice_number}"
                ),
                reference=reference,
                entries=[
                    {
                        "account": account,
                        "debit": amount,
                        "credit": Decimal("0.00"),
                        "narration": "Payment received",
                    },
                    {
                        "account": income_account,
                        "debit": Decimal("0.00"),
                        "credit": amount,
                        "narration": "Income recognised",
                    },
                ],
            )
        )

        payment = Payment.objects.create(
            payment_number=FinanceService.generate_number(
                model=Payment,
                field_name="payment_number",
                prefix="LKP-PAY",
            ),
            invoice=invoice,
            client=invoice.client,
            project=invoice.project,
            account=account,
            transaction=finance_transaction,
            payment_date=payment_date,
            amount=amount,
            currency=invoice.currency,
            method=method,
            status=PaymentStatus.COMPLETED,
            reference=reference,
            notes=notes,
            created_by=request.auth,
            updated_by=request.auth,
        )

        invoice.paid_amount = money(
            invoice.paid_amount + amount
        )
        invoice.balance_due = money(
            invoice.total_amount - invoice.paid_amount
        )

        if invoice.balance_due == Decimal("0.00"):
            invoice.status = InvoiceStatus.PAID
            invoice.paid_at = timezone.now()
        else:
            invoice.status = InvoiceStatus.PARTIALLY_PAID

        invoice.updated_by = request.auth
        invoice.save(
            update_fields=[
                "paid_amount",
                "balance_due",
                "status",
                "paid_at",
                "updated_by",
                "updated_at",
            ],
        )

        return payment

    @staticmethod
    @transaction.atomic
    def record_expense(
        *,
        request,
        account: Account,
        expense_account: Account,
        expense_date,
        category: str,
        vendor: str,
        description: str,
        amount: Decimal,
        currency: str = "LKR",
        reference: str = "",
        project=None,
        notes: str = "",
    ) -> Expense:
        amount = money(amount)

        if amount <= Decimal("0.00"):
            raise ValueError(
                "Expense amount must be greater than zero."
            )

        finance_transaction = (
            FinanceService.post_transaction(
                request=request,
                transaction_type=TransactionType.EXPENSE,
                transaction_date=expense_date,
                description=description,
                reference=reference,
                entries=[
                    {
                        "account": expense_account,
                        "debit": amount,
                        "credit": Decimal("0.00"),
                        "narration": description,
                    },
                    {
                        "account": account,
                        "debit": Decimal("0.00"),
                        "credit": amount,
                        "narration": "Expense payment",
                    },
                ],
            )
        )

        expense = Expense.objects.create(
            expense_number=FinanceService.generate_number(
                model=Expense,
                field_name="expense_number",
                prefix="LKP-EXP",
            ),
            account=account,
            expense_account=expense_account,
            project=project,
            transaction=finance_transaction,
            expense_date=expense_date,
            category=category,
            status=ExpenseStatus.PAID,
            vendor=vendor,
            description=description,
            amount=amount,
            currency=currency.upper(),
            reference=reference,
            notes=notes,
            created_by=request.auth,
            updated_by=request.auth,
        )

        return expense
