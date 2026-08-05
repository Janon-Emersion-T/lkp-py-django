from datetime import datetime
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr, Field


class ClientContactSchema(Schema):
    id: UUID
    first_name: str
    last_name: str
    position: str
    department: str
    email: str
    phone: str
    whatsapp: str
    is_primary: bool
    receives_quotations: bool
    receives_invoices: bool
    receives_project_updates: bool
    notes: str
    created_at: datetime


class ClientWebsiteSchema(Schema):
    id: UUID
    name: str
    url: str
    platform: str
    admin_url: str
    is_primary: bool
    is_active: bool
    notes: str
    created_at: datetime


class ClientSchema(Schema):
    id: UUID
    client_code: str
    company_name: str
    legal_name: str
    client_type: str
    status: str
    industry: str
    country: str
    timezone: str
    email: str
    phone: str
    whatsapp: str
    website: str
    tax_number: str
    registration_number: str
    billing_address: str
    shipping_address: str
    default_currency: str
    payment_terms_days: int
    notes: str
    tags: list[str]
    source_lead_id: UUID | None
    contacts: list[ClientContactSchema]
    websites: list[ClientWebsiteSchema]
    created_at: datetime
    updated_at: datetime


class ClientCreateSchema(Schema):
    company_name: str = Field(min_length=1, max_length=250)
    legal_name: str = Field(default="", max_length=250)
    client_type: str = "company"
    status: str = "active"
    industry: str = Field(default="", max_length=150)
    country: str = Field(default="", max_length=100)
    timezone: str = Field(default="Asia/Colombo", max_length=64)
    email: EmailStr | None = None
    phone: str = Field(default="", max_length=40)
    whatsapp: str = Field(default="", max_length=40)
    website: str = ""
    tax_number: str = Field(default="", max_length=100)
    registration_number: str = Field(default="", max_length=100)
    billing_address: str = ""
    shipping_address: str = ""
    default_currency: str = Field(
        default="LKR",
        min_length=3,
        max_length=3,
    )
    payment_terms_days: int = Field(default=14, ge=0, le=365)
    notes: str = ""
    tags: list[str] = Field(default_factory=list)


class ClientUpdateSchema(ClientCreateSchema):
    pass


class ClientContactCreateSchema(Schema):
    first_name: str = Field(min_length=1, max_length=150)
    last_name: str = Field(default="", max_length=150)
    position: str = Field(default="", max_length=150)
    department: str = Field(default="", max_length=150)
    email: EmailStr | None = None
    phone: str = Field(default="", max_length=40)
    whatsapp: str = Field(default="", max_length=40)
    is_primary: bool = False
    receives_quotations: bool = True
    receives_invoices: bool = True
    receives_project_updates: bool = True
    notes: str = ""


class ClientWebsiteCreateSchema(Schema):
    name: str = Field(min_length=1, max_length=200)
    url: str
    platform: str = Field(default="", max_length=100)
    admin_url: str = ""
    is_primary: bool = False
    is_active: bool = True
    notes: str = ""
