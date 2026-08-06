from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from .models import DashboardReportSnapshot


ALLOWED_ENVIRONMENTS = {
    "development",
    "staging",
    "production",
    "test",
}


def normalize_environment(environment):
    normalized = (environment or "production").strip().lower()

    if normalized not in ALLOWED_ENVIRONMENTS:
        allowed = ", ".join(sorted(ALLOWED_ENVIRONMENTS))
        raise ValueError(
            f"Invalid dashboard reporting environment. "
            f"Allowed values: {allowed}."
        )

    return normalized


class DashboardSnapshotRepository:
    @staticmethod
    def queryset():
        return DashboardReportSnapshot.objects.all()

    @classmethod
    def latest(
        cls,
        *,
        report_type,
        period_preset,
        date_from,
        date_to,
        environment,
        include_expired=False,
    ):
        queryset = cls.queryset().filter(
            report_type=report_type,
            period_preset=period_preset,
            date_from=date_from,
            date_to=date_to,
            environment=environment,
            is_active=True,
        )

        if not include_expired:
            now = timezone.now()
            queryset = queryset.filter(
                models_expiry_filter(now),
            )

        return queryset.order_by(
            "-version",
            "-generated_at",
        ).first()

    @classmethod
    def list_snapshots(
        cls,
        *,
        report_type=None,
        environment=None,
        active_only=False,
    ):
        queryset = cls.queryset()

        if report_type:
            queryset = queryset.filter(
                report_type=report_type,
            )

        if environment:
            queryset = queryset.filter(
                environment=environment,
            )

        if active_only:
            queryset = queryset.filter(is_active=True)

        return queryset.order_by(
            "report_type",
            "-version",
            "-generated_at",
        )

    @classmethod
    def next_version(
        cls,
        *,
        report_type,
        period_preset,
        date_from,
        date_to,
        environment,
    ):
        current = (
            cls.queryset()
            .filter(
                report_type=report_type,
                period_preset=period_preset,
                date_from=date_from,
                date_to=date_to,
                environment=environment,
            )
            .aggregate(maximum=Max("version"))
            .get("maximum")
        )

        return (current or 0) + 1

    @classmethod
    @transaction.atomic
    def create_snapshot(
        cls,
        *,
        report_type,
        period_preset,
        date_from,
        date_to,
        environment,
        payload,
        checksum,
        generated_at,
        expires_at,
        metadata=None,
        actor=None,
    ):
        cls.queryset().select_for_update().filter(
            report_type=report_type,
            period_preset=period_preset,
            date_from=date_from,
            date_to=date_to,
            environment=environment,
            is_active=True,
        ).update(
            is_active=False,
            updated_by=actor,
        )

        version = cls.next_version(
            report_type=report_type,
            period_preset=period_preset,
            date_from=date_from,
            date_to=date_to,
            environment=environment,
        )

        return cls.queryset().create(
            report_type=report_type,
            period_preset=period_preset,
            date_from=date_from,
            date_to=date_to,
            environment=environment,
            version=version,
            payload=payload,
            checksum=checksum,
            generated_at=generated_at,
            expires_at=expires_at,
            is_active=True,
            metadata=metadata or {},
            created_by=actor,
            updated_by=actor,
        )

    @classmethod
    def invalidate(
        cls,
        *,
        report_type=None,
        environment=None,
        actor=None,
    ):
        queryset = cls.queryset().filter(is_active=True)

        if report_type:
            queryset = queryset.filter(
                report_type=report_type,
            )

        if environment:
            queryset = queryset.filter(
                environment=environment,
            )

        return queryset.update(
            is_active=False,
            updated_by=actor,
        )


def models_expiry_filter(now):
    from django.db.models import Q

    return (
        Q(expires_at__isnull=True)
        | Q(expires_at__gt=now)
    )
