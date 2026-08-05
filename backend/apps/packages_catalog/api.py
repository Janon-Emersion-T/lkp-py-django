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

from .models import Package, PackageSeo
from .repositories import PackageRepository
from .schemas import (
    PackageCreateSchema,
    PackageScheduleSchema,
    PackageSchema,
    PackageUpdateSchema,
)
from .services import PackageCatalogService


router = Router(
    tags=["Packages Catalog"],
    auth=jwt_auth,
)


def resolve_service(service_id):
    if service_id is None:
        return None

    service = Service.objects.filter(
        pk=service_id,
    ).first()

    if service is None:
        raise ApiHttpError(
            400,
            "Service not found.",
            code="invalid_service",
        )

    return service


def resolve_media(asset_id):
    if asset_id is None:
        return None

    asset = MediaAsset.objects.filter(
        pk=asset_id,
    ).first()

    if asset is None:
        raise ApiHttpError(
            400,
            "Media asset not found.",
            code="invalid_media_asset",
        )

    return asset


def get_package(package_id):
    package = PackageRepository.find_by_id(package_id)

    if package is None:
        raise ApiHttpError(
            404,
            "Package not found.",
            code="package_not_found",
        )

    return package


def refresh_package(package):
    refreshed = PackageRepository.queryset().filter(
        pk=package.pk,
    ).first()

    if refreshed is None:
        raise ApiHttpError(
            404,
            "Package not found.",
            code="package_not_found",
        )

    return refreshed


def serialize_package(package):
    try:
        seo = package.seo
    except PackageSeo.DoesNotExist:
        seo = None

    return {
        "id": package.id,
        "name": package.name,
        "slug": package.slug,
        "category": package.category,
        "service_id": package.service_id,
        "service_title": (
            package.service.title
            if package.service
            else None
        ),
        "short_description": package.short_description,
        "description": package.description,
        "pricing_type": package.pricing_type,
        "price": package.price,
        "compare_at_price": package.compare_at_price,
        "currency": package.currency,
        "billing_cycle": package.billing_cycle,
        "delivery_time": package.delivery_time,
        "revisions_included": (
            package.revisions_included
        ),
        "support_period_days": (
            package.support_period_days
        ),
        "status": package.status,
        "published_at": package.published_at,
        "scheduled_for": package.scheduled_for,
        "is_featured": package.is_featured,
        "is_popular": package.is_popular,
        "is_active": package.is_active,
        "is_publicly_available": (
            package.is_publicly_available
        ),
        "sort_order": package.sort_order,
        "badge_text": package.badge_text,
        "cta_label": package.cta_label,
        "cta_url": package.cta_url,
        "current_revision_number": (
            package.current_revision_number
        ),
        "features": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "is_included": item.is_included,
                "value": item.value,
                "icon": item.icon,
                "sort_order": item.sort_order,
            }
            for item in package.features.all()
        ],
        "addons": [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "currency": item.currency,
                "billing_cycle": item.billing_cycle,
                "is_active": item.is_active,
                "sort_order": item.sort_order,
            }
            for item in package.addons.all()
        ],
        "target_audiences": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "sort_order": item.sort_order,
            }
            for item in package.target_audiences.all()
        ],
        "faqs": [
            {
                "id": item.id,
                "question": item.question,
                "answer": item.answer,
                "sort_order": item.sort_order,
            }
            for item in package.faqs.all()
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
            for item in package.revisions.all()
        ],
        "created_at": package.created_at,
        "updated_at": package.updated_at,
    }


def payload_parts(payload):
    raw = payload.dict()

    features = [
        item.dict()
        for item in payload.features
    ]

    addons = []

    for item in payload.addons:
        values = item.dict()
        values["currency"] = values[
            "currency"
        ].upper()
        addons.append(values)

    audiences = [
        item.dict()
        for item in payload.target_audiences
    ]

    faqs = [
        item.dict()
        for item in payload.faqs
    ]

    seo = payload.seo.dict()
    image_id = seo.pop("open_graph_image_id")
    seo["open_graph_image"] = resolve_media(image_id)

    values = {
        key: value
        for key, value in raw.items()
        if key not in (
            "features",
            "addons",
            "target_audiences",
            "faqs",
            "seo",
            "change_summary",
            "service_id",
        )
    }

    values["slug"] = slugify(payload.slug)
    values["currency"] = payload.currency.upper()
    values["service"] = resolve_service(
        payload.service_id
    )

    return (
        values,
        features,
        addons,
        audiences,
        faqs,
        seo,
    )


@router.get(
    "",
    response={
        200: PaginatedResponseSchema[PackageSchema],
        403: ErrorSchema,
    },
)
@require_permissions("packages_catalog.view_package")
def list_packages(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    category: str | None = None,
    status: str | None = None,
    service_id: str | None = None,
    currency: str | None = None,
    billing_cycle: str | None = None,
    is_featured: bool | None = None,
    is_popular: bool | None = None,
    is_active: bool | None = None,
    ordering: str | None = None,
):
    result = paginate_queryset(
        PackageRepository.search(
            search=search,
            category=category,
            status=status,
            service_id=service_id,
            currency=currency,
            billing_cycle=billing_cycle,
            is_featured=is_featured,
            is_popular=is_popular,
            is_active=is_active,
            ordering=ordering,
        ),
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_package,
    )


@router.post(
    "",
    response={
        201: PackageSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("packages_catalog.add_package")
def create_package(
    request,
    payload: PackageCreateSchema,
):
    normalized_slug = slugify(payload.slug)

    if Package.all_objects.filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Package slug already exists.",
            code="duplicate_package_slug",
        )

    (
        values,
        features,
        addons,
        audiences,
        faqs,
        seo,
    ) = payload_parts(payload)

    package = PackageCatalogService.create_package(
        request=request,
        values=values,
        features=features,
        addons=addons,
        target_audiences=audiences,
        faqs=faqs,
        seo_values=seo,
    )

    return 201, serialize_package(
        refresh_package(package)
    )


@router.get(
    "/{package_id}",
    response={
        200: PackageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("packages_catalog.view_package")
def package_detail(request, package_id: str):
    return serialize_package(
        get_package(package_id)
    )


@router.put(
    "/{package_id}",
    response={
        200: PackageSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("packages_catalog.change_package")
def update_package(
    request,
    package_id: str,
    payload: PackageUpdateSchema,
):
    package = get_package(package_id)
    normalized_slug = slugify(payload.slug)

    if Package.all_objects.exclude(
        pk=package.pk
    ).filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Package slug already exists.",
            code="duplicate_package_slug",
        )

    (
        values,
        features,
        addons,
        audiences,
        faqs,
        seo,
    ) = payload_parts(payload)

    package = PackageCatalogService.update_package(
        request=request,
        package=package,
        values=values,
        features=features,
        addons=addons,
        target_audiences=audiences,
        faqs=faqs,
        seo_values=seo,
        change_summary=payload.change_summary,
    )

    return serialize_package(
        refresh_package(package)
    )


@router.delete(
    "/{package_id}",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("packages_catalog.delete_package")
def delete_package(request, package_id: str):
    PackageCatalogService.soft_delete_package(
        request=request,
        package=get_package(package_id),
    )

    return {
        "status": "ok",
        "message": "Package deleted successfully.",
    }


@router.post(
    "/{package_id}/publish",
    response={
        200: PackageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("packages_catalog.change_package")
def publish_package(request, package_id: str):
    package = PackageCatalogService.publish_package(
        request=request,
        package=get_package(package_id),
    )

    return serialize_package(
        refresh_package(package)
    )


@router.post(
    "/{package_id}/schedule",
    response={
        200: PackageSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("packages_catalog.change_package")
def schedule_package(
    request,
    package_id: str,
    payload: PackageScheduleSchema,
):
    try:
        package = (
            PackageCatalogService.schedule_package(
                request=request,
                package=get_package(package_id),
                scheduled_for=payload.scheduled_for,
            )
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_publish_schedule",
        ) from exc

    return serialize_package(
        refresh_package(package)
    )
