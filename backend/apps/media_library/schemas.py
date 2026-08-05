from datetime import datetime
from uuid import UUID

from ninja import Schema
from pydantic import Field


class MediaFolderCreateSchema(Schema):
    name: str = Field(min_length=1, max_length=200)
    parent_id: UUID | None = None
    description: str = ""


class MediaFolderSchema(Schema):
    id: UUID
    name: str
    slug: str
    parent_id: UUID | None
    description: str
    created_at: datetime
    updated_at: datetime


class MediaAssetUpdateSchema(Schema):
    folder_id: UUID | None = None
    title: str = Field(min_length=1, max_length=250)
    media_type: str
    alt_text: str = Field(default="", max_length=250)
    caption: str = ""
    description: str = ""
    tags: list[str] = Field(default_factory=list)
    is_public: bool = True


class MediaUsageCreateSchema(Schema):
    application: str = Field(min_length=1, max_length=100)
    model_name: str = Field(min_length=1, max_length=100)
    object_id: str = Field(min_length=1, max_length=100)
    field_name: str = Field(default="", max_length=100)
    usage_context: str = Field(
        default="",
        max_length=200,
    )


class MediaUsageSchema(Schema):
    id: UUID
    application: str
    model_name: str
    object_id: str
    field_name: str
    usage_context: str
    created_at: datetime


class MediaAssetSchema(Schema):
    id: UUID
    folder_id: UUID | None
    folder_name: str | None
    title: str
    file_url: str
    original_name: str
    media_type: str
    mime_type: str
    extension: str
    size: int
    width: int | None
    height: int | None
    duration_seconds: int | None
    alt_text: str
    caption: str
    description: str
    tags: list[str]
    checksum: str
    is_optimized: bool
    optimized_file_url: str | None
    webp_file_url: str | None
    is_public: bool
    usages: list[MediaUsageSchema]
    created_at: datetime
    updated_at: datetime
