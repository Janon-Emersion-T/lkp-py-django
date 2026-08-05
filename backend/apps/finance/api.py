from decimal import Decimal

from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.api.exceptions import ApiHttpError
from apps.api.pagination_schemas import PaginatedResponseSchema
from apps.api.responses import paginated_response
from apps.clients.models import Client
from apps.common.pagination import paginate_queryset
from apps.projects.models import Project
from apps.quotations.models import Quotation
from apps.rbac.services import require_permissions

from .models import (
    Account,
    AccountType,
    Expense,
    Invoice,
    Payment,
)
from .repositories import (
    AccountRepository,
    ExpenseRepository,
    InvoiceRepository,
    PaymentRepository,
    TransactionRepository,
)
from .schemas import (
    AccountCreateSchema,
    AccountSchema,
    ExpenseCreateSchema,
    ExpenseSchema,
    FinanceSummarySchema,
    InvoiceCreateSchema,
    InvoiceSchema,
    PaymentCreateSchema,
    PaymentSchema,
    TransactionCreateSchema,
    TransactionSchema,
)
from .services import FinanceService


router = Router(
    tags=["Finance"],
    auth=jwt_auth,
)


def get_account(account_id):
    account = Account.objects.filter(pk=account_id).first()

    if account is None:
        raise ApiHttpError(
            400,
            "Finance account not found.",
            code="invalid_account",
        )

    return account


def get_client(client_id):
    client = Client.objects.filter(pk=client_id).first()

    if client is None:
        raise ApiHttpError(
            400,
            "Client not found.",
            code="invalid_client",
        )

    return client


def get_project(project_id):
    if project_id is None:
        return None

    project = Project.objects.filter(pk=project_id).first()

    if project is None:
        raise ApiHttpError(
            400,
            "Project not found.",
            code="invalid_project",
        )

    return project


def get_quotation(quotation_id):
    if quotation_id is None:
        return None

    quotation = Quotation.objects.filter(
        pk=quotation_id,
    ).first()

    if quotation is None:
        raise ApiHttpError(
            400,
            "Quotation not found.",
            code="invalid_quotation",
        )

    return quotation


def get_invoice(invoice_id):
    invoice = InvoiceRepository.find_by_id(invoice_id)

    if invoice is None:
        raise ApiHttpError(
            404,
            "Invoice not found.",
            code="invoice_not_found",
        )

    return invoice


def serialize_account(account):
    return {
        "id": account.id,
        "account_code": account.account_code,
        "name": account.name,
        "account_type": account.account_type,
        "description": account.description,
        "opening_balance": account.opening_balance,
        "current_balance": account.current_balance,
        "currency": account.currency,
        "is_system": account.is_system,
        "is_active": account.is_active,
        "created_at": account.created_at,
        "updated_at": account.updated_at,
    }


def serialize_entry(entry):
    return {
        "id": entry.id,
        "account_id": entry.account_id,
        "account_code": entry.account.account_code,
        "account_name": entry.account.name,
        "debit": entry.debit,
        "credit": entry.credit,
        "narration": entry.narration,
    }


def serialize_transaction(finance_transaction):
    return {
        "id": finance_transaction.id,
        "transaction_number": (
            finance_transaction.transaction_number
        ),
        "transaction_type": (
            finance_transaction.transaction_type
        ),
        "transaction_date": (
            finance_transaction.transaction_date
        ),
        "description": finance_transaction.description,
        "reference": finance_transaction.reference,
        "total_amount": finance_transaction.total_amount,
        "entries": [
            serialize_entry(entry)
            for entry in finance_transaction.entries.all()
        ],
        "created_at": finance_transaction.created_at,
    }


def serialize_invoice_item(item):
    return {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "quantity": item.quantity,
        "unit_price": item.unit_price,
        "discount_amount": item.discount_amount,
        "tax_rate": item.tax_rate,
        "subtotal": item.subtotal,
        "tax_amount": item.tax_amount,
        "total_amount": item.total_amount,
        "sort_order": item.sort_order,
    }


def serialize_invoice(invoice):
    return {
        "id": invoice.id,
        "invoice_number": invoice.invoice_number,
        "client_id": invoice.client_id,
        "client_name": invoice.client.company_name,
        "project_id": invoice.project_id,
        "quotation_id": invoice.quotation_id,
        "status": invoice.status,
        "issue_date": invoice.issue_date,
        "due_date": invoice.due_date,
        "currency": invoice.currency,
        "subtotal": invoice.subtotal,
        "discount_amount": invoice.discount_amount,
        "tax_amount": invoice.tax_amount,
        "total_amount": invoice.total_amount,
        "paid_amount": invoice.paid_amount,
        "balance_due": invoice.balance_due,
        "notes": invoice.notes,
        "terms": invoice.terms,
        "sent_at": invoice.sent_at,
        "paid_at": invoice.paid_at,
        "items": [
            serialize_invoice_item(item)
            for item in invoice.items.all()
        ],
        "created_at": invoice.created_at,
        "updated_at": invoice.updated_at,
    }


def serialize_payment(payment):
    return {
        "id": payment.id,
        "payment_number": payment.payment_number,
        "invoice_id": payment.invoice_id,
        "client_id": payment.client_id,
        "project_id": payment.project_id,
        "account_id": payment.account_id,
        "transaction_id": payment.transaction_id,
        "payment_date": payment.payment_date,
        "amount": payment.amount,
        "currency": payment.currency,
        "method": payment.method,
        "status": payment.status,
        "reference": payment.reference,
        "notes": payment.notes,
        "created_at": payment.created_at,
    }


def serialize_expense(expense):
    return {
        "id": expense.id,
        "expense_number": expense.expense_number,
        "account_id": expense.account_id,
        "expense_account_id": expense.expense_account_id,
        "project_id": expense.project_id,
        "transaction_id": expense.transaction_id,
        "expense_date": expense.expense_date,
        "category": expense.category,
        "status": expense.status,
        "vendor": expense.vendor,
        "description": expense.description,
        "amount": expense.amount,
        "currency": expense.currency,
        "reference": expense.reference,
        "notes": expense.notes,
        "created_at": expense.created_at,
    }


@router.get(
    "/accounts",
    response={
        200: PaginatedResponseSchema[AccountSchema],
        403: ErrorSchema,
    },
)
@require_permissions("finance.view_account")
def list_accounts(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    account_type: str | None = None,
    is_active: bool | None = None,
    ordering: str | None = None,
):
    result = paginate_queryset(
        AccountRepository.search(
            search=search,
            account_type=account_type,
            is_active=is_active,
            ordering=ordering,
        ),
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_account,
    )


@router.post(
    "/accounts",
    response={
        201: AccountSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("finance.add_account")
def create_account(request, payload: AccountCreateSchema):
    if Account.all_objects.filter(
        account_code=payload.account_code,
    ).exists():
        raise ApiHttpError(
            400,
            "Account code already exists.",
            code="duplicate_account_code",
        )

    account = FinanceService.create_account(
        request=request,
        values=payload.dict(),
    )

    return 201, serialize_account(account)


@router.get(
    "/transactions",
    response={
        200: PaginatedResponseSchema[TransactionSchema],
        403: ErrorSchema,
    },
)
@require_permissions("finance.view_transaction")
def list_transactions(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    transaction_type: str | None = None,
    ordering: str | None = None,
):
    result = paginate_queryset(
        TransactionRepository.search(
            search=search,
            transaction_type=transaction_type,
            ordering=ordering,
        ),
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_transaction,
    )


@router.post(
    "/transactions",
    response={
        201: TransactionSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("finance.add_transaction")
def post_transaction(
    request,
    payload: TransactionCreateSchema,
):
    entries = [
        {
            "account": get_account(entry.account_id),
            "debit": entry.debit,
            "credit": entry.credit,
            "narration": entry.narration,
        }
        for entry in payload.entries
    ]

    try:
        finance_transaction = (
            FinanceService.post_transaction(
                request=request,
                transaction_type=payload.transaction_type,
                transaction_date=payload.transaction_date,
                description=payload.description,
                reference=payload.reference,
                entries=entries,
            )
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_ledger_transaction",
        ) from exc

    return 201, serialize_transaction(
        finance_transaction
    )


@router.get(
    "/invoices",
    response={
        200: PaginatedResponseSchema[InvoiceSchema],
        403: ErrorSchema,
    },
)
@require_permissions("finance.view_invoice")
def list_invoices(
    request,
    page: int = 1,
    page_size: int = 25,
):
    result = paginate_queryset(
        InvoiceRepository.queryset().order_by(
            "-issue_date",
            "-created_at",
        ),
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_invoice,
    )


@router.post(
    "/invoices",
    response={
        201: InvoiceSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("finance.add_invoice")
def create_invoice(request, payload: InvoiceCreateSchema):
    values = {
        "client": get_client(payload.client_id),
        "project": get_project(payload.project_id),
        "quotation": get_quotation(
            payload.quotation_id
        ),
        "currency": payload.currency,
        "discount_amount": payload.discount_amount,
        "notes": payload.notes,
        "terms": payload.terms,
    }

    if payload.issue_date:
        values["issue_date"] = payload.issue_date

    if payload.due_date:
        values["due_date"] = payload.due_date

    invoice = FinanceService.create_invoice(
        request=request,
        values=values,
        items=[
            item.dict()
            for item in payload.items
        ],
    )

    return 201, serialize_invoice(invoice)


@router.get(
    "/invoices/{invoice_id}",
    response={
        200: InvoiceSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("finance.view_invoice")
def invoice_detail(request, invoice_id: str):
    return serialize_invoice(
        get_invoice(invoice_id)
    )


@router.post(
    "/payments",
    response={
        201: PaymentSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("finance.add_payment")
def record_payment(
    request,
    payload: PaymentCreateSchema,
):
    try:
        payment = FinanceService.record_payment(
            request=request,
            invoice=get_invoice(payload.invoice_id),
            account=get_account(payload.account_id),
            income_account=get_account(
                payload.income_account_id
            ),
            payment_date=payload.payment_date,
            amount=payload.amount,
            method=payload.method,
            reference=payload.reference,
            notes=payload.notes,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_payment",
        ) from exc

    return 201, serialize_payment(payment)


@router.get(
    "/payments",
    response={
        200: PaginatedResponseSchema[PaymentSchema],
        403: ErrorSchema,
    },
)
@require_permissions("finance.view_payment")
def list_payments(
    request,
    page: int = 1,
    page_size: int = 25,
):
    result = paginate_queryset(
        PaymentRepository.queryset().order_by(
            "-payment_date",
            "-created_at",
        ),
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_payment,
    )


@router.post(
    "/expenses",
    response={
        201: ExpenseSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("finance.add_expense")
def record_expense(
    request,
    payload: ExpenseCreateSchema,
):
    try:
        expense = FinanceService.record_expense(
            request=request,
            account=get_account(payload.account_id),
            expense_account=get_account(
                payload.expense_account_id
            ),
            project=get_project(payload.project_id),
            expense_date=payload.expense_date,
            category=payload.category,
            vendor=payload.vendor,
            description=payload.description,
            amount=payload.amount,
            currency=payload.currency,
            reference=payload.reference,
            notes=payload.notes,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_expense",
        ) from exc

    return 201, serialize_expense(expense)


@router.get(
    "/expenses",
    response={
        200: PaginatedResponseSchema[ExpenseSchema],
        403: ErrorSchema,
    },
)
@require_permissions("finance.view_expense")
def list_expenses(
    request,
    page: int = 1,
    page_size: int = 25,
):
    result = paginate_queryset(
        ExpenseRepository.queryset().order_by(
            "-expense_date",
            "-created_at",
        ),
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_expense,
    )


@router.get(
    "/summary",
    response={
        200: FinanceSummarySchema,
        403: ErrorSchema,
    },
)
@require_permissions("finance.view_account")
def finance_summary(request):
    totals = {
        account_type: sum(
            (
                account.current_balance
                for account in Account.objects.filter(
                    account_type=account_type,
                    is_active=True,
                )
            ),
            Decimal("0.00"),
        )
        for account_type in AccountType.values
    }

    receivables = sum(
        (
            invoice.balance_due
            for invoice in Invoice.objects.exclude(
                status__in=(
                    "paid",
                    "cancelled",
                ),
            )
        ),
        Decimal("0.00"),
    )

    return {
        "total_assets": totals[AccountType.ASSET],
        "total_liabilities": totals[
            AccountType.LIABILITY
        ],
        "total_equity": totals[AccountType.EQUITY],
        "total_income": totals[AccountType.INCOME],
        "total_expenses": totals[
            AccountType.EXPENSE
        ],
        "profit": (
            totals[AccountType.INCOME]
            - totals[AccountType.EXPENSE]
        ),
        "receivables": receivables,
    }
