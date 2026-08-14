from datetime import datetime

from ninja import Schema


class ResourceCreateSchema(Schema):
    title: str
    slug: str
    resource_type: str

    excerpt: str = ""
    content: dict = {}

    external_url: str = ""

    status: str = "draft"

    published_at: datetime | None = None
    scheduled_for: datetime | None = None

    is_featured: bool = False
    is_active: bool = True

    sort_order: int = 0


class ResourceUpdateSchema(Schema):
    title: str | None = None
    slug: str | None = None
    resource_type: str | None = None

    excerpt: str | None = None
    content: dict | None = None

    external_url: str | None = None

    status: str | None = None

    published_at: datetime | None = None
    scheduled_for: datetime | None = None

    is_featured: bool | None = None
    is_active: bool | None = None

    sort_order: int | None = None


class ResourceScheduleSchema(Schema):
    scheduled_for: datetime
