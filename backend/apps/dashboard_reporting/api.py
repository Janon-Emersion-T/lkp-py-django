from datetime import date

from django.utils import timezone
from ninja import Query, Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.api.exceptions import ApiHttpError
from apps.rbac.services import require_permissions

from .models import (
    DashboardPeriodPreset,
    DashboardReportType,
)
from .repositories import (
    DashboardSnapshotRepository,
    normalize_environment,
)
from .schemas import (
    DashboardFoundationReportSchema,
    DashboardPeriodSchema,
    DashboardReportingHealthSchema,
    DashboardSnapshotGenerateSchema,
    DashboardSnapshotInvalidationResultSchema,
    DashboardSnapshotInvalidateSchema,
    DashboardSnapshotListSchema,
    DashboardSnapshotRefreshAllSchema,
    DashboardSnapshotRefreshResultSchema,
    DashboardSnapshotSchema,
)
from .services import (
    DashboardPeriodService,
    DashboardReportFoundationService,
    DashboardSnapshotService,
)


router = Router(
    tags=["Dashboard Reporting"],
    auth=jwt_auth,
)


def require_dashboard_view(request):
    require_permissions(
        request.auth,
        ["dashboard_reporting.view"],
    )


def require_dashboard_manage(request):
    require_permissions(
        request.auth,
        ["dashboard_reporting.manage"],
    )


def api_error(exc, code):
    raise ApiHttpError(
        400,
        str(exc),
        code=code,
    ) from exc


@router.get(
    "/health",
    response={
        200: DashboardReportingHealthSchema,
        401: ErrorSchema,
        403: ErrorSchema,
    },
)
def dashboard_reporting_health(request):
    require_dashboard_view(request)

    return {
        "status": "ok",
        "service": "dashboard_reporting",
        "timestamp": timezone.now(),
        "snapshot_model": (
            "dashboard_reporting."
            "DashboardReportSnapshot"
        ),
        "supported_report_types": [
            value
            for value, _label
            in DashboardReportType.choices
        ],
        "supported_period_presets": [
            value
            for value, _label
            in DashboardPeriodPreset.choices
        ],
    }


@router.get(
    "/period",
    response={
        200: DashboardPeriodSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        403: ErrorSchema,
    },
)
def resolve_dashboard_period(
    request,
    preset: DashboardPeriodPreset = (
        DashboardPeriodPreset.THIS_MONTH
    ),
    date_from: date | None = None,
    date_to: date | None = None,
):
    require_dashboard_view(request)

    try:
        period = DashboardPeriodService.resolve(
            preset=preset,
            date_from=date_from,
            date_to=date_to,
        )
    except ValueError as exc:
        api_error(
            exc,
            "invalid_dashboard_period",
        )

    return period.as_dict()


@router.get(
    "/foundation/{report_type}",
    response={
        200: DashboardFoundationReportSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        403: ErrorSchema,
    },
)
def dashboard_foundation_report(
    request,
    report_type: DashboardReportType,
    preset: DashboardPeriodPreset = (
        DashboardPeriodPreset.THIS_MONTH
    ),
    date_from: date | None = None,
    date_to: date | None = None,
    environment: str = "production",
):
    require_dashboard_view(request)

    try:
        period = DashboardPeriodService.resolve(
            preset=preset,
            date_from=date_from,
            date_to=date_to,
        )

        return (
            DashboardReportFoundationService
            .build_report_context(
                report_type=report_type,
                period=period,
                environment=environment,
            )
        )
    except ValueError as exc:
        api_error(
            exc,
            "invalid_dashboard_report_request",
        )


@router.get(
    "/snapshots",
    response={
        200: DashboardSnapshotListSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        403: ErrorSchema,
    },
)
def list_dashboard_snapshots(
    request,
    report_type: DashboardReportType | None = None,
    environment: str | None = None,
    active_only: bool = False,
):
    require_dashboard_view(request)

    try:
        normalized_environment = (
            normalize_environment(environment)
            if environment
            else None
        )
    except ValueError as exc:
        api_error(
            exc,
            "invalid_dashboard_environment",
        )

    snapshots = list(
        DashboardSnapshotRepository.list_snapshots(
            report_type=report_type,
            environment=normalized_environment,
            active_only=active_only,
        )[:200]
    )

    return {
        "items": [
            DashboardSnapshotService.serialize(snapshot)
            for snapshot in snapshots
        ],
        "count": len(snapshots),
    }


@router.post(
    "/snapshots/generate",
    response={
        201: DashboardSnapshotSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        403: ErrorSchema,
    },
)
def generate_dashboard_snapshot(
    request,
    payload: DashboardSnapshotGenerateSchema,
):
    require_dashboard_manage(request)

    try:
        snapshot = DashboardSnapshotService.generate(
            report_type=payload.report_type,
            period_preset=payload.period_preset,
            date_from=payload.date_from,
            date_to=payload.date_to,
            environment=payload.environment,
            expiry_minutes=payload.expiry_minutes,
            actor=request.auth,
        )
    except ValueError as exc:
        api_error(
            exc,
            "invalid_dashboard_snapshot_request",
        )

    return 201, DashboardSnapshotService.serialize(
        snapshot
    )


@router.post(
    "/snapshots/refresh-all",
    response={
        200: DashboardSnapshotRefreshResultSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        403: ErrorSchema,
    },
)
def refresh_all_dashboard_snapshots(
    request,
    payload: DashboardSnapshotRefreshAllSchema,
):
    require_dashboard_manage(request)

    try:
        snapshots = DashboardSnapshotService.refresh_all(
            period_preset=payload.period_preset,
            date_from=payload.date_from,
            date_to=payload.date_to,
            environment=payload.environment,
            expiry_minutes=payload.expiry_minutes,
            actor=request.auth,
        )
    except ValueError as exc:
        api_error(
            exc,
            "invalid_dashboard_snapshot_request",
        )

    return {
        "items": [
            DashboardSnapshotService.serialize(snapshot)
            for snapshot in snapshots
        ],
        "count": len(snapshots),
    }


@router.post(
    "/snapshots/invalidate",
    response={
        200: DashboardSnapshotInvalidationResultSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        403: ErrorSchema,
    },
)
def invalidate_dashboard_snapshots(
    request,
    payload: DashboardSnapshotInvalidateSchema,
):
    require_dashboard_manage(request)

    try:
        environment = normalize_environment(
            payload.environment
        )
    except ValueError as exc:
        api_error(
            exc,
            "invalid_dashboard_environment",
        )

    invalidated_count = (
        DashboardSnapshotRepository.invalidate(
            report_type=payload.report_type,
            environment=environment,
            actor=request.auth,
        )
    )

    return {
        "invalidated_count": invalidated_count,
        "report_type": payload.report_type,
        "environment": environment,
    }
