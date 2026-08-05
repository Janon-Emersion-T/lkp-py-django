from datetime import datetime
from typing import Any
from uuid import UUID

from ninja import Schema
from pydantic import Field


class IndustryServiceInputSchema(Schema):
    service_id: UUID
    description: str = ""
    sort_order: int = Field(default=0, ge=0)
    is_featured: bool = False


class IndustryFaqInputSchema(Schema):
    question: str = Field(min_length=1, max_length=300)
    answer: str = Field(min_length=1)
    sort_order: int = Field(default=0, ge=0)


class IndustrySeoInputSchema(Schema):
    meta_title: str = Field(default="", max_length=70)
    meta_description: str = Field(
        default="",
        max_length=170,
    )
    canonical_url: str = ""
    robots_index: bool = True
    robots_follow: bool = True
    open_graph_title: str = Field(
        default="",
        max_length=100,
    )
    open_graph_description: str = Field(
        default="",
        max_length=200,
    )
    open_graph_image_id: UUID | None = None
    twitter_title: str = Field(
        default="",
        max_length=100,
    )
    twitter_description: str = Field(
        default="",
        max_length=200,
    )
    structured_data: dict[str, Any] = Field(
        default_factory=dict,
    )


class IndustryCreateSchema(Schema):
    name: str = Field(min_length=1, max_length=250)
    slug: str = Field(min_length=1, max_length=250)
    short_description: str = Field(
        default="",
        max_length=350,
    )
    description: dict[str, Any] = Field(
        default_factory=dict,
    )
    hero_title: str = Field(default="", max_length=250)
    hero_description: str = ""
    hero_image_id: UUID | None = None
    icon: str = Field(default="", max_length=100)
    status: str = "draft"
    is_featured: bool = False
    is_active: bool = True
    sort_order: int = Field(default=0, ge=0)
    challenges: list[Any] = Field(default_factory=list)
    solutions: list[Any] = Field(default_factory=list)
    benefits: list[Any] = Field(default_factory=list)
    cta_title: str = Field(default="", max_length=200)
    cta_text: str = Field(default="", max_length=300)
    cta_label: str = Field(default="", max_length=100)
    cta_url: str = Field(default="", max_length=500)
    services: list[IndustryServiceInputSchema] = Field(
        default_factory=list,
    )
    faqs: list[IndustryFaqInputSchema] = Field(
        default_factory=list,
    )
    seo: IndustrySeoInputSchema = Field(
        default_factory=IndustrySeoInputSchema,
    )


class IndustryUpdateSchema(IndustryCreateSchema):
    change_summary: str = Field(
        default="",
        max_length=300,
    )


class IndustryScheduleSchema(Schema):
    scheduled_for: datetime


class IndustrySchema(Schema):
    id: UUID
    name: str
    slug: str
    short_description: str
    description: dict[str, Any]
    hero_title: str
    hero_description: str
    hero_image_id: UUID | None
    icon: str
    status: str
    published_at: datetime | None
    scheduled_for: datetime | None
    is_featured: bool
    is_active: bool
    is_publicly_available: bool
    sort_order: int
    challenges: list[Any]
    solutions: list[Any]
    benefits: list[Any]
    cta_title: str
    cta_text: str
    cta_label: str
    cta_url: str
    current_revision_number: int
    services: list[dict[str, Any]]
    faqs: list[dict[str, Any]]
    seo: dict[str, Any] | None
    revisions: list[dict[str, Any]]
    created_at: datetime
    updated_at: datetime
