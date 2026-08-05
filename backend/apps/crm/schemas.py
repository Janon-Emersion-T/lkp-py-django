from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr, Field


class UserSummarySchema(Schema):
    id: int
    email: str
    first_name: str
    last_name: str


class LeadSchema(Schema):
    id: UUID
    name: str
    company: str
    email: str
    phone: str
    whatsapp: str
    country: str
    website: str
    source: str
    status: str
    priority: str
    assigned_to: UserSummarySchema | None
    lead_score: int
    estimated_value: Decimal | None
    currency: str
    notes: str
    tags: list[str]
    next_follow_up_at: datetime | None
    last_contacted_at: datetime | None
    created_at: datetime
    updated_at: datetime


class LeadCreateSchema(Schema):
    name: str = Field(min_length=1, max_length=200)
    company: str = Field(default="", max_length=200)
    email: EmailStr | None = None
    phone: str = Field(default="", max_length=40)
    whatsapp: str = Field(default="", max_length=40)
    country: str = Field(default="", max_length=100)
    website: str = ""
    source: str = "manual"
    status: str = "new"
    priority: str = "normal"
    assigned_to_id: int | None = None
    lead_score: int = Field(default=0, ge=0, le=100)
    estimated_value: Decimal | None = None
    currency: str = Field(default="LKR", min_length=3, max_length=3)
    notes: str = ""
    tags: list[str] = Field(default_factory=list)
    next_follow_up_at: datetime | None = None


class LeadUpdateSchema(LeadCreateSchema):
    pass


class LeadNoteCreateSchema(Schema):
    content: str = Field(min_length=1)
    is_pinned: bool = False


class LeadNoteSchema(Schema):
    id: UUID
    content: str
    is_pinned: bool
    created_at: datetime


class LeadTimelineSchema(Schema):
    id: UUID
    event_type: str
    description: str
    metadata: dict[str, Any]
    created_at: datetime
