from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from ninja import Schema
from pydantic import Field


class PackageFeatureInputSchema(Schema):
    title: str = Field(min_length=1, max_length=250)
    description: str = ""
    is_included: bool = True
    value: str = Field(default="", max_length=200)
    icon: str = Field(default="", max_length=100)
    sort_order: int = Field(default=0, ge=0)


class PackageAddonInputSchema(Schema):
    name: str = Field(min_length=1, max_length=200)
    description: str = ""
    price: Decimal = Field(default=Decimal("0.00"), ge=0)
    currency: str = Field(
        default="LKR",
        min_length=3,
        max_length=3,
    )
    billing_cycle: str = "one_time"
    is_active: bool = True
    sort_order: int = Field(default=0, ge=0)


class PackageAudienceInputSchema(Schema):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    sort_order: int = Field(default=0, ge=0)


class PackageFaqInputSchema(Schema):
    question: str = Field(min_length=1, max_length=300)
    answer: str = Field(min_length=1)
    sort_order: int = Field(default=0, ge=0)


class PackageSeoInputSchema(Schema):
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


class PackageCreateSchema(Schema):
    name: str = Field(min_length=1, max_length=250)
    slug: str = Field(min_length=1, max_length=250)
    category: str = "other"
    service_id: UUID | None = None
    short_description: str = Field(
        default="",
        max_length=350,
    )
    description: dict[str, Any] = Field(
        default_factory=dict,
    )
    pricing_type: str = "fixed"
    price: Decimal = Field(default=Decimal("0.00"), ge=0)
    compare_at_price: Decimal | None = Field(
        default=None,
        ge=0,
    )
    currency: str = Field(
        default="LKR",
        min_length=3,
        max_length=3,
    )
    billing_cycle: str = "one_time"
    delivery_time: str = Field(
        default="",
        max_length=150,
    )
    revisions_included: int = Field(default=0, ge=0)
    support_period_days: int = Field(default=0, ge=0)
    status: str = "draft"
    is_featured: bool = False
    is_popular: bool = False
    is_active: bool = True
    sort_order: int = Field(default=0, ge=0)
    badge_text: str = Field(default="", max_length=100)
    cta_label: str = Field(default="", max_length=100)
    cta_url: str = Field(default="", max_length=500)

    features: list[PackageFeatureInputSchema] = Field(
        default_factory=list,
    )
    addons: list[PackageAddonInputSchema] = Field(
        default_factory=list,
    )
    target_audiences: list[
        PackageAudienceInputSchema
    ] = Field(default_factory=list)
    faqs: list[PackageFaqInputSchema] = Field(
        default_factory=list,
    )
    seo: PackageSeoInputSchema = Field(
        default_factory=PackageSeoInputSchema,
    )


class PackageUpdateSchema(PackageCreateSchema):
    change_summary: str = Field(
        default="",
        max_length=300,
    )


class PackageScheduleSchema(Schema):
    scheduled_for: datetime


class PackageFeatureSchema(PackageFeatureInputSchema):
    id: UUID


class PackageAddonSchema(PackageAddonInputSchema):
    id: UUID


class PackageAudienceSchema(PackageAudienceInputSchema):
    id: UUID


class PackageFaqSchema(PackageFaqInputSchema):
    id: UUID


class PackageSeoSchema(Schema):
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


class PackageRevisionSchema(Schema):
    id: UUID
    revision_number: int
    snapshot: dict[str, Any]
    change_summary: str
    created_at: datetime


class PackageSchema(Schema):
    id: UUID
    name: str
    slug: str
    category: str
    service_id: UUID | None
    service_title: str | None
    short_description: str
    description: dict[str, Any]
    pricing_type: str
    price: Decimal
    compare_at_price: Decimal | None
    currency: str
    billing_cycle: str
    delivery_time: str
    revisions_included: int
    support_period_days: int
    status: str
    published_at: datetime | None
    scheduled_for: datetime | None
    is_featured: bool
    is_popular: bool
    is_active: bool
    is_publicly_available: bool
    sort_order: int
    badge_text: str
    cta_label: str
    cta_url: str
    current_revision_number: int
    features: list[PackageFeatureSchema]
    addons: list[PackageAddonSchema]
    target_audiences: list[PackageAudienceSchema]
    faqs: list[PackageFaqSchema]
    seo: PackageSeoSchema | None
    revisions: list[PackageRevisionSchema]
    created_at: datetime
    updated_at: datetime
