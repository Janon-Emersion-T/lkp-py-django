from django.utils import timezone
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.api.exceptions import ApiHttpError
from apps.rbac.services import require_permissions

from .models import PublicWebsiteSnapshot
from .repositories import (
    PublicSnapshotRepository,
    normalize_environment,
)
from .schemas import (
    PublicSnapshotGenerateSchema,
    PublicSnapshotInvalidateSchema,
    PublicSnapshotInvalidationResultSchema,
    PublicSnapshotRefreshAllSchema,
    PublicSnapshotRefreshResultSchema,
    PublicSnapshotSchema,
    PublicWebsiteHealthSchema,
)
from .services import (
    PublicSnapshotService,
    PublicWebsiteService,
)


router = Router(
    tags=["Public Website API"],
    auth=jwt_auth,
)


def validate_environment(environment):
    try:
        return normalize_environment(environment)
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_public_environment",
        ) from exc


def serialize_snapshot(snapshot):
    return {
        "id": snapshot.id,
        "snapshot_type": snapshot.snapshot_type,
        "environment": snapshot.environment,
        "version": snapshot.version,
        "payload": snapshot.payload,
        "generated_at": snapshot.generated_at,
        "expires_at": snapshot.expires_at,
        "is_active": snapshot.is_active,
        "is_expired": snapshot.is_expired,
        "checksum": snapshot.checksum,
    }


def snapshot_or_live(
    snapshot_type,
    environment,
    builder,
):
    snapshot = PublicSnapshotRepository.latest(
        snapshot_type,
        environment,
    )

    if snapshot is not None:
        return {
            **snapshot.payload,
            "snapshot": {
                "id": str(snapshot.id),
                "version": snapshot.version,
                "generated_at": (
                    snapshot.generated_at.isoformat()
                ),
                "expires_at": (
                    snapshot.expires_at.isoformat()
                    if snapshot.expires_at
                    else None
                ),
                "checksum": snapshot.checksum,
            },
        }

    return builder(environment)


@router.get(
    "/health",
    auth=None,
    response={
        200: PublicWebsiteHealthSchema,
    },
)
def public_website_health(request):
    return {
        "status": "ok",
        "service": "public-website-api",
        "timestamp": timezone.now(),
        "version": "1.0",
    }


@router.get(
    "/bootstrap",
    auth=None,
    response={
        200: dict,
        400: ErrorSchema,
    },
)
def public_bootstrap(
    request,
    environment: str = "production",
):
    environment = validate_environment(
        environment
    )

    return snapshot_or_live(
        "bootstrap",
        environment,
        PublicWebsiteService.build_bootstrap,
    )


@router.get(
    "/homepage",
    auth=None,
    response={
        200: dict,
        400: ErrorSchema,
    },
)
def public_homepage(
    request,
    environment: str = "production",
):
    environment = validate_environment(
        environment
    )

    return snapshot_or_live(
        "homepage",
        environment,
        PublicWebsiteService.build_homepage,
    )


@router.get(
    "/catalog",
    auth=None,
    response={
        200: dict,
        400: ErrorSchema,
    },
)
def public_catalog(
    request,
    environment: str = "production",
):
    environment = validate_environment(
        environment
    )

    return snapshot_or_live(
        "catalog",
        environment,
        PublicWebsiteService.build_catalog,
    )


@router.get(
    "/content",
    auth=None,
    response={
        200: dict,
        400: ErrorSchema,
    },
)
def public_content(
    request,
    environment: str = "production",
):
    environment = validate_environment(
        environment
    )

    return snapshot_or_live(
        "content",
        environment,
        PublicWebsiteService.build_content,
    )


@router.get(
    "/snapshots",
    response={
        200: list[PublicSnapshotSchema],
        403: ErrorSchema,
    },
)
@require_permissions(
    "public_website.view_publicwebsitesnapshot"
)
def list_snapshots(
    request,
    snapshot_type: str | None = None,
    environment: str | None = None,
    is_active: bool | None = None,
):
    queryset = PublicWebsiteSnapshot.objects.all()

    if snapshot_type:
        queryset = queryset.filter(
            snapshot_type=snapshot_type,
        )

    if environment:
        queryset = queryset.filter(
            environment=environment,
        )

    if is_active is not None:
        queryset = queryset.filter(
            is_active=is_active,
        )

    return [
        serialize_snapshot(snapshot)
        for snapshot in queryset
    ]


@router.post(
    "/snapshots/generate",
    response={
        201: PublicSnapshotSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "public_website.add_publicwebsitesnapshot"
)
def generate_snapshot(
    request,
    payload: PublicSnapshotGenerateSchema,
):
    environment = validate_environment(
        payload.environment
    )

    if payload.ttl_minutes < 1:
        raise ApiHttpError(
            400,
            "Snapshot TTL must be at least one minute.",
            code="invalid_snapshot_ttl",
        )

    try:
        snapshot = PublicSnapshotService.generate(
            request=request,
            snapshot_type=(
                payload.snapshot_type
            ),
            environment=environment,
            ttl_minutes=payload.ttl_minutes,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_snapshot_type",
        ) from exc

    return 201, serialize_snapshot(snapshot)



@router.post(
    "/snapshots/invalidate",
    response={
        200: PublicSnapshotInvalidationResultSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "public_website.change_publicwebsitesnapshot"
)
def invalidate_snapshots(
    request,
    payload: PublicSnapshotInvalidateSchema,
):
    environment = payload.environment

    if environment is not None:
        environment = validate_environment(
            environment
        )

    invalidated_count = (
        PublicSnapshotService.invalidate(
            request=request,
            snapshot_type=payload.snapshot_type,
            environment=environment,
        )
    )

    return {
        "invalidated_count": invalidated_count,
    }


@router.post(
    "/snapshots/refresh-all",
    response={
        201: PublicSnapshotRefreshResultSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "public_website.add_publicwebsitesnapshot"
)
def refresh_all_snapshots(
    request,
    payload: PublicSnapshotRefreshAllSchema,
):
    environment = validate_environment(
        payload.environment
    )

    if payload.ttl_minutes < 1:
        raise ApiHttpError(
            400,
            "Snapshot TTL must be at least one minute.",
            code="invalid_snapshot_ttl",
        )

    snapshots = PublicSnapshotService.refresh_all(
        request=request,
        environment=environment,
        ttl_minutes=payload.ttl_minutes,
    )

    return 201, {
        "environment": environment,
        "snapshot_count": len(snapshots),
        "snapshots": [
            serialize_snapshot(snapshot)
            for snapshot in snapshots
        ],
    }
