import hashlib
import json
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from decimal import Decimal

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

from .models import (
    DashboardPeriodPreset,
    DashboardReportType,
)
from .repositories import (
    CrmReportingRepository,
    DashboardSnapshotRepository,
    ExecutiveDashboardRepository,
    ProjectReportingRepository,
    SalesReportingRepository,
    normalize_environment,
)


@dataclass(frozen=True)
class DashboardDateRange:
    preset: str
    date_from: date
    date_to: date
    datetime_from: datetime
    datetime_to: datetime

    def as_dict(self):
        return {
            "preset": self.preset,
            "date_from": self.date_from.isoformat(),
            "date_to": self.date_to.isoformat(),
            "datetime_from": self.datetime_from.isoformat(),
            "datetime_to": self.datetime_to.isoformat(),
        }


class DashboardPeriodService:
    @staticmethod
    def resolve(
        *,
        preset=DashboardPeriodPreset.THIS_MONTH,
        date_from=None,
        date_to=None,
        reference_date=None,
    ):
        reference_date = (
            reference_date
            or timezone.localdate()
        )

        valid_presets = {
            value
            for value, _label
            in DashboardPeriodPreset.choices
        }

        if preset not in valid_presets:
            raise ValueError(
                "Invalid dashboard period preset."
            )

        if preset == DashboardPeriodPreset.CUSTOM:
            if date_from is None or date_to is None:
                raise ValueError(
                    "date_from and date_to are required "
                    "for the custom period."
                )
            resolved_from = date_from
            resolved_to = date_to

        elif date_from is not None or date_to is not None:
            raise ValueError(
                "date_from and date_to may only be supplied "
                "with the custom period."
            )

        elif preset == DashboardPeriodPreset.TODAY:
            resolved_from = reference_date
            resolved_to = reference_date

        elif preset == DashboardPeriodPreset.THIS_WEEK:
            resolved_from = (
                reference_date
                - timedelta(days=reference_date.weekday())
            )
            resolved_to = reference_date

        elif preset == DashboardPeriodPreset.THIS_MONTH:
            resolved_from = reference_date.replace(day=1)
            resolved_to = reference_date

        elif preset == DashboardPeriodPreset.THIS_QUARTER:
            quarter_start_month = (
                ((reference_date.month - 1) // 3) * 3
                + 1
            )
            resolved_from = reference_date.replace(
                month=quarter_start_month,
                day=1,
            )
            resolved_to = reference_date

        elif preset == DashboardPeriodPreset.THIS_YEAR:
            resolved_from = reference_date.replace(
                month=1,
                day=1,
            )
            resolved_to = reference_date

        elif preset == DashboardPeriodPreset.LAST_7_DAYS:
            resolved_from = (
                reference_date - timedelta(days=6)
            )
            resolved_to = reference_date

        elif preset == DashboardPeriodPreset.LAST_30_DAYS:
            resolved_from = (
                reference_date - timedelta(days=29)
            )
            resolved_to = reference_date

        elif preset == DashboardPeriodPreset.LAST_90_DAYS:
            resolved_from = (
                reference_date - timedelta(days=89)
            )
            resolved_to = reference_date

        else:
            raise ValueError(
                "Unsupported dashboard period preset."
            )

        if resolved_to < resolved_from:
            raise ValueError(
                "date_to cannot be before date_from."
            )

        current_timezone = timezone.get_current_timezone()

        datetime_from = timezone.make_aware(
            datetime.combine(
                resolved_from,
                time.min,
            ),
            current_timezone,
        )

        datetime_to = timezone.make_aware(
            datetime.combine(
                resolved_to + timedelta(days=1),
                time.min,
            ),
            current_timezone,
        )

        return DashboardDateRange(
            preset=preset,
            date_from=resolved_from,
            date_to=resolved_to,
            datetime_from=datetime_from,
            datetime_to=datetime_to,
        )


class DashboardReportFoundationService:
    @staticmethod
    def build_report_context(
        *,
        report_type,
        period,
        environment,
    ):
        valid_report_types = {
            value
            for value, _label
            in DashboardReportType.choices
        }

        if report_type not in valid_report_types:
            raise ValueError(
                "Invalid dashboard report type."
            )

        normalized_environment = normalize_environment(
            environment
        )

        generated_at = timezone.now()

        if report_type == DashboardReportType.EXECUTIVE:
            data = ExecutiveDashboardRepository.build(
                period,
                generated_at,
            )
            aggregation_status = "complete"
            foundation = False
        elif report_type == DashboardReportType.CRM:
            data = CrmReportingRepository.build(
                period,
                generated_at,
            )
            aggregation_status = "complete"
            foundation = False
        elif report_type == DashboardReportType.SALES:
            data = SalesReportingRepository.build(
                period,
                generated_at,
            )
            aggregation_status = "complete"
            foundation = False
        elif report_type == DashboardReportType.PROJECTS:
            data = ProjectReportingRepository.build(
                period,
                generated_at,
            )
            aggregation_status = "complete"
            foundation = False
        else:
            data = {}
            aggregation_status = "foundation_ready"
            foundation = True

        return {
            "report_type": report_type,
            "environment": normalized_environment,
            "period": period.as_dict(),
            "generated_at": generated_at.isoformat(),
            "timezone": str(
                timezone.get_current_timezone()
            ),
            "schema_version": 1,
            "data": data,
            "metadata": {
                "foundation": foundation,
                "aggregation_status": aggregation_status,
            },
        }


class DashboardSnapshotService:
    DEFAULT_EXPIRY_MINUTES = 30

    @staticmethod
    def canonical_payload(payload):
        return json.dumps(
            payload,
            cls=DjangoJSONEncoder,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )

    @classmethod
    def checksum(cls, payload):
        canonical = cls.canonical_payload(payload)

        return hashlib.sha256(
            canonical.encode("utf-8")
        ).hexdigest()

    @classmethod
    def generate(
        cls,
        *,
        report_type,
        period_preset,
        date_from=None,
        date_to=None,
        environment=None,
        expiry_minutes=None,
        actor=None,
    ):
        period = DashboardPeriodService.resolve(
            preset=period_preset,
            date_from=date_from,
            date_to=date_to,
        )

        normalized_environment = normalize_environment(
            environment
            or getattr(
                settings,
                "DASHBOARD_REPORTING_ENVIRONMENT",
                "production",
            )
        )

        payload = (
            DashboardReportFoundationService
            .build_report_context(
                report_type=report_type,
                period=period,
                environment=normalized_environment,
            )
        )

        generated_at = timezone.now()

        if expiry_minutes is None:
            expiry_minutes = getattr(
                settings,
                "DASHBOARD_REPORTING_SNAPSHOT_EXPIRY_MINUTES",
                cls.DEFAULT_EXPIRY_MINUTES,
            )

        if expiry_minutes < 1:
            raise ValueError(
                "expiry_minutes must be at least 1."
            )

        expires_at = (
            generated_at
            + timedelta(minutes=expiry_minutes)
        )

        checksum = cls.checksum(payload)

        return DashboardSnapshotRepository.create_snapshot(
            report_type=report_type,
            period_preset=period.preset,
            date_from=period.date_from,
            date_to=period.date_to,
            environment=normalized_environment,
            payload=payload,
            checksum=checksum,
            generated_at=generated_at,
            expires_at=expires_at,
            metadata={
                "schema_version": 1,
                "expiry_minutes": expiry_minutes,
            },
            actor=actor,
        )

    @classmethod
    def refresh_all(
        cls,
        *,
        period_preset,
        date_from=None,
        date_to=None,
        environment=None,
        expiry_minutes=None,
        actor=None,
    ):
        snapshots = []

        for report_type, _label in (
            DashboardReportType.choices
        ):
            snapshots.append(
                cls.generate(
                    report_type=report_type,
                    period_preset=period_preset,
                    date_from=date_from,
                    date_to=date_to,
                    environment=environment,
                    expiry_minutes=expiry_minutes,
                    actor=actor,
                )
            )

        return snapshots

    @staticmethod
    def serialize(snapshot):
        return {
            "id": snapshot.id,
            "report_type": snapshot.report_type,
            "period_preset": snapshot.period_preset,
            "date_from": snapshot.date_from,
            "date_to": snapshot.date_to,
            "environment": snapshot.environment,
            "version": snapshot.version,
            "payload": snapshot.payload,
            "checksum": snapshot.checksum,
            "generated_at": snapshot.generated_at,
            "expires_at": snapshot.expires_at,
            "is_active": snapshot.is_active,
            "is_expired": snapshot.is_expired,
        }


def json_safe_decimal(value):
    if isinstance(value, Decimal):
        return str(value)

    return value
