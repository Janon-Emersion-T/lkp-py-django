from datetime import date, datetime
from typing import Any
from uuid import UUID

from ninja import Schema
from pydantic import Field


class CaseStudyServiceInputSchema(Schema):
    service_id: UUID
    description: str = ""
    sort_order: int = Field(default=0, ge=0)


class CaseStudyTechnologyInputSchema(Schema):
    name: str = Field(min_length=1, max_length=150)
    description: str = ""
    logo_id: UUID | None = None
    sort_order: int = Field(default=0, ge=0)


class CaseStudyMediaInputSchema(Schema):
    asset_id: UUID
    title: str = Field(default="", max_length=200)
    caption: str = ""
    media_role: str = Field(
        default="gallery",
        max_length=50,
    )
    sort_order: int = Field(default=0, ge=0)


class CaseStudyMetricInputSchema(Schema):
    label: str = Field(min_length=1, max_length=150)
    value: str = Field(min_length=1, max_length=150)
    description: str = ""
    icon: str = Field(default="", max_length=100)
    sort_order: int = Field(default=0, ge=0)


class CaseStudyMilestoneInputSchema(Schema):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    milestone_date: date | None = None
    sort_order: int = Field(default=0, ge=0)


class CaseStudySeoInputSchema(Schema):
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


class CaseStudyCreateSchema(Schema):
    title: str = Field(min_length=1, max_length=300)
    slug: str = Field(min_length=1, max_length=320)

    client_id: UUID | None = None
    project_id: UUID | None = None
    industry_id: UUID | None = None

    client_name: str = Field(default="", max_length=250)
    location: str = Field(default="", max_length=200)
    website_url: str = ""

    short_description: str = Field(
        default="",
        max_length=400,
    )

    overview: dict[str, Any] = Field(default_factory=dict)
    challenge: dict[str, Any] = Field(default_factory=dict)
    solution: dict[str, Any] = Field(default_factory=dict)
    implementation: dict[str, Any] = Field(
        default_factory=dict,
    )
    results: dict[str, Any] = Field(default_factory=dict)

    testimonial: str = ""
    testimonial_author: str = Field(
        default="",
        max_length=200,
    )
    testimonial_position: str = Field(
        default="",
        max_length=200,
    )

    featured_image_id: UUID | None = None

    status: str = "draft"

    project_start_date: date | None = None
    project_completion_date: date | None = None
    project_duration: str = Field(
        default="",
        max_length=150,
    )

    is_featured: bool = False
    is_active: bool = True
    sort_order: int = Field(default=0, ge=0)

    services: list[CaseStudyServiceInputSchema] = Field(
        default_factory=list,
    )
    technologies: list[
        CaseStudyTechnologyInputSchema
    ] = Field(default_factory=list)
    media_items: list[
        CaseStudyMediaInputSchema
    ] = Field(default_factory=list)
    metrics: list[CaseStudyMetricInputSchema] = Field(
        default_factory=list,
    )
    milestones: list[
        CaseStudyMilestoneInputSchema
    ] = Field(default_factory=list)

    seo: CaseStudySeoInputSchema = Field(
        default_factory=CaseStudySeoInputSchema,
    )


class CaseStudyUpdateSchema(CaseStudyCreateSchema):
    change_summary: str = Field(
        default="",
        max_length=300,
    )


class CaseStudyScheduleSchema(Schema):
    scheduled_for: datetime


class CaseStudyRevisionSchema(Schema):
    id: UUID
    revision_number: int
    snapshot: dict[str, Any]
    change_summary: str
    created_at: datetime


class CaseStudySchema(Schema):
    id: UUID
    title: str
    slug: str

    client_id: UUID | None
    client_name: str
    linked_client_name: str | None

    project_id: UUID | None
    project_name: str | None

    industry_id: UUID | None
    industry_name: str | None

    location: str
    website_url: str
    short_description: str

    overview: dict[str, Any]
    challenge: dict[str, Any]
    solution: dict[str, Any]
    implementation: dict[str, Any]
    results: dict[str, Any]

    testimonial: str
    testimonial_author: str
    testimonial_position: str

    featured_image_id: UUID | None

    status: str
    published_at: datetime | None
    scheduled_for: datetime | None

    project_start_date: date | None
    project_completion_date: date | None
    project_duration: str

    is_featured: bool
    is_active: bool
    is_publicly_available: bool

    sort_order: int
    view_count: int
    current_revision_number: int

    services: list[dict[str, Any]]
    technologies: list[dict[str, Any]]
    media_items: list[dict[str, Any]]
    metrics: list[dict[str, Any]]
    milestones: list[dict[str, Any]]

    seo: dict[str, Any] | None
    revisions: list[CaseStudyRevisionSchema]

    created_at: datetime
    updated_at: datetime
