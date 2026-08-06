from datetime import datetime
from typing import Literal
from uuid import UUID

from ninja import Schema
from pydantic import Field


TestimonialStatusValue = Literal[
    "draft",
    "review",
    "scheduled",
    "published",
    "archived",
]

TestimonialSourceValue = Literal[
    "direct",
    "google",
    "facebook",
    "linkedin",
    "whatsapp",
    "email",
    "other",
]


class TestimonialCreateSchema(Schema):
    client_id: UUID | None = None
    project_id: UUID | None = None
    author_name: str = Field(min_length=1, max_length=200)
    author_position: str = Field(default="", max_length=200)
    company_name: str = Field(default="", max_length=250)
    content: str = Field(min_length=1)
    short_content: str = Field(default="", max_length=400)
    rating: int = Field(default=5, ge=1, le=5)
    source: TestimonialSourceValue = "direct"
    source_url: str = ""
    author_image_id: UUID | None = None
    company_logo_id: UUID | None = None
    status: TestimonialStatusValue = "draft"
    published_at: datetime | None = None
    scheduled_for: datetime | None = None
    is_featured: bool = False
    is_verified: bool = False
    is_active: bool = True
    sort_order: int = Field(default=0, ge=0)
    internal_notes: str = ""


class TestimonialUpdateSchema(TestimonialCreateSchema):
    pass


class TestimonialScheduleSchema(Schema):
    scheduled_for: datetime


class TestimonialSchema(Schema):
    id: UUID
    client_id: UUID | None
    client_name: str | None
    project_id: UUID | None
    project_title: str | None
    author_name: str
    author_position: str
    company_name: str
    content: str
    short_content: str
    rating: int
    source: str
    source_url: str
    author_image_id: UUID | None
    company_logo_id: UUID | None
    status: str
    published_at: datetime | None
    scheduled_for: datetime | None
    is_featured: bool
    is_verified: bool
    is_active: bool
    is_publicly_available: bool
    sort_order: int
    internal_notes: str
    created_at: datetime
    updated_at: datetime
