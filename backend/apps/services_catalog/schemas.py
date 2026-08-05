from datetime import datetime
from typing import Any
from uuid import UUID

from ninja import Schema
from pydantic import Field


class ServiceFeatureInputSchema(Schema):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    icon: str = Field(default="", max_length=100)
    sort_order: int = Field(default=0, ge=0)


class ServiceProcessStepInputSchema(Schema):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    step_number: int = Field(ge=1)
    sort_order: int = Field(default=0, ge=0)


class ServiceTechnologyInputSchema(Schema):
    name: str = Field(min_length=1, max_length=150)
    description: str = ""
    logo_id: UUID | None = None
    sort_order: int = Field(default=0, ge=0)


class ServiceFaqInputSchema(Schema):
    question: str = Field(min_length=1, max_length=300)
    answer: str = Field(min_length=1)
    sort_order: int = Field(default=0, ge=0)


class ServiceSeoInputSchema(Schema):
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


class ServiceCreateSchema(Schema):
    title: str = Field(min_length=1, max_length=250)
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
    status: str = "draft"
    icon: str = Field(default="", max_length=100)
    sort_order: int = Field(default=0, ge=0)
    is_featured: bool = False
    is_active: bool = True
    cta_title: str = Field(default="", max_length=200)
    cta_text: str = Field(default="", max_length=250)
    cta_label: str = Field(default="", max_length=100)
    cta_url: str = Field(default="", max_length=500)

    features: list[ServiceFeatureInputSchema] = Field(
        default_factory=list,
    )
    process_steps: list[
        ServiceProcessStepInputSchema
    ] = Field(default_factory=list)
    technologies: list[
        ServiceTechnologyInputSchema
    ] = Field(default_factory=list)
    faqs: list[ServiceFaqInputSchema] = Field(
        default_factory=list,
    )
    seo: ServiceSeoInputSchema = Field(
        default_factory=ServiceSeoInputSchema,
    )


class ServiceUpdateSchema(ServiceCreateSchema):
    change_summary: str = Field(
        default="",
        max_length=300,
    )


class ServiceScheduleSchema(Schema):
    scheduled_for: datetime


class ServiceFeatureSchema(ServiceFeatureInputSchema):
    id: UUID


class ServiceProcessStepSchema(
    ServiceProcessStepInputSchema
):
    id: UUID


class ServiceTechnologySchema(Schema):
    id: UUID
    name: str
    description: str
    logo_id: UUID | None
    sort_order: int


class ServiceFaqSchema(ServiceFaqInputSchema):
    id: UUID


class ServiceSeoSchema(Schema):
    id: UUID
    meta_title: str
    meta_description: str
    canonical_url: str
    robots_index: bool
    robots_follow: bool
    open_graph_title: str
    open_graph_description: str
    open_graph_image_id: UUID | None
    twitter_title: str
    twitter_description: str
    structured_data: dict[str, Any]


class ServiceRevisionSchema(Schema):
    id: UUID
    revision_number: int
    snapshot: dict[str, Any]
    change_summary: str
    created_at: datetime


class ServiceSchema(Schema):
    id: UUID
    title: str
    slug: str
    short_description: str
    description: dict[str, Any]
    hero_title: str
    hero_description: str
    hero_image_id: UUID | None
    status: str
    published_at: datetime | None
    scheduled_for: datetime | None
    icon: str
    sort_order: int
    is_featured: bool
    is_active: bool
    is_publicly_available: bool
    cta_title: str
    cta_text: str
    cta_label: str
    cta_url: str
    current_revision_number: int
    features: list[ServiceFeatureSchema]
    process_steps: list[ServiceProcessStepSchema]
    technologies: list[ServiceTechnologySchema]
    faqs: list[ServiceFaqSchema]
    seo: ServiceSeoSchema | None
    revisions: list[ServiceRevisionSchema]
    created_at: datetime
    updated_at: datetime
