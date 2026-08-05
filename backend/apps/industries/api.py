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
from apps.services_catalog.models import Service

from .models import Industry, IndustrySeo
from .repositories import IndustryRepository
from .schemas import (
    IndustryCreateSchema,
    IndustryScheduleSchema,
    IndustrySchema,
    IndustryUpdateSchema,
)
from .services import IndustryServiceLayer


router = Router(
    tags=["Industries"],
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


def resolve_service(service_id):
    service = Service.objects.filter(pk=service_id).first()

    if service is None:
        raise ApiHttpError(
            400,
            "Service not found.",
            code="invalid_service",
        )

    return service


def get_industry(industry_id):
    industry = IndustryRepository.find_by_id(industry_id)

    if industry is None:
        raise ApiHttpError(
            404,
            "Industry not found.",
            code="industry_not_found",
        )

    return industry


def refresh_industry(industry):
    refreshed = IndustryRepository.queryset().filter(
        pk=industry.pk,
    ).first()

    if refreshed is None:
        raise ApiHttpError(
            404,
            "Industry not found.",
            code="industry_not_found",
        )

    return refreshed


def serialize_industry(industry):
    try:
        seo = industry.seo
    except IndustrySeo.DoesNotExist:
        seo = None

    return {
        "id": industry.id,
        "name": industry.name,
        "slug": industry.slug,
        "short_description": industry.short_description,
        "description": industry.description,
        "hero_title": industry.hero_title,
        "hero_description": industry.hero_description,
        "hero_image_id": industry.hero_image_id,
        "icon": industry.icon,
        "status": industry.status,
        "published_at": industry.published_at,
        "scheduled_for": industry.scheduled_for,
        "is_featured": industry.is_featured,
        "is_active": industry.is_active,
        "is_publicly_available": (
            industry.is_publicly_available
        ),
        "sort_order": industry.sort_order,
        "challenges": industry.challenges,
        "solutions": industry.solutions,
        "benefits": industry.benefits,
        "cta_title": industry.cta_title,
        "cta_text": industry.cta_text,
        "cta_label": industry.cta_label,
        "cta_url": industry.cta_url,
        "current_revision_number": (
            industry.current_revision_number
        ),
        "services": [
            {
                "id": item.id,
                "service_id": item.service_id,
                "service_title": item.service.title,
                "description": item.description,
                "sort_order": item.sort_order,
                "is_featured": item.is_featured,
            }
            for item in industry.service_links.all()
        ],
        "faqs": [
            {
                "id": item.id,
                "question": item.question,
                "answer": item.answer,
                "sort_order": item.sort_order,
            }
            for item in industry.faqs.all()
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
                "id": item.id,
                "revision_number": item.revision_number,
                "snapshot": item.snapshot,
                "change_summary": item.change_summary,
                "created_at": item.created_at,
            }
            for item in industry.revisions.all()
        ],
        "created_at": industry.created_at,
        "updated_at": industry.updated_at,
    }


def payload_parts(payload):
    raw = payload.dict()

    services = []

    for item in payload.services:
        values = item.dict()
        service_id = values.pop("service_id")
        values["service"] = resolve_service(service_id)
        services.append(values)

    faqs = [item.dict() for item in payload.faqs]

    seo = payload.seo.dict()
    image_id = seo.pop("open_graph_image_id")
    seo["open_graph_image"] = resolve_media(image_id)

    values = {
        key: value
        for key, value in raw.items()
        if key not in (
            "services",
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

    return values, services, faqs, seo


@router.get(
    "",
    response={
        200: PaginatedResponseSchema[IndustrySchema],
        403: ErrorSchema,
    },
)
@require_permissions("industries.view_industry")
def list_industries(
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
        IndustryRepository.search(
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
        serializer=serialize_industry,
    )


@router.post(
    "",
    response={
        201: IndustrySchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("industries.add_industry")
def create_industry(
    request,
    payload: IndustryCreateSchema,
):
    normalized_slug = slugify(payload.slug)

    if Industry.all_objects.filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Industry slug already exists.",
            code="duplicate_industry_slug",
        )

    values, services, faqs, seo = payload_parts(payload)

    industry = IndustryServiceLayer.create_industry(
        request=request,
        values=values,
        services=services,
        faqs=faqs,
        seo_values=seo,
    )

    return 201, serialize_industry(
        refresh_industry(industry)
    )


@router.get(
    "/{industry_id}",
    response={
        200: IndustrySchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("industries.view_industry")
def industry_detail(request, industry_id: str):
    return serialize_industry(
        get_industry(industry_id)
    )


@router.put(
    "/{industry_id}",
    response={
        200: IndustrySchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("industries.change_industry")
def update_industry(
    request,
    industry_id: str,
    payload: IndustryUpdateSchema,
):
    industry = get_industry(industry_id)
    normalized_slug = slugify(payload.slug)

    if Industry.all_objects.exclude(
        pk=industry.pk
    ).filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Industry slug already exists.",
            code="duplicate_industry_slug",
        )

    values, services, faqs, seo = payload_parts(payload)

    industry = IndustryServiceLayer.update_industry(
        request=request,
        industry=industry,
        values=values,
        services=services,
        faqs=faqs,
        seo_values=seo,
        change_summary=payload.change_summary,
    )

    return serialize_industry(
        refresh_industry(industry)
    )


@router.delete(
    "/{industry_id}",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("industries.delete_industry")
def delete_industry(request, industry_id: str):
    IndustryServiceLayer.soft_delete(
        request=request,
        industry=get_industry(industry_id),
    )

    return {
        "status": "ok",
        "message": "Industry deleted successfully.",
    }


@router.post(
    "/{industry_id}/publish",
    response={
        200: IndustrySchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("industries.change_industry")
def publish_industry(request, industry_id: str):
    industry = IndustryServiceLayer.publish_industry(
        request=request,
        industry=get_industry(industry_id),
    )

    return serialize_industry(
        refresh_industry(industry)
    )


@router.post(
    "/{industry_id}/schedule",
    response={
        200: IndustrySchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("industries.change_industry")
def schedule_industry(
    request,
    industry_id: str,
    payload: IndustryScheduleSchema,
):
    try:
        industry = IndustryServiceLayer.schedule_industry(
            request=request,
            industry=get_industry(industry_id),
            scheduled_for=payload.scheduled_for,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_publish_schedule",
        ) from exc

    return serialize_industry(
        refresh_industry(industry)
    )
