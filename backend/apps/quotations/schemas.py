from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr, Field


class QuotationItemCreateSchema(Schema):
    title: str = Field(min_length=1, max_length=250)
    description: str = ""
    quantity: Decimal = Field(default=Decimal("1.00"), gt=0)
    unit_price: Decimal = Field(default=Decimal("0.00"), ge=0)
    discount_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    tax_rate: Decimal = Field(default=Decimal("0.00"), ge=0)
    sort_order: int = Field(default=0, ge=0)


class QuotationItemSchema(Schema):
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


class QuotationRecipientCreateSchema(Schema):
    name: str = Field(default="", max_length=200)
    email: EmailStr
    is_primary: bool = False


class QuotationRecipientSchema(Schema):
    id: UUID
    name: str
    email: str
    is_primary: bool
    received_at: datetime | None
    viewed_at: datetime | None


class QuotationEventSchema(Schema):
    id: UUID
    event_type: str
    description: str
    metadata: dict[str, Any]
    created_at: datetime


class QuotationSchema(Schema):
    id: UUID
    quotation_number: str
    client_id: UUID
    client_name: str
    lead_id: UUID | None
    title: str
    subject: str
    description: str
    status: str
    issue_date: date
    expiry_date: date | None
    currency: str
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    terms: str
    notes: str
    accepted_at: datetime | None
    accepted_by_name: str
    accepted_by_email: str
    sent_at: datetime | None
    duplicated_from_id: UUID | None
    is_expired: bool
    items: list[QuotationItemSchema]
    recipients: list[QuotationRecipientSchema]
    events: list[QuotationEventSchema]
    created_at: datetime
    updated_at: datetime


class QuotationCreateSchema(Schema):
    client_id: UUID
    lead_id: UUID | None = None
    title: str = Field(min_length=1, max_length=250)
    subject: str = Field(default="", max_length=250)
    description: str = ""
    issue_date: date | None = None
    expiry_date: date | None = None
    currency: str = Field(default="LKR", min_length=3, max_length=3)
    discount_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    tax_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    terms: str = ""
    notes: str = ""
    items: list[QuotationItemCreateSchema] = Field(default_factory=list)
    recipients: list[QuotationRecipientCreateSchema] = Field(
        default_factory=list
    )


class QuotationUpdateSchema(Schema):
    title: str = Field(min_length=1, max_length=250)
    subject: str = Field(default="", max_length=250)
    description: str = ""
    issue_date: date
    expiry_date: date | None = None
    currency: str = Field(min_length=3, max_length=3)
    discount_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    tax_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    terms: str = ""
    notes: str = ""
    items: list[QuotationItemCreateSchema] = Field(default_factory=list)
    recipients: list[QuotationRecipientCreateSchema] = Field(
        default_factory=list
    )


class QuotationAcceptSchema(Schema):
    accepted_by_name: str = Field(min_length=1, max_length=200)
    accepted_by_email: EmailStr


class QuotationRejectSchema(Schema):
    reason: str = ""


class QuotationPdfPayloadSchema(Schema):
    company: dict[str, Any]
    client: dict[str, Any]
    quotation: dict[str, Any]
    items: list[dict[str, Any]]
    totals: dict[str, Any]
