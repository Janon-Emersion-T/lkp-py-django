from datetime import datetime
from typing import Any
from uuid import UUID

from ninja import Schema
from pydantic import Field


class PageSeoInputSchema(Schema):
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


class PageSeoSchema(PageSeoInputSchema):
    id: UUID


class PageCreateSchema(Schema):
    title: str = Field(min_length=1, max_length=250)
    slug: str = Field(min_length=1, max_length=250)

    page_type: str = "generic"
    status: str = "draft"

    excerpt: str = ""
    content: dict[str, Any] = Field(default_factory=dict)

    template_name: str = Field(
        default="pages/default.html",
        max_length=150,
    )

    is_indexable: bool = True
    is_visible_in_navigation: bool = False

    navigation_label: str = Field(
        default="",
        max_length=100,
    )
    navigation_order: int = Field(default=0, ge=0)

    seo: PageSeoInputSchema = Field(
        default_factory=PageSeoInputSchema,
    )


class PageUpdateSchema(PageCreateSchema):
    change_summary: str = Field(
        default="",
        max_length=300,
    )


class PageRevisionSchema(Schema):
    id: UUID
    revision_number: int
    title: str
    excerpt: str
    content: dict[str, Any]
    status: str
    change_summary: str
    created_at: datetime


class PublishingEventSchema(Schema):
    id: UUID
    event_type: str
    description: str
    metadata: dict[str, Any]
    created_at: datetime


class PageSchema(Schema):
    id: UUID
    title: str
    slug: str
    page_type: str
    status: str
    excerpt: str
    content: dict[str, Any]
    template_name: str

    is_indexable: bool
    is_visible_in_navigation: bool
    navigation_label: str
    navigation_order: int

    published_at: datetime | None
    scheduled_for: datetime | None
    current_revision_number: int
    is_publicly_available: bool

    seo: PageSeoSchema | None
    revisions: list[PageRevisionSchema]
    publishing_events: list[PublishingEventSchema]

    created_at: datetime
    updated_at: datetime


class PageScheduleSchema(Schema):
    scheduled_for: datetime


class RevisionRestoreSchema(Schema):
    revision_id: UUID


class RedirectCreateSchema(Schema):
    source_path: str = Field(min_length=1, max_length=500)
    destination_url: str = Field(
        min_length=1,
        max_length=1000,
    )
    redirect_type: int = 301
    is_active: bool = True
    notes: str = ""


class RedirectSchema(Schema):
    id: UUID
    source_path: str
    destination_url: str
    redirect_type: int
    is_active: bool
    hit_count: int
    last_accessed_at: datetime | None
    notes: str
    created_at: datetime
    updated_at: datetime
