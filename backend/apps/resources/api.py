from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.api.exceptions import ApiHttpError
from apps.rbac.services import require_permissions

from .repositories import ResourceRepository
from .schemas import (
    ResourceCreateSchema,
    ResourceScheduleSchema,
    ResourceUpdateSchema,
)
from .services import ResourceService


router = Router(
    tags=["Resources"],
    auth=jwt_auth,
)


def serialize_resource(
    request,
    resource,
):
    try:
        seo = resource.seo
    except Exception:
        seo = None

    file_url = None
    featured_image_url = None

    if resource.file:
        file_url = request.build_absolute_uri(
            resource.file.url
        )

    if resource.featured_image:
        featured_image_url = (
            request.build_absolute_uri(
                resource.featured_image.url
            )
        )

    return {
        "id": str(resource.id),
        "title": resource.title,
        "slug": resource.slug,
        "resource_type": resource.resource_type,
        "excerpt": resource.excerpt,
        "content": resource.content,
        "file_url": file_url,
        "external_url": resource.external_url,
        "resource_url": (
            file_url
            or resource.external_url
            or ""
        ),
        "featured_image_url": (
            featured_image_url
        ),
        "status": resource.status,
        "published_at": resource.published_at,
        "scheduled_for": resource.scheduled_for,
        "is_featured": resource.is_featured,
        "is_active": resource.is_active,
        "is_publicly_available": (
            resource.is_publicly_available
        ),
        "download_count": resource.download_count,
        "sort_order": resource.sort_order,
        "created_at": resource.created_at,
        "updated_at": resource.updated_at,
        "seo": (
            {
                "meta_title": seo.meta_title,
                "meta_description": (
                    seo.meta_description
                ),
                "canonical_url": seo.canonical_url,
                "robots_index": seo.robots_index,
                "robots_follow": seo.robots_follow,
                "open_graph_title": (
                    seo.open_graph_title
                ),
                "open_graph_description": (
                    seo.open_graph_description
                ),
                "structured_data": (
                    seo.structured_data
                ),
            }
            if seo
            else None
        ),
    }


def get_resource(resource_id):
    resource = ResourceRepository.find_by_id(
        resource_id
    )

    if resource is None:
        raise ApiHttpError(
            404,
            "Resource not found.",
            code="resource_not_found",
        )

    return resource


@router.get(
    "/public",
    auth=None,
    response={200: dict},
)
def public_resources(
    request,
    resource_type: str | None = None,
    featured_only: bool = False,
):
    items = [
        serialize_resource(
            request,
            resource,
        )
        for resource in (
            ResourceRepository.public_resources(
                resource_type=resource_type,
                featured_only=featured_only,
            )
        )
    ]

    return {
        "count": len(items),
        "resource_type": resource_type,
        "items": items,
    }


@router.get(
    "/public/{slug}",
    auth=None,
    response={
        200: dict,
        404: ErrorSchema,
    },
)
def public_resource_detail(
    request,
    slug: str,
):
    resource = (
        ResourceRepository
        .public_resources()
        .filter(slug=slug)
        .first()
    )

    if resource is None:
        raise ApiHttpError(
            404,
            "Resource not found.",
            code="resource_not_found",
        )

    return serialize_resource(
        request,
        resource,
    )


@router.get(
    "",
    response={200: dict},
)
@require_permissions(
    "resources.view_resource"
)
def list_resources(
    request,
    search: str | None = None,
    resource_type: str | None = None,
    status: str | None = None,
    is_featured: bool | None = None,
    is_active: bool | None = None,
    ordering: str | None = None,
):
    resources = ResourceRepository.search(
        search=search,
        resource_type=resource_type,
        status=status,
        is_featured=is_featured,
        is_active=is_active,
        ordering=ordering,
    )

    items = [
        serialize_resource(
            request,
            resource,
        )
        for resource in resources
    ]

    return {
        "count": len(items),
        "items": items,
    }


@router.post(
    "",
    response={
        201: dict,
        403: ErrorSchema,
    },
)
@require_permissions(
    "resources.add_resource"
)
def create_resource(
    request,
    payload: ResourceCreateSchema,
):
    resource = (
        ResourceService.create_resource(
            values=payload.dict(),
        )
    )

    return 201, serialize_resource(
        request,
        resource,
    )


@router.get(
    "/{resource_id}",
    response={
        200: dict,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "resources.view_resource"
)
def resource_detail(
    request,
    resource_id: str,
):
    return serialize_resource(
        request,
        get_resource(resource_id),
    )


@router.put(
    "/{resource_id}",
    response={
        200: dict,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "resources.change_resource"
)
def update_resource(
    request,
    resource_id: str,
    payload: ResourceUpdateSchema,
):
    resource = get_resource(resource_id)

    updated = ResourceService.update_resource(
        resource=resource,
        values=payload.dict(),
    )

    return serialize_resource(
        request,
        updated,
    )


@router.post(
    "/{resource_id}/publish",
    response={
        200: dict,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "resources.change_resource"
)
def publish_resource(
    request,
    resource_id: str,
):
    resource = (
        ResourceService.publish_resource(
            resource=get_resource(
                resource_id
            )
        )
    )

    return serialize_resource(
        request,
        resource,
    )


@router.post(
    "/{resource_id}/schedule",
    response={
        200: dict,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "resources.change_resource"
)
def schedule_resource(
    request,
    resource_id: str,
    payload: ResourceScheduleSchema,
):
    try:
        resource = (
            ResourceService.schedule_resource(
                resource=get_resource(
                    resource_id
                ),
                scheduled_for=(
                    payload.scheduled_for
                ),
            )
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_publish_schedule",
        ) from exc

    return serialize_resource(
        request,
        resource,
    )


@router.post(
    "/public/{slug}/download",
    auth=None,
    response={
        200: dict,
        404: ErrorSchema,
    },
)
def track_resource_download(
    request,
    slug: str,
):
    resource = (
        ResourceRepository
        .public_resources()
        .filter(slug=slug)
        .first()
    )

    if resource is None:
        raise ApiHttpError(
            404,
            "Resource not found.",
            code="resource_not_found",
        )

    ResourceService.increment_download(
        resource
    )

    return {
        "status": "ok",
        "download_count": (
            resource.download_count
        ),
        "resource_url": (
            request.build_absolute_uri(
                resource.file.url
            )
            if resource.file
            else resource.external_url
        ),
    }
