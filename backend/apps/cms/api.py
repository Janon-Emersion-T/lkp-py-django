from django.utils.text import slugify
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema, MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.api.pagination_schemas import PaginatedResponseSchema
from apps.api.responses import paginated_response
from apps.common.pagination import paginate_queryset
from apps.rbac.services import require_permissions

from .models import (
    Page,
    PageRevision,
    Redirect,
)
from .repositories import PageRepository
from .schemas import (
    PageCreateSchema,
    PageRevisionSchema,
    PageScheduleSchema,
    PageSchema,
    PageUpdateSchema,
    RedirectCreateSchema,
    RedirectSchema,
    RevisionRestoreSchema,
)
from .services import CmsService


router = Router(
    tags=["CMS"],
    auth=jwt_auth,
)


def serialize_seo(seo):
    if seo is None:
        return None

    return {
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
        "twitter_title": seo.twitter_title,
        "twitter_description": (
            seo.twitter_description
        ),
        "structured_data": seo.structured_data,
    }


def serialize_revision(revision):
    return {
        "id": revision.id,
        "revision_number": revision.revision_number,
        "title": revision.title,
        "excerpt": revision.excerpt,
        "content": revision.content,
        "status": revision.status,
        "change_summary": revision.change_summary,
        "created_at": revision.created_at,
    }


def serialize_event(event):
    return {
        "id": event.id,
        "event_type": event.event_type,
        "description": event.description,
        "metadata": event.metadata,
        "created_at": event.created_at,
    }


def serialize_page(page):
    try:
        seo = page.seo
    except Page.seo.RelatedObjectDoesNotExist:
        seo = None

    return {
        "id": page.id,
        "title": page.title,
        "slug": page.slug,
        "page_type": page.page_type,
        "status": page.status,
        "excerpt": page.excerpt,
        "content": page.content,
        "template_name": page.template_name,
        "is_indexable": page.is_indexable,
        "is_visible_in_navigation": (
            page.is_visible_in_navigation
        ),
        "navigation_label": page.navigation_label,
        "navigation_order": page.navigation_order,
        "published_at": page.published_at,
        "scheduled_for": page.scheduled_for,
        "current_revision_number": (
            page.current_revision_number
        ),
        "is_publicly_available": (
            page.is_publicly_available
        ),
        "seo": serialize_seo(seo),
        "revisions": [
            serialize_revision(revision)
            for revision in page.revisions.all()
        ],
        "publishing_events": [
            serialize_event(event)
            for event in page.publishing_events.all()
        ],
        "created_at": page.created_at,
        "updated_at": page.updated_at,
    }


def serialize_redirect(redirect):
    return {
        "id": redirect.id,
        "source_path": redirect.source_path,
        "destination_url": redirect.destination_url,
        "redirect_type": redirect.redirect_type,
        "is_active": redirect.is_active,
        "hit_count": redirect.hit_count,
        "last_accessed_at": redirect.last_accessed_at,
        "notes": redirect.notes,
        "created_at": redirect.created_at,
        "updated_at": redirect.updated_at,
    }


def get_page(page_id):
    page = PageRepository.find_by_id(page_id)

    if page is None:
        raise ApiHttpError(
            404,
            "Page not found.",
            code="page_not_found",
        )

    return page


def refresh_page(page):
    refreshed = PageRepository.queryset().filter(
        pk=page.pk,
    ).first()

    if refreshed is None:
        raise ApiHttpError(
            404,
            "Page not found.",
            code="page_not_found",
        )

    return refreshed


def page_values(payload):
    values = payload.dict()
    values.pop("seo", None)
    values.pop("change_summary", None)

    values["slug"] = slugify(values["slug"])

    return values


def seo_values(payload):
    return payload.seo.dict()


@router.get(
    "/pages",
    response={
        200: PaginatedResponseSchema[PageSchema],
        403: ErrorSchema,
    },
)
@require_permissions("cms.view_page")
def list_pages(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    status: str | None = None,
    page_type: str | None = None,
    is_indexable: bool | None = None,
    ordering: str | None = None,
):
    result = paginate_queryset(
        PageRepository.search(
            search=search,
            status=status,
            page_type=page_type,
            is_indexable=is_indexable,
            ordering=ordering,
        ),
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_page,
    )


@router.post(
    "/pages",
    response={
        201: PageSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("cms.add_page")
def create_page(request, payload: PageCreateSchema):
    normalized_slug = slugify(payload.slug)

    if Page.all_objects.filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Page slug already exists.",
            code="duplicate_page_slug",
        )

    page = CmsService.create_page(
        request=request,
        values=page_values(payload),
        seo_values=seo_values(payload),
    )

    return 201, serialize_page(refresh_page(page))


@router.get(
    "/pages/{page_id}",
    response={
        200: PageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("cms.view_page")
def page_detail(request, page_id: str):
    return serialize_page(get_page(page_id))


@router.put(
    "/pages/{page_id}",
    response={
        200: PageSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("cms.change_page")
def update_page(
    request,
    page_id: str,
    payload: PageUpdateSchema,
):
    page = get_page(page_id)
    normalized_slug = slugify(payload.slug)

    if Page.all_objects.exclude(pk=page.pk).filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Page slug already exists.",
            code="duplicate_page_slug",
        )

    page = CmsService.update_page(
        request=request,
        page=page,
        values=page_values(payload),
        seo_values=seo_values(payload),
        change_summary=payload.change_summary,
    )

    return serialize_page(refresh_page(page))


@router.delete(
    "/pages/{page_id}",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("cms.delete_page")
def delete_page(request, page_id: str):
    page = get_page(page_id)

    CmsService.soft_delete_page(
        request=request,
        page=page,
    )

    return {
        "status": "ok",
        "message": "Page deleted successfully.",
    }


@router.post(
    "/pages/{page_id}/publish",
    response={
        200: PageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("cms.change_page")
def publish_page(request, page_id: str):
    page = CmsService.publish_page(
        request=request,
        page=get_page(page_id),
    )

    return serialize_page(refresh_page(page))


@router.post(
    "/pages/{page_id}/schedule",
    response={
        200: PageSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("cms.change_page")
def schedule_page(
    request,
    page_id: str,
    payload: PageScheduleSchema,
):
    try:
        page = CmsService.schedule_page(
            request=request,
            page=get_page(page_id),
            scheduled_for=payload.scheduled_for,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_publish_schedule",
        ) from exc

    return serialize_page(refresh_page(page))


@router.post(
    "/pages/{page_id}/restore",
    response={
        200: PageSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("cms.change_page")
def restore_revision(
    request,
    page_id: str,
    payload: RevisionRestoreSchema,
):
    page = get_page(page_id)

    revision = PageRevision.objects.filter(
        pk=payload.revision_id,
    ).first()

    if revision is None:
        raise ApiHttpError(
            404,
            "Page revision not found.",
            code="revision_not_found",
        )

    try:
        page = CmsService.restore_revision(
            request=request,
            page=page,
            revision=revision,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_revision",
        ) from exc

    return serialize_page(refresh_page(page))


@router.get(
    "/pages/{page_id}/revisions",
    response={
        200: list[PageRevisionSchema],
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("cms.view_pagerevision")
def list_revisions(request, page_id: str):
    page = get_page(page_id)

    return [
        serialize_revision(revision)
        for revision in page.revisions.all()
    ]


@router.post(
    "/redirects",
    response={
        201: RedirectSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("cms.add_redirect")
def create_redirect(
    request,
    payload: RedirectCreateSchema,
):
    if Redirect.all_objects.filter(
        source_path=payload.source_path,
    ).exists():
        raise ApiHttpError(
            400,
            "Redirect source path already exists.",
            code="duplicate_redirect",
        )

    redirect = CmsService.create_redirect(
        request=request,
        values=payload.dict(),
    )

    return 201, serialize_redirect(redirect)


@router.get(
    "/redirects",
    response={
        200: list[RedirectSchema],
        403: ErrorSchema,
    },
)
@require_permissions("cms.view_redirect")
def list_redirects(request):
    return [
        serialize_redirect(redirect)
        for redirect in Redirect.objects.all()
    ]
