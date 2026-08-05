from django.utils.text import slugify
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema, MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.api.pagination_schemas import PaginatedResponseSchema
from apps.api.responses import paginated_response
from apps.common.pagination import paginate_queryset
from apps.media_library.models import MediaAsset
from apps.rbac.services import require_permissions

from .models import Service
from .repositories import ServiceRepository
from .schemas import (
    ServiceCreateSchema,
    ServiceScheduleSchema,
    ServiceSchema,
    ServiceUpdateSchema,
)
from .services import ServiceCatalogService


router = Router(
    tags=["Services Catalog"],
    auth=jwt_auth,
)


def resolve_media(asset_id):
    if asset_id is None:
        return None

    asset = MediaAsset.objects.filter(pk=asset_id).first()

    if asset is None:
        raise ApiHttpError(
            400,
            "Media asset not found.",
            code="invalid_media_asset",
        )

    return asset


def serialize_service(service):
    try:
        seo = service.seo
    except service._meta.get_field(
        "seo"
    ).related_model.DoesNotExist:
        seo = None

    return {
        "id": service.id,
        "title": service.title,
        "slug": service.slug,
        "short_description": service.short_description,
        "description": service.description,
        "hero_title": service.hero_title,
        "hero_description": service.hero_description,
        "hero_image_id": service.hero_image_id,
        "status": service.status,
        "published_at": service.published_at,
        "scheduled_for": service.scheduled_for,
        "icon": service.icon,
        "sort_order": service.sort_order,
        "is_featured": service.is_featured,
        "is_active": service.is_active,
        "is_publicly_available": (
            service.is_publicly_available
        ),
        "cta_title": service.cta_title,
        "cta_text": service.cta_text,
        "cta_label": service.cta_label,
        "cta_url": service.cta_url,
        "current_revision_number": (
            service.current_revision_number
        ),
        "features": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "icon": item.icon,
                "sort_order": item.sort_order,
            }
            for item in service.features.all()
        ],
        "process_steps": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "step_number": item.step_number,
                "sort_order": item.sort_order,
            }
            for item in service.process_steps.all()
        ],
        "technologies": [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "logo_id": item.logo_id,
                "sort_order": item.sort_order,
            }
            for item in service.technologies.all()
        ],
        "faqs": [
            {
                "id": item.id,
                "question": item.question,
                "answer": item.answer,
                "sort_order": item.sort_order,
            }
            for item in service.faqs.all()
        ],
        "seo": (
            {
                "id": seo.id,
                "meta_title": seo.meta_title,
                "meta_description": seo.meta_description,
                "canonical_url": seo.canonical_url,
                "robots_index": seo.robots_index,
                "robots_follow": seo.robots_follow,
                "open_graph_title": seo.open_graph_title,
                "open_graph_description": (
                    seo.open_graph_description
                ),
                "open_graph_image_id": (
                    seo.open_graph_image_id
                ),
                "twitter_title": seo.twitter_title,
                "twitter_description": (
                    seo.twitter_description
                ),
                "structured_data": seo.structured_data,
            }
            if seo
            else None
        ),
        "revisions": [
            {
                "id": revision.id,
                "revision_number": revision.revision_number,
                "snapshot": revision.snapshot,
                "change_summary": revision.change_summary,
                "created_at": revision.created_at,
            }
            for revision in service.revisions.all()
        ],
        "created_at": service.created_at,
        "updated_at": service.updated_at,
    }


def get_service(service_id):
    service = ServiceRepository.find_by_id(service_id)

    if service is None:
        raise ApiHttpError(
            404,
            "Service not found.",
            code="service_not_found",
        )

    return service


def refresh_service(service):
    refreshed = ServiceRepository.queryset().filter(
        pk=service.pk,
    ).first()

    if refreshed is None:
        raise ApiHttpError(
            404,
            "Service not found.",
            code="service_not_found",
        )

    return refreshed


def payload_parts(payload):
    raw = payload.dict()

    features = [
        item.dict()
        for item in payload.features
    ]

    process_steps = [
        item.dict()
        for item in payload.process_steps
    ]

    technologies = []

    for item in payload.technologies:
        values = item.dict()
        logo_id = values.pop("logo_id")
        values["logo"] = resolve_media(logo_id)
        technologies.append(values)

    faqs = [
        item.dict()
        for item in payload.faqs
    ]

    seo = payload.seo.dict()
    open_graph_image_id = seo.pop(
        "open_graph_image_id"
    )
    seo["open_graph_image"] = resolve_media(
        open_graph_image_id
    )

    values = {
        key: value
        for key, value in raw.items()
        if key not in (
            "features",
            "process_steps",
            "technologies",
            "faqs",
            "seo",
            "change_summary",
            "hero_image_id",
        )
    }

    values["slug"] = slugify(payload.slug)
    values["hero_image"] = resolve_media(
        payload.hero_image_id
    )

    return (
        values,
        features,
        process_steps,
        technologies,
        faqs,
        seo,
    )


@router.get(
    "",
    response={
        200: PaginatedResponseSchema[ServiceSchema],
        403: ErrorSchema,
    },
)
@require_permissions("services_catalog.view_service")
def list_services(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    status: str | None = None,
    is_featured: bool | None = None,
    is_active: bool | None = None,
    ordering: str | None = None,
):
    result = paginate_queryset(
        ServiceRepository.search(
            search=search,
            status=status,
            is_featured=is_featured,
            is_active=is_active,
            ordering=ordering,
        ),
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_service,
    )


@router.post(
    "",
    response={
        201: ServiceSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("services_catalog.add_service")
def create_service(
    request,
    payload: ServiceCreateSchema,
):
    if Service.all_objects.filter(
        slug=slugify(payload.slug),
    ).exists():
        raise ApiHttpError(
            400,
            "Service slug already exists.",
            code="duplicate_service_slug",
        )

    (
        values,
        features,
        process_steps,
        technologies,
        faqs,
        seo,
    ) = payload_parts(payload)

    service = ServiceCatalogService.create_service(
        request=request,
        values=values,
        features=features,
        process_steps=process_steps,
        technologies=technologies,
        faqs=faqs,
        seo_values=seo,
    )

    return 201, serialize_service(
        refresh_service(service)
    )


@router.get(
    "/{service_id}",
    response={
        200: ServiceSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("services_catalog.view_service")
def service_detail(request, service_id: str):
    return serialize_service(
        get_service(service_id)
    )


@router.put(
    "/{service_id}",
    response={
        200: ServiceSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("services_catalog.change_service")
def update_service(
    request,
    service_id: str,
    payload: ServiceUpdateSchema,
):
    service = get_service(service_id)

    if Service.all_objects.exclude(
        pk=service.pk
    ).filter(
        slug=slugify(payload.slug),
    ).exists():
        raise ApiHttpError(
            400,
            "Service slug already exists.",
            code="duplicate_service_slug",
        )

    (
        values,
        features,
        process_steps,
        technologies,
        faqs,
        seo,
    ) = payload_parts(payload)

    service = ServiceCatalogService.update_service(
        request=request,
        service=service,
        values=values,
        features=features,
        process_steps=process_steps,
        technologies=technologies,
        faqs=faqs,
        seo_values=seo,
        change_summary=payload.change_summary,
    )

    return serialize_service(refresh_service(service))


@router.delete(
    "/{service_id}",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("services_catalog.delete_service")
def delete_service(request, service_id: str):
    ServiceCatalogService.soft_delete_service(
        request=request,
        service=get_service(service_id),
    )

    return {
        "status": "ok",
        "message": "Service deleted successfully.",
    }


@router.post(
    "/{service_id}/publish",
    response={
        200: ServiceSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("services_catalog.change_service")
def publish_service(request, service_id: str):
    service = ServiceCatalogService.publish_service(
        request=request,
        service=get_service(service_id),
    )

    return serialize_service(refresh_service(service))


@router.post(
    "/{service_id}/schedule",
    response={
        200: ServiceSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("services_catalog.change_service")
def schedule_service(
    request,
    service_id: str,
    payload: ServiceScheduleSchema,
):
    try:
        service = (
            ServiceCatalogService.schedule_service(
                request=request,
                service=get_service(service_id),
                scheduled_for=payload.scheduled_for,
            )
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_publish_schedule",
        ) from exc

    return serialize_service(refresh_service(service))
