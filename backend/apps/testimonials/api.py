from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema, MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.api.pagination_schemas import PaginatedResponseSchema
from apps.api.responses import paginated_response
from apps.clients.models import Client
from apps.common.pagination import paginate_queryset
from apps.media_library.models import MediaAsset
from apps.projects.models import Project
from apps.rbac.services import require_permissions

from .repositories import TestimonialRepository
from .schemas import (
    TestimonialCreateSchema,
    TestimonialScheduleSchema,
    TestimonialSchema,
    TestimonialUpdateSchema,
)
from .services import TestimonialService


router = Router(
    tags=["Testimonials"],
    auth=jwt_auth,
)


def get_testimonial(testimonial_id):
    testimonial = TestimonialRepository.find_by_id(
        testimonial_id
    )

    if testimonial is None:
        raise ApiHttpError(
            404,
            "Testimonial not found.",
            code="testimonial_not_found",
        )

    return testimonial


def resolve_client(client_id):
    if client_id is None:
        return None

    client = Client.objects.filter(pk=client_id).first()

    if client is None:
        raise ApiHttpError(
            400,
            "Client not found.",
            code="invalid_client",
        )

    return client


def resolve_project(project_id):
    if project_id is None:
        return None

    project = Project.objects.filter(pk=project_id).first()

    if project is None:
        raise ApiHttpError(
            400,
            "Project not found.",
            code="invalid_project",
        )

    return project


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


def payload_values(payload):
    values = payload.dict()

    client_id = values.pop("client_id")
    project_id = values.pop("project_id")
    author_image_id = values.pop("author_image_id")
    company_logo_id = values.pop("company_logo_id")

    values["client"] = resolve_client(client_id)
    values["project"] = resolve_project(project_id)
    values["author_image"] = resolve_media(author_image_id)
    values["company_logo"] = resolve_media(company_logo_id)

    return values


def serialize_testimonial(testimonial):
    return {
        "id": testimonial.id,
        "client_id": testimonial.client_id,
        "client_name": (
            str(testimonial.client)
            if testimonial.client
            else None
        ),
        "project_id": testimonial.project_id,
        "project_title": (
            testimonial.project.title
            if testimonial.project
            else None
        ),
        "author_name": testimonial.author_name,
        "author_position": testimonial.author_position,
        "company_name": testimonial.company_name,
        "content": testimonial.content,
        "short_content": testimonial.short_content,
        "rating": testimonial.rating,
        "source": testimonial.source,
        "source_url": testimonial.source_url,
        "author_image_id": testimonial.author_image_id,
        "company_logo_id": testimonial.company_logo_id,
        "status": testimonial.status,
        "published_at": testimonial.published_at,
        "scheduled_for": testimonial.scheduled_for,
        "is_featured": testimonial.is_featured,
        "is_verified": testimonial.is_verified,
        "is_active": testimonial.is_active,
        "is_publicly_available": (
            testimonial.is_publicly_available
        ),
        "sort_order": testimonial.sort_order,
        "internal_notes": testimonial.internal_notes,
        "created_at": testimonial.created_at,
        "updated_at": testimonial.updated_at,
    }


@router.get(
    "",
    response={
        200: PaginatedResponseSchema[TestimonialSchema],
        403: ErrorSchema,
    },
)
@require_permissions("testimonials.view_testimonial")
def list_testimonials(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    status: str | None = None,
    source: str | None = None,
    rating: int | None = None,
    is_featured: bool | None = None,
    is_verified: bool | None = None,
    is_active: bool | None = None,
    client_id: str | None = None,
    project_id: str | None = None,
    ordering: str | None = None,
):
    result = paginate_queryset(
        TestimonialRepository.search(
            search=search,
            status=status,
            source=source,
            rating=rating,
            is_featured=is_featured,
            is_verified=is_verified,
            is_active=is_active,
            client_id=client_id,
            project_id=project_id,
            ordering=ordering,
        ),
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_testimonial,
    )


@router.post(
    "",
    response={
        201: TestimonialSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("testimonials.add_testimonial")
def create_testimonial(
    request,
    payload: TestimonialCreateSchema,
):
    testimonial = TestimonialService.create_testimonial(
        request=request,
        values=payload_values(payload),
    )

    return 201, serialize_testimonial(
        get_testimonial(testimonial.pk)
    )


@router.get(
    "/{testimonial_id}",
    response={
        200: TestimonialSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("testimonials.view_testimonial")
def testimonial_detail(request, testimonial_id: str):
    return serialize_testimonial(
        get_testimonial(testimonial_id)
    )


@router.put(
    "/{testimonial_id}",
    response={
        200: TestimonialSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("testimonials.change_testimonial")
def update_testimonial(
    request,
    testimonial_id: str,
    payload: TestimonialUpdateSchema,
):
    testimonial = TestimonialService.update_testimonial(
        request=request,
        testimonial=get_testimonial(testimonial_id),
        values=payload_values(payload),
    )

    return serialize_testimonial(
        get_testimonial(testimonial.pk)
    )


@router.delete(
    "/{testimonial_id}",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("testimonials.delete_testimonial")
def delete_testimonial(request, testimonial_id: str):
    TestimonialService.soft_delete(
        request=request,
        testimonial=get_testimonial(testimonial_id),
    )

    return {
        "status": "ok",
        "message": "Testimonial deleted successfully.",
    }


@router.post(
    "/{testimonial_id}/publish",
    response={
        200: TestimonialSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("testimonials.change_testimonial")
def publish_testimonial(request, testimonial_id: str):
    testimonial = TestimonialService.publish_testimonial(
        request=request,
        testimonial=get_testimonial(testimonial_id),
    )

    return serialize_testimonial(
        get_testimonial(testimonial.pk)
    )


@router.post(
    "/{testimonial_id}/schedule",
    response={
        200: TestimonialSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("testimonials.change_testimonial")
def schedule_testimonial(
    request,
    testimonial_id: str,
    payload: TestimonialScheduleSchema,
):
    try:
        testimonial = (
            TestimonialService.schedule_testimonial(
                request=request,
                testimonial=get_testimonial(
                    testimonial_id
                ),
                scheduled_for=payload.scheduled_for,
            )
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_publish_schedule",
        ) from exc

    return serialize_testimonial(
        get_testimonial(testimonial.pk)
    )
