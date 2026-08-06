from datetime import datetime
from typing import Literal
from uuid import UUID

from ninja import Schema


PublicSnapshotTypeValue = Literal[
    "bootstrap",
    "homepage",
    "catalog",
    "content",
]


class PublicWebsitePayloadSchema(Schema):
    environment: str
    generated_at: str
    data: dict


class PublicWebsiteHealthSchema(Schema):
    status: str
    service: str
    timestamp: datetime
    version: str


class PublicSnapshotGenerateSchema(Schema):
    snapshot_type: PublicSnapshotTypeValue
    environment: str = "production"
    ttl_minutes: int = 30


class PublicSnapshotSchema(Schema):
    id: UUID
    snapshot_type: str
    environment: str
    version: int
    payload: dict
    generated_at: datetime
    expires_at: datetime | None
    is_active: bool
    is_expired: bool
    checksum: str



class PublicSnapshotInvalidateSchema(Schema):
    snapshot_type: PublicSnapshotTypeValue | None = None
    environment: str | None = None


class PublicSnapshotRefreshAllSchema(Schema):
    environment: str = "production"
    ttl_minutes: int = 30


class PublicSnapshotInvalidationResultSchema(Schema):
    invalidated_count: int


class PublicSnapshotRefreshResultSchema(Schema):
    environment: str
    snapshot_count: int
    snapshots: list[PublicSnapshotSchema]
