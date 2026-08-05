from django.utils.text import slugify
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import (
    ErrorSchema,
    MessageSchema,
)
from apps.api.exceptions import ApiHttpError
from apps.api.pagination_schemas import (
    PaginatedResponseSchema,
)
from apps.api.responses import paginated_response
from apps.clients.models import Client
from apps.common.pagination import paginate_queryset
from apps.industries.models import Industry
from apps.media_library.models import MediaAsset
from apps.projects.models import Project
from apps.rbac.services import require_permissions
from apps.services_catalog.models import Service

from .models import (
    CaseStudy,
    CaseStudySeo,
)
from .repositories import CaseStudyRepository
from .schemas import (
    CaseStudyCreateSchema,
    CaseStudyScheduleSchema,
    CaseStudySchema,
    CaseStudyUpdateSchema,
)
from .services import CaseStudyServiceLayer


router = Router(
    tags=["Case Studies"],
    auth=jwt_auth,
)


def resolve_optional(model, object_id, error_message, error_code):
    if object_id is None:
        return None

    instance = model.objects.filter(pk=object_id).first()

    if instance is None:
        raise ApiHttpError(
            400,
            error_message,
            code=error_code,
        )

    return instance


def resolve_service(service_id):
    return resolve_optional(
        Service,
        service_id,
        "Service not found.",
        "invalid_service",
    )


def resolve_media(asset_id):
    return resolve_optional(
        MediaAsset,
        asset_id,
        "Media asset not found.",
        "invalid_media_asset",
    )


def get_case_study(case_study_id):
    case_study = CaseStudyRepository.find_by_id(
        case_study_id
    )

    if case_study is None:
        raise ApiHttpError(
            404,
            "Case study not found.",
            code="case_study_not_found",
        )

    return case_study


def refresh_case_study(case_study):
    refreshed = CaseStudyRepository.queryset().filter(
        pk=case_study.pk,
    ).first()

    if refreshed is None:
        raise ApiHttpError(
            404,
            "Case study not found.",
            code="case_study_not_found",
        )

    return refreshed


def serialize_case_study(case_study):
    try:
        seo = case_study.seo
    except CaseStudySeo.DoesNotExist:
        seo = None

    return {
        "id": case_study.id,
        "title": case_study.title,
        "slug": case_study.slug,
        "client_id": case_study.client_id,
        "client_name": case_study.client_name,
        "linked_client_name": (
            case_study.client.company_name
            if case_study.client
            else None
        ),
        "project_id": case_study.project_id,
        "project_name": (
            case_study.project.name
            if case_study.project
            else None
        ),
        "industry_id": case_study.industry_id,
        "industry_name": (
            case_study.industry.name
            if case_study.industry
            else None
        ),
        "location": case_study.location,
        "website_url": case_study.website_url,
        "short_description": (
            case_study.short_description
        ),
        "overview": case_study.overview,
        "challenge": case_study.challenge,
        "solution": case_study.solution,
        "implementation": case_study.implementation,
        "results": case_study.results,
        "testimonial": case_study.testimonial,
        "testimonial_author": (
            case_study.testimonial_author
        ),
        "testimonial_position": (
            case_study.testimonial_position
        ),
        "featured_image_id": (
            case_study.featured_image_id
        ),
        "status": case_study.status,
        "published_at": case_study.published_at,
        "scheduled_for": case_study.scheduled_for,
        "project_start_date": (
            case_study.project_start_date
        ),
        "project_completion_date": (
            case_study.project_completion_date
        ),
        "project_duration": (
            case_study.project_duration
        ),
        "is_featured": case_study.is_featured,
        "is_active": case_study.is_active,
        "is_publicly_available": (
            case_study.is_publicly_available
        ),
        "sort_order": case_study.sort_order,
        "view_count": case_study.view_count,
        "current_revision_number": (
            case_study.current_revision_number
        ),
        "services": [
            {
                "id": item.id,
                "service_id": item.service_id,
                "service_title": item.service.title,
                "description": item.description,
                "sort_order": item.sort_order,
            }
            for item in case_study.service_links.all()
        ],
        "technologies": [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "logo_id": item.logo_id,
                "sort_order": item.sort_order,
            }
            for item in case_study.technologies.all()
        ],
        "media_items": [
            {
                "id": item.id,
                "asset_id": item.asset_id,
                "asset_title": item.asset.title,
                "title": item.title,
                "caption": item.caption,
                "media_role": item.media_role,
                "sort_order": item.sort_order,
            }
            for item in case_study.media_items.all()
        ],
        "metrics": [
            {
                "id": item.id,
                "label": item.label,
                "value": item.value,
                "description": item.description,
                "icon": item.icon,
                "sort_order": item.sort_order,
            }
            for item in case_study.metrics.all()
        ],
        "milestones": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "milestone_date": item.milestone_date,
                "sort_order": item.sort_order,
            }
            for item in case_study.milestones.all()
        ],
        "seo": (
            {
                "id": seo.id,
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
                "revision_number": (
                    revision.revision_number
                ),
                "snapshot": revision.snapshot,
                "change_summary": (
                    revision.change_summary
                ),
                "created_at": revision.created_at,
            }
            for revision in case_study.revisions.all()
        ],
        "created_at": case_study.created_at,
        "updated_at": case_study.updated_at,
    }


def payload_parts(payload):
    raw = payload.dict()

    services = []

    for item in payload.services:
        values = item.dict()
        service_id = values.pop("service_id")
        values["service"] = resolve_service(service_id)
        services.append(values)

    technologies = []

    for item in payload.technologies:
        values = item.dict()
        logo_id = values.pop("logo_id")
        values["logo"] = resolve_media(logo_id)
        technologies.append(values)

    media_items = []

    for item in payload.media_items:
        values = item.dict()
        asset_id = values.pop("asset_id")
        values["asset"] = resolve_media(asset_id)
        media_items.append(values)

    metrics = [
        item.dict()
        for item in payload.metrics
    ]

    milestones = [
        item.dict()
        for item in payload.milestones
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
            "services",
            "technologies",
            "media_items",
            "metrics",
            "milestones",
            "seo",
            "change_summary",
            "client_id",
            "project_id",
            "industry_id",
            "featured_image_id",
        )
    }

    values["slug"] = slugify(payload.slug)

    values["client"] = resolve_optional(
        Client,
        payload.client_id,
        "Client not found.",
        "invalid_client",
    )

    values["project"] = resolve_optional(
        Project,
        payload.project_id,
        "Project not found.",
        "invalid_project",
    )

    values["industry"] = resolve_optional(
        Industry,
        payload.industry_id,
        "Industry not found.",
        "invalid_industry",
    )

    values["featured_image"] = resolve_media(
        payload.featured_image_id
    )

    return (
        values,
        services,
        technologies,
        media_items,
        metrics,
        milestones,
        seo,
    )


@router.get(
    "",
    response={
        200: PaginatedResponseSchema[CaseStudySchema],
        403: ErrorSchema,
    },
)
@require_permissions("case_studies.view_casestudy")
def list_case_studies(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    status: str | None = None,
    client_id: str | None = None,
    project_id: str | None = None,
    industry_id: str | None = None,
    service_id: str | None = None,
    is_featured: bool | None = None,
    is_active: bool | None = None,
    ordering: str | None = None,
):
    result = paginate_queryset(
        CaseStudyRepository.search(
            search=search,
            status=status,
            client_id=client_id,
            project_id=project_id,
            industry_id=industry_id,
            service_id=service_id,
            is_featured=is_featured,
            is_active=is_active,
            ordering=ordering,
        ),
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_case_study,
    )


@router.post(
    "",
    response={
        201: CaseStudySchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("case_studies.add_casestudy")
def create_case_study(
    request,
    payload: CaseStudyCreateSchema,
):
    normalized_slug = slugify(payload.slug)

    if CaseStudy.all_objects.filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Case study slug already exists.",
            code="duplicate_case_study_slug",
        )

    (
        values,
        services,
        technologies,
        media_items,
        metrics,
        milestones,
        seo,
    ) = payload_parts(payload)

    case_study = (
        CaseStudyServiceLayer.create_case_study(
            request=request,
            values=values,
            services=services,
            technologies=technologies,
            media_items=media_items,
            metrics=metrics,
            milestones=milestones,
            seo_values=seo,
        )
    )

    return 201, serialize_case_study(
        refresh_case_study(case_study)
    )


@router.get(
    "/{case_study_id}",
    response={
        200: CaseStudySchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("case_studies.view_casestudy")
def case_study_detail(
    request,
    case_study_id: str,
):
    return serialize_case_study(
        get_case_study(case_study_id)
    )


@router.put(
    "/{case_study_id}",
    response={
        200: CaseStudySchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("case_studies.change_casestudy")
def update_case_study(
    request,
    case_study_id: str,
    payload: CaseStudyUpdateSchema,
):
    case_study = get_case_study(case_study_id)
    normalized_slug = slugify(payload.slug)

    if CaseStudy.all_objects.exclude(
        pk=case_study.pk
    ).filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Case study slug already exists.",
            code="duplicate_case_study_slug",
        )

    (
        values,
        services,
        technologies,
        media_items,
        metrics,
        milestones,
        seo,
    ) = payload_parts(payload)

    case_study = (
        CaseStudyServiceLayer.update_case_study(
            request=request,
            case_study=case_study,
            values=values,
            services=services,
            technologies=technologies,
            media_items=media_items,
            metrics=metrics,
            milestones=milestones,
            seo_values=seo,
            change_summary=payload.change_summary,
        )
    )

    return serialize_case_study(
        refresh_case_study(case_study)
    )


@router.delete(
    "/{case_study_id}",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("case_studies.delete_casestudy")
def delete_case_study(
    request,
    case_study_id: str,
):
    CaseStudyServiceLayer.soft_delete(
        request=request,
        case_study=get_case_study(case_study_id),
    )

    return {
        "status": "ok",
        "message": "Case study deleted successfully.",
    }


@router.post(
    "/{case_study_id}/publish",
    response={
        200: CaseStudySchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("case_studies.change_casestudy")
def publish_case_study(
    request,
    case_study_id: str,
):
    case_study = CaseStudyServiceLayer.publish(
        request=request,
        case_study=get_case_study(case_study_id),
    )

    return serialize_case_study(
        refresh_case_study(case_study)
    )


@router.post(
    "/{case_study_id}/schedule",
    response={
        200: CaseStudySchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("case_studies.change_casestudy")
def schedule_case_study(
    request,
    case_study_id: str,
    payload: CaseStudyScheduleSchema,
):
    try:
        case_study = CaseStudyServiceLayer.schedule(
            request=request,
            case_study=get_case_study(
                case_study_id
            ),
            scheduled_for=payload.scheduled_for,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_publish_schedule",
        ) from exc

    return serialize_case_study(
        refresh_case_study(case_study)
    )
