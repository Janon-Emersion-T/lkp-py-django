from datetime import datetime
from typing import Literal
from uuid import UUID

from ninja import Schema
from pydantic import Field


SubscriberStatusValue = Literal[
    "pending",
    "active",
    "unsubscribed",
    "bounced",
    "complained",
    "suppressed",
]

SubscriptionSourceValue = Literal[
    "website",
    "manual",
    "import",
    "contact_form",
    "quote_form",
    "careers",
    "client_portal",
    "other",
]


class PublicNewsletterSubscribeSchema(Schema):
    email: str
    consent_given: bool = True
    source_reference: str = "website-footer"


class PublicNewsletterSubscribeResponseSchema(Schema):
    status: str
    message: str


class NewsletterListCreateSchema(Schema):
    name: str
    slug: str
    description: str = ""
    is_default: bool = False
    is_public: bool = False
    is_active: bool = True
    sort_order: int = 0


class NewsletterListSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str
    is_default: bool
    is_public: bool
    is_active: bool
    sort_order: int
    subscriber_count: int


class NewsletterTagCreateSchema(Schema):
    name: str
    slug: str
    description: str = ""
    color: str = ""
    is_active: bool = True


class NewsletterTagSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str
    color: str
    is_active: bool
    subscriber_count: int


class SubscriberCreateSchema(Schema):
    email: str
    first_name: str = ""
    last_name: str = ""
    company_name: str = ""
    phone: str = ""
    country: str = ""
    language: str = "en"
    status: SubscriberStatusValue = "pending"
    source: SubscriptionSourceValue = "manual"
    source_reference: str = ""
    consent_given: bool = False
    consent_ip_address: str | None = None
    consent_user_agent: str = ""
    metadata: dict = Field(default_factory=dict)
    list_ids: list[UUID] = Field(default_factory=list)
    tag_ids: list[UUID] = Field(default_factory=list)


class SubscriberUpdateSchema(SubscriberCreateSchema):
    pass


class SubscriberSchema(Schema):
    id: UUID
    email: str
    first_name: str
    last_name: str
    full_name: str
    company_name: str
    phone: str
    country: str
    language: str
    status: str
    source: str
    source_reference: str
    consent_given: bool
    subscribed_at: datetime
    confirmed_at: datetime | None
    unsubscribed_at: datetime | None
    confirmation_token: str
    unsubscribe_token: str
    bounce_count: int
    last_bounced_at: datetime | None
    last_email_sent_at: datetime | None
    metadata: dict
    can_receive_email: bool
    lists: list[NewsletterListSchema]
    tags: list[NewsletterTagSchema]
    created_at: datetime
    updated_at: datetime



CampaignStatusValue = Literal[
    "draft",
    "review",
    "scheduled",
    "queued",
    "sending",
    "sent",
    "paused",
    "cancelled",
    "failed",
    "archived",
]


class NewsletterCampaignCreateSchema(Schema):
    name: str
    subject: str
    preview_text: str = ""
    from_name: str = "LKProfessionals"
    from_email: str
    reply_to_email: str = ""
    html_content: str = ""
    text_content: str = ""
    status: CampaignStatusValue = "draft"
    metadata: dict = Field(default_factory=dict)
    list_ids: list[UUID] = Field(default_factory=list)
    tag_ids: list[UUID] = Field(default_factory=list)


class NewsletterCampaignUpdateSchema(
    NewsletterCampaignCreateSchema
):
    pass


class NewsletterCampaignScheduleSchema(Schema):
    scheduled_for: datetime


class CampaignRecipientSchema(Schema):
    id: UUID
    subscriber_id: UUID | None
    email: str
    first_name: str
    last_name: str
    status: str
    queued_at: datetime | None
    sent_at: datetime | None
    delivered_at: datetime | None
    opened_at: datetime | None
    clicked_at: datetime | None
    bounced_at: datetime | None
    complained_at: datetime | None
    unsubscribed_at: datetime | None
    failed_at: datetime | None
    failure_reason: str
    provider_message_id: str
    open_count: int
    click_count: int


class NewsletterCampaignSchema(Schema):
    id: UUID
    name: str
    subject: str
    preview_text: str
    from_name: str
    from_email: str
    reply_to_email: str
    html_content: str
    text_content: str
    status: str
    scheduled_for: datetime | None
    queued_at: datetime | None
    sending_started_at: datetime | None
    sent_at: datetime | None
    completed_at: datetime | None
    failure_reason: str
    recipient_count: int
    queued_count: int
    sent_count: int
    delivered_count: int
    opened_count: int
    clicked_count: int
    bounced_count: int
    complained_count: int
    unsubscribed_count: int
    failed_count: int
    open_rate: float
    click_rate: float
    metadata: dict
    lists: list[NewsletterListSchema]
    tags: list[NewsletterTagSchema]
    created_at: datetime
    updated_at: datetime


class NewsletterDashboardSchema(Schema):
    total_subscribers: int
    active_subscribers: int
    pending_subscribers: int
    unsubscribed_subscribers: int
    bounced_subscribers: int
    total_campaigns: int
    draft_campaigns: int
    scheduled_campaigns: int
    sent_campaigns: int
    total_emails_sent: int
    total_delivered: int
    total_opened: int
    total_clicked: int
