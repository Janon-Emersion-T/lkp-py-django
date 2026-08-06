from datetime import date, datetime
from typing import Any
from uuid import UUID

from ninja import Schema

from .models import (
    DashboardPeriodPreset,
    DashboardReportType,
)


class DashboardPeriodQuerySchema(Schema):
    preset: DashboardPeriodPreset = (
        DashboardPeriodPreset.THIS_MONTH
    )
    date_from: date | None = None
    date_to: date | None = None


class DashboardPeriodSchema(Schema):
    preset: str
    date_from: date
    date_to: date
    datetime_from: datetime
    datetime_to: datetime


class DashboardFoundationReportSchema(Schema):
    report_type: str
    environment: str
    period: dict[str, Any]
    generated_at: datetime
    timezone: str
    schema_version: int
    data: dict[str, Any]
    metadata: dict[str, Any]


class DashboardSnapshotGenerateSchema(Schema):
    report_type: DashboardReportType
    period_preset: DashboardPeriodPreset = (
        DashboardPeriodPreset.THIS_MONTH
    )
    date_from: date | None = None
    date_to: date | None = None
    environment: str = "production"
    expiry_minutes: int = 30


class DashboardSnapshotRefreshAllSchema(Schema):
    period_preset: DashboardPeriodPreset = (
        DashboardPeriodPreset.THIS_MONTH
    )
    date_from: date | None = None
    date_to: date | None = None
    environment: str = "production"
    expiry_minutes: int = 30


class DashboardSnapshotInvalidateSchema(Schema):
    report_type: DashboardReportType | None = None
    environment: str = "production"


class DashboardSnapshotSchema(Schema):
    id: UUID
    report_type: str
    period_preset: str
    date_from: date | None
    date_to: date | None
    environment: str
    version: int
    payload: dict[str, Any]
    checksum: str
    generated_at: datetime
    expires_at: datetime | None
    is_active: bool
    is_expired: bool


class DashboardSnapshotListSchema(Schema):
    items: list[DashboardSnapshotSchema]
    count: int


class DashboardSnapshotRefreshResultSchema(Schema):
    items: list[DashboardSnapshotSchema]
    count: int


class DashboardSnapshotInvalidationResultSchema(Schema):
    invalidated_count: int
    report_type: str | None
    environment: str


class DashboardReportingHealthSchema(Schema):
    status: str
    service: str
    timestamp: datetime
    snapshot_model: str
    supported_report_types: list[str]
    supported_period_presets: list[str]
