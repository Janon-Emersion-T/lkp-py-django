from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from ninja import Schema
from pydantic import Field


class AccountCreateSchema(Schema):
    account_code: str = Field(min_length=1, max_length=30)
    name: str = Field(min_length=1, max_length=200)
    account_type: str
    description: str = ""
    opening_balance: Decimal = Decimal("0.00")
    currency: str = Field(default="LKR", min_length=3, max_length=3)
    is_system: bool = False
    is_active: bool = True


class AccountSchema(Schema):
    id: UUID
    account_code: str
    name: str
    account_type: str
    description: str
    opening_balance: Decimal
    current_balance: Decimal
    currency: str
    is_system: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


class LedgerEntryCreateSchema(Schema):
    account_id: UUID
    debit: Decimal = Field(default=Decimal("0.00"), ge=0)
    credit: Decimal = Field(default=Decimal("0.00"), ge=0)
    narration: str = Field(default="", max_length=300)


class LedgerEntrySchema(Schema):
    id: UUID
    account_id: UUID
    account_code: str
    account_name: str
    debit: Decimal
    credit: Decimal
    narration: str


class TransactionCreateSchema(Schema):
    transaction_type: str
    transaction_date: date
    description: str = Field(min_length=1, max_length=300)
    reference: str = Field(default="", max_length=120)
    entries: list[LedgerEntryCreateSchema] = Field(min_length=2)


class TransactionSchema(Schema):
    id: UUID
    transaction_number: str
    transaction_type: str
    transaction_date: date
    description: str
    reference: str
    total_amount: Decimal
    entries: list[LedgerEntrySchema]
    created_at: datetime


class InvoiceItemCreateSchema(Schema):
    title: str = Field(min_length=1, max_length=250)
    description: str = ""
    quantity: Decimal = Field(default=Decimal("1.00"), gt=0)
    unit_price: Decimal = Field(default=Decimal("0.00"), ge=0)
    discount_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    tax_rate: Decimal = Field(default=Decimal("0.00"), ge=0)
    sort_order: int = Field(default=0, ge=0)


class InvoiceItemSchema(Schema):
    id: UUID
    title: str
    description: str
    quantity: Decimal
    unit_price: Decimal
    discount_amount: Decimal
    tax_rate: Decimal
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    sort_order: int


class InvoiceCreateSchema(Schema):
    client_id: UUID
    project_id: UUID | None = None
    quotation_id: UUID | None = None
    issue_date: date | None = None
    due_date: date | None = None
    currency: str = Field(default="LKR", min_length=3, max_length=3)
    discount_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    notes: str = ""
    terms: str = ""
    items: list[InvoiceItemCreateSchema] = Field(default_factory=list)


class InvoiceSchema(Schema):
    id: UUID
    invoice_number: str
    client_id: UUID
    client_name: str
    project_id: UUID | None
    quotation_id: UUID | None
    status: str
    issue_date: date
    due_date: date | None
    currency: str
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    paid_amount: Decimal
    balance_due: Decimal
    notes: str
    terms: str
    sent_at: datetime | None
    paid_at: datetime | None
    items: list[InvoiceItemSchema]
    created_at: datetime
    updated_at: datetime


class PaymentCreateSchema(Schema):
    invoice_id: UUID
    account_id: UUID
    income_account_id: UUID
    payment_date: date
    amount: Decimal = Field(gt=0)
    method: str = "bank_transfer"
    reference: str = Field(default="", max_length=150)
    notes: str = ""


class PaymentSchema(Schema):
    id: UUID
    payment_number: str
    invoice_id: UUID | None
    client_id: UUID | None
    project_id: UUID | None
    account_id: UUID
    transaction_id: UUID | None
    payment_date: date
    amount: Decimal
    currency: str
    method: str
    status: str
    reference: str
    notes: str
    created_at: datetime


class ExpenseCreateSchema(Schema):
    account_id: UUID
    expense_account_id: UUID
    project_id: UUID | None = None
    expense_date: date
    category: str = "miscellaneous"
    vendor: str = Field(default="", max_length=200)
    description: str = Field(min_length=1, max_length=300)
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="LKR", min_length=3, max_length=3)
    reference: str = Field(default="", max_length=150)
    notes: str = ""


class ExpenseSchema(Schema):
    id: UUID
    expense_number: str
    account_id: UUID
    expense_account_id: UUID
    project_id: UUID | None
    transaction_id: UUID | None
    expense_date: date
    category: str
    status: str
    vendor: str
    description: str
    amount: Decimal
    currency: str
    reference: str
    notes: str
    created_at: datetime


class FinanceSummarySchema(Schema):
    total_assets: Decimal
    total_liabilities: Decimal
    total_equity: Decimal
    total_income: Decimal
    total_expenses: Decimal
    profit: Decimal
    receivables: Decimal
