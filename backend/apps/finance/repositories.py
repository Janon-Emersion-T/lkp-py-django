from django.db.models import QuerySet

from apps.common.query import (
    apply_ordering,
    apply_search,
)
from apps.common.repositories import BaseRepository

from .models import (
    Account,
    Expense,
    Invoice,
    Payment,
    Transaction,
)


class AccountRepository(BaseRepository[Account]):
    model = Account

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        account_type: str | None = None,
        is_active: bool | None = None,
        ordering: str | None = None,
    ) -> QuerySet[Account]:
        queryset = Account.objects.all()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "account_code",
                "name",
                "description",
            ),
        )

        if account_type:
            queryset = queryset.filter(
                account_type=account_type,
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        return apply_ordering(
            queryset,
            ordering=ordering,
            allowed_fields=(
                "account_code",
                "name",
                "account_type",
                "current_balance",
                "created_at",
            ),
            default="account_code",
        )


class TransactionRepository(BaseRepository[Transaction]):
    model = Transaction

    @classmethod
    def queryset(cls) -> QuerySet[Transaction]:
        return Transaction.objects.prefetch_related(
            "entries__account",
        )

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        transaction_type: str | None = None,
        ordering: str | None = None,
    ) -> QuerySet[Transaction]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "transaction_number",
                "description",
                "reference",
            ),
        )

        if transaction_type:
            queryset = queryset.filter(
                transaction_type=transaction_type,
            )

        return apply_ordering(
            queryset,
            ordering=ordering,
            allowed_fields=(
                "transaction_number",
                "transaction_date",
                "transaction_type",
                "total_amount",
                "created_at",
            ),
            default="-transaction_date",
        )


class InvoiceRepository(BaseRepository[Invoice]):
    model = Invoice

    @classmethod
    def queryset(cls) -> QuerySet[Invoice]:
        return (
            Invoice.objects.select_related(
                "client",
                "project",
                "quotation",
            )
            .prefetch_related(
                "items",
                "payments",
            )
        )


class PaymentRepository(BaseRepository[Payment]):
    model = Payment

    @classmethod
    def queryset(cls) -> QuerySet[Payment]:
        return Payment.objects.select_related(
            "invoice",
            "client",
            "project",
            "account",
            "transaction",
        )


class ExpenseRepository(BaseRepository[Expense]):
    model = Expense

    @classmethod
    def queryset(cls) -> QuerySet[Expense]:
        return Expense.objects.select_related(
            "account",
            "expense_account",
            "project",
            "transaction",
        )
