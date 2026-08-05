from datetime import datetime
from typing import Any
from uuid import UUID

from ninja import Schema
from pydantic import Field


class CategoryCreateSchema(Schema):
    name: str = Field(min_length=1, max_length=150)
    slug: str = Field(min_length=1, max_length=170)
    description: str = ""
    parent_id: UUID | None = None
    is_active: bool = True
    sort_order: int = Field(default=0, ge=0)


class CategorySchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str
    parent_id: UUID | None
    is_active: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime


class TagCreateSchema(Schema):
    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=1, max_length=120)
    description: str = ""
    is_active: bool = True


class TagSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class InternalLinkInputSchema(Schema):
    target_article_id: UUID
    anchor_text: str = Field(min_length=1, max_length=250)
    context: str = ""
    is_active: bool = True


class InsightSeoInputSchema(Schema):
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

    article_schema: dict[str, Any] = Field(
        default_factory=dict,
    )
    faq_schema: list[dict[str, Any]] = Field(
        default_factory=list,
    )


class InsightArticleCreateSchema(Schema):
    title: str = Field(min_length=1, max_length=300)
    slug: str = Field(min_length=1, max_length=320)
    excerpt: str = ""
    content: dict[str, Any] = Field(default_factory=dict)

    category_id: UUID | None = None
    tag_ids: list[UUID] = Field(default_factory=list)
    author_id: int | None = None
    featured_image_id: UUID | None = None

    status: str = "draft"
    is_featured: bool = False
    is_active: bool = True
    allow_comments: bool = False

    related_article_ids: list[UUID] = Field(
        default_factory=list,
    )

    internal_links: list[
        InternalLinkInputSchema
    ] = Field(default_factory=list)

    seo: InsightSeoInputSchema = Field(
        default_factory=InsightSeoInputSchema,
    )


class InsightArticleUpdateSchema(
    InsightArticleCreateSchema
):
    change_summary: str = Field(
        default="",
        max_length=300,
    )


class InsightScheduleSchema(Schema):
    scheduled_for: datetime


class InsightRevisionSchema(Schema):
    id: UUID
    revision_number: int
    snapshot: dict[str, Any]
    change_summary: str
    created_at: datetime


class InsightArticleSchema(Schema):
    id: UUID
    title: str
    slug: str
    excerpt: str
    content: dict[str, Any]

    category_id: UUID | None
    category_name: str | None

    author_id: int | None
    author_email: str | None

    featured_image_id: UUID | None

    status: str
    published_at: datetime | None
    scheduled_for: datetime | None

    reading_time_minutes: int
    word_count: int
    view_count: int

    is_featured: bool
    is_active: bool
    allow_comments: bool
    is_publicly_available: bool

    current_revision_number: int

    tags: list[dict[str, Any]]
    related_articles: list[dict[str, Any]]
    internal_links: list[dict[str, Any]]

    seo: dict[str, Any] | None
    revisions: list[InsightRevisionSchema]
    publishing_events: list[dict[str, Any]]

    created_at: datetime
    updated_at: datetime
