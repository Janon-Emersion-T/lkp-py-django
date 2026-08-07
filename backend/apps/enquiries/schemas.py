from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from ninja import Schema
from pydantic import Field


EnquiryStatusValue = Literal[
    "new",
    "assigned",
    "contacted",
    "qualified",
    "proposal_sent",
    "won",
    "lost",
    "spam",
    "archived",
]

EnquiryPriorityValue = Literal[
    "low",
    "normal",
    "high",
    "urgent",
]

EnquirySourceValue = Literal[
    "website",
    "google",
    "facebook",
    "instagram",
    "linkedin",
    "tiktok",
    "whatsapp",
    "referral",
    "email",
    "phone",
    "manual",
    "other",
]


PublicQuoteContactMethodValue = Literal[
    "email",
    "whatsapp",
]

PublicQuoteContactTimeValue = Literal[
    "",
    "morning",
    "afternoon",
    "evening",
    "anytime",
]

PublicQuoteSurfaceValue = Literal[
    "page",
    "modal",
]


class PublicQuoteRequestSchema(Schema):
    full_name: str
    company_name: str = ""
    service_required: str
    email: str
    whatsapp_number: str = ""
    preferred_contact_method: PublicQuoteContactMethodValue
    country: str
    project_description: str
    best_time_to_contact: PublicQuoteContactTimeValue = ""
    source_surface: PublicQuoteSurfaceValue = "page"
    source_url: str = ""


class PublicQuoteResponseSchema(Schema):
    status: str
    reference_code: str
    message: str


class ContactEnquiryCreateSchema(Schema):
    reference_code: str
    name: str
    email: str = ""
    phone: str = ""
    company_name: str = ""
    subject: str = ""
    message: str
    source: EnquirySourceValue = "website"
    source_url: str = ""
    priority: EnquiryPriorityValue = "normal"
    assigned_to_id: UUID | None = None
    client_id: UUID | None = None
    lead_id: UUID | None = None
    metadata: dict = Field(default_factory=dict)


class QuoteEnquiryServiceInputSchema(Schema):
    service_id: UUID
    notes: str = ""
    sort_order: int = 0


class QuoteEnquiryCreateSchema(Schema):
    reference_code: str
    name: str
    email: str = ""
    phone: str = ""
    company_name: str = ""
    country: str = ""
    website_url: str = ""
    project_title: str = ""
    project_description: str
    preferred_package_id: UUID | None = None
    budget_min: Decimal | None = None
    budget_max: Decimal | None = None
    budget_currency: str = "LKR"
    desired_start_date: date | None = None
    desired_completion_date: date | None = None
    source: EnquirySourceValue = "website"
    source_url: str = ""
    priority: EnquiryPriorityValue = "normal"
    assigned_to_id: UUID | None = None
    client_id: UUID | None = None
    lead_id: UUID | None = None
    metadata: dict = Field(default_factory=dict)
    services: list[
        QuoteEnquiryServiceInputSchema
    ] = Field(default_factory=list)


class EnquiryStatusUpdateSchema(Schema):
    status: EnquiryStatusValue
    loss_reason: str = ""


class EnquiryAssignmentSchema(Schema):
    assigned_to_id: UUID | None = None
    priority: EnquiryPriorityValue = "normal"
    internal_summary: str = ""
    next_follow_up_at: datetime | None = None


class EnquiryNoteCreateSchema(Schema):
    note: str
    is_private: bool = True


class EnquiryNoteSchema(Schema):
    id: UUID
    author_id: UUID | None
    author_name: str | None
    note: str
    is_private: bool
    created_at: datetime


class QuoteEnquiryServiceSchema(Schema):
    id: UUID
    service_id: UUID
    service_title: str
    notes: str
    sort_order: int


class ContactEnquirySchema(Schema):
    id: UUID
    reference_code: str
    name: str
    email: str
    phone: str
    company_name: str
    subject: str
    message: str
    source: str
    source_url: str
    status: str
    priority: str
    assigned_to_id: UUID | None
    assigned_to_name: str | None
    client_id: UUID | None
    lead_id: UUID | None
    submitted_at: datetime
    first_contacted_at: datetime | None
    resolved_at: datetime | None
    last_follow_up_at: datetime | None
    next_follow_up_at: datetime | None
    internal_summary: str
    loss_reason: str
    metadata: dict
    notes: list[EnquiryNoteSchema]
    created_at: datetime
    updated_at: datetime


class QuoteEnquirySchema(Schema):
    id: UUID
    reference_code: str
    name: str
    email: str
    phone: str
    company_name: str
    country: str
    website_url: str
    project_title: str
    project_description: str
    preferred_package_id: UUID | None
    budget_min: Decimal | None
    budget_max: Decimal | None
    budget_currency: str
    desired_start_date: date | None
    desired_completion_date: date | None
    source: str
    source_url: str
    status: str
    priority: str
    assigned_to_id: UUID | None
    assigned_to_name: str | None
    client_id: UUID | None
    lead_id: UUID | None
    quotation_id: UUID | None
    submitted_at: datetime
    first_contacted_at: datetime | None
    resolved_at: datetime | None
    last_follow_up_at: datetime | None
    next_follow_up_at: datetime | None
    internal_summary: str
    loss_reason: str
    metadata: dict
    services: list[QuoteEnquiryServiceSchema]
    notes: list[EnquiryNoteSchema]
    created_at: datetime
    updated_at: datetime



class ContactEnquiryUpdateSchema(
    ContactEnquiryCreateSchema
):
    pass


class QuoteEnquiryUpdateSchema(
    QuoteEnquiryCreateSchema
):
    pass


class EnquiryFollowUpSchema(Schema):
    next_follow_up_at: datetime | None = None


class EnquiryDashboardSchema(Schema):
    total_contact_enquiries: int
    total_quote_enquiries: int
    new_contact_enquiries: int
    new_quote_enquiries: int
    active_contact_enquiries: int
    active_quote_enquiries: int
    won_contact_enquiries: int
    won_quote_enquiries: int
    lost_contact_enquiries: int
    lost_quote_enquiries: int
    urgent_contact_enquiries: int
    urgent_quote_enquiries: int
    overdue_contact_follow_ups: int
    overdue_quote_follow_ups: int
    contact_enquiries_by_status: dict
    quote_enquiries_by_status: dict
    contact_enquiries_by_source: dict
    quote_enquiries_by_source: dict
