from django.core.exceptions import ValidationError
from django.utils.text import slugify
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.api.exceptions import ApiHttpError
from apps.case_studies.models import CaseStudy
from apps.cms.models import Page
from apps.industries.models import Industry
from apps.insights.models import InsightArticle
from apps.packages_catalog.models import Package
from apps.rbac.services import require_permissions
from apps.services_catalog.models import Service

from .models import (
    NavigationMenu,
    NavigationMenuItem,
)
from .repositories import (
    NavigationMenuItemRepository,
    NavigationMenuRepository,
)
from .schemas import (
    NavigationMenuCreateSchema,
    NavigationMenuItemCreateSchema,
    NavigationMenuItemSchema,
    NavigationMenuItemUpdateSchema,
    NavigationMenuSchema,
    NavigationMenuUpdateSchema,
    NavigationReorderSchema,
)
from .services import NavigationService


router = Router(
    tags=["Navigation"],
    auth=jwt_auth,
)


def get_menu(menu_id):
    menu = NavigationMenuRepository.find_by_id(
        menu_id
    )

    if menu is None:
        raise ApiHttpError(
            404,
            "Navigation menu not found.",
            code="navigation_menu_not_found",
        )

    return menu


def get_item(item_id):
    item = NavigationMenuItemRepository.find_by_id(
        item_id
    )

    if item is None:
        raise ApiHttpError(
            404,
            "Navigation item not found.",
            code="navigation_item_not_found",
        )

    return item


def resolve_optional(model, object_id, label):
    if object_id is None:
        return None

    instance = model.objects.filter(
        pk=object_id,
    ).first()

    if instance is None:
        raise ApiHttpError(
            400,
            f"{label} not found.",
            code=f"invalid_{label.lower().replace(' ', '_')}",
        )

    return instance


def build_item_values(menu, payload):
    values = payload.dict()

    parent_id = values.pop("parent_id")
    cms_page_id = values.pop("cms_page_id")
    service_id = values.pop("service_id")
    package_id = values.pop("package_id")
    industry_id = values.pop("industry_id")
    insight_id = values.pop("insight_id")
    case_study_id = values.pop("case_study_id")

    values["menu"] = menu
    values["parent"] = (
        get_item(parent_id)
        if parent_id
        else None
    )

    if (
        values["parent"]
        and values["parent"].menu_id != menu.id
    ):
        raise ApiHttpError(
            400,
            "Parent item belongs to another menu.",
            code="invalid_navigation_parent",
        )

    values["cms_page"] = resolve_optional(
        Page,
        cms_page_id,
        "CMS page",
    )
    values["service"] = resolve_optional(
        Service,
        service_id,
        "Service",
    )
    values["package"] = resolve_optional(
        Package,
        package_id,
        "Package",
    )
    values["industry"] = resolve_optional(
        Industry,
        industry_id,
        "Industry",
    )
    values["insight"] = resolve_optional(
        InsightArticle,
        insight_id,
        "Insight",
    )
    values["case_study"] = resolve_optional(
        CaseStudy,
        case_study_id,
        "Case study",
    )

    return values


def serialize_item(item, children_map=None):
    children_map = children_map or {}

    return {
        "id": item.id,
        "menu_id": item.menu_id,
        "parent_id": item.parent_id,
        "label": item.label,
        "link_type": item.link_type,
        "url": item.url,
        "resolved_url": item.resolved_url,
        "route_name": item.route_name,
        "route_parameters": item.route_parameters,
        "cms_page_id": item.cms_page_id,
        "service_id": item.service_id,
        "package_id": item.package_id,
        "industry_id": item.industry_id,
        "insight_id": item.insight_id,
        "case_study_id": item.case_study_id,
        "visibility": item.visibility,
        "icon": item.icon,
        "css_class": item.css_class,
        "target_blank": item.target_blank,
        "rel_attribute": item.rel_attribute,
        "is_active": item.is_active,
        "is_featured": item.is_featured,
        "sort_order": item.sort_order,
        "depth": item.depth,
        "metadata": item.metadata,
        "children": [
            serialize_item(child, children_map)
            for child in children_map.get(
                item.id,
                [],
            )
        ],
    }


def serialize_menu(menu):
    items = list(
        NavigationMenuItemRepository.for_menu(
            menu.id,
        )
    )

    children_map = {}

    for item in items:
        children_map.setdefault(
            item.parent_id,
            [],
        ).append(item)

    return {
        "id": menu.id,
        "name": menu.name,
        "slug": menu.slug,
        "location": menu.location,
        "description": menu.description,
        "is_active": menu.is_active,
        "is_public": menu.is_public,
        "sort_order": menu.sort_order,
        "metadata": menu.metadata,
        "item_count": len(items),
        "items": [
            serialize_item(item, children_map)
            for item in children_map.get(
                None,
                [],
            )
        ],
    }


@router.get(
    "/menus",
    response={
        200: list[NavigationMenuSchema],
        403: ErrorSchema,
    },
)
@require_permissions("navigation.view_navigationmenu")
def list_menus(
    request,
    search: str | None = None,
    location: str | None = None,
    is_active: bool | None = None,
    is_public: bool | None = None,
    ordering: str | None = None,
):
    return [
        serialize_menu(menu)
        for menu in NavigationMenuRepository.search(
            search=search,
            location=location,
            is_active=is_active,
            is_public=is_public,
            ordering=ordering,
        )
    ]


@router.post(
    "/menus",
    response={
        201: NavigationMenuSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("navigation.add_navigationmenu")
def create_menu(
    request,
    payload: NavigationMenuCreateSchema,
):
    values = payload.dict()
    values["slug"] = slugify(payload.slug)

    if NavigationMenu.all_objects.filter(
        slug=values["slug"],
    ).exists():
        raise ApiHttpError(
            400,
            "Navigation menu slug already exists.",
            code="duplicate_navigation_menu_slug",
        )

    menu = NavigationService.create_menu(
        request=request,
        values=values,
    )

    return 201, serialize_menu(
        get_menu(menu.id)
    )


@router.get(
    "/menus/{menu_id}",
    response={
        200: NavigationMenuSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("navigation.view_navigationmenu")
def menu_detail(request, menu_id: str):
    return serialize_menu(get_menu(menu_id))


@router.put(
    "/menus/{menu_id}",
    response={
        200: NavigationMenuSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "navigation.change_navigationmenu"
)
def update_menu(
    request,
    menu_id: str,
    payload: NavigationMenuUpdateSchema,
):
    menu = get_menu(menu_id)
    values = payload.dict()
    values["slug"] = slugify(payload.slug)

    if NavigationMenu.all_objects.exclude(
        pk=menu.pk
    ).filter(
        slug=values["slug"],
    ).exists():
        raise ApiHttpError(
            400,
            "Navigation menu slug already exists.",
            code="duplicate_navigation_menu_slug",
        )

    menu = NavigationService.update_menu(
        request=request,
        menu=menu,
        values=values,
    )

    return serialize_menu(get_menu(menu.id))


@router.get(
    "/menus/{menu_id}/items",
    response={
        200: list[NavigationMenuItemSchema],
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "navigation.view_navigationmenuitem"
)
def list_menu_items(
    request,
    menu_id: str,
    parent_id: str | None = None,
    is_active: bool | None = None,
):
    menu = get_menu(menu_id)

    return [
        serialize_item(item)
        for item in (
            NavigationMenuItemRepository.for_menu(
                menu.id,
                parent_id=parent_id,
                is_active=is_active,
            )
        )
    ]


@router.post(
    "/menus/{menu_id}/items",
    response={
        201: NavigationMenuItemSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "navigation.add_navigationmenuitem"
)
def create_menu_item(
    request,
    menu_id: str,
    payload: NavigationMenuItemCreateSchema,
):
    try:
        item = NavigationService.create_item(
            request=request,
            values=build_item_values(
                get_menu(menu_id),
                payload,
            ),
        )
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Navigation item validation failed.",
            code="invalid_navigation_item",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    return 201, serialize_item(get_item(item.id))


@router.get(
    "/items/{item_id}",
    response={
        200: NavigationMenuItemSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "navigation.view_navigationmenuitem"
)
def menu_item_detail(request, item_id: str):
    return serialize_item(get_item(item_id))


@router.put(
    "/items/{item_id}",
    response={
        200: NavigationMenuItemSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "navigation.change_navigationmenuitem"
)
def update_menu_item(
    request,
    item_id: str,
    payload: NavigationMenuItemUpdateSchema,
):
    item = get_item(item_id)

    try:
        item = NavigationService.update_item(
            request=request,
            item=item,
            values=build_item_values(
                item.menu,
                payload,
            ),
        )
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Navigation item validation failed.",
            code="invalid_navigation_item",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    return serialize_item(get_item(item.id))


@router.post(
    "/menus/{menu_id}/reorder",
    response={
        200: NavigationMenuSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "navigation.change_navigationmenuitem"
)
def reorder_menu_items(
    request,
    menu_id: str,
    payload: NavigationReorderSchema,
):
    menu = get_menu(menu_id)

    try:
        NavigationService.reorder_items(
            request=request,
            menu=menu,
            items=[
                item.dict()
                for item in payload.items
            ],
        )
    except (
        ValueError,
        ValidationError,
    ) as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_navigation_reorder",
        ) from exc

    return serialize_menu(get_menu(menu.id))



from .repositories import PublicNavigationRepository
from .schemas import PublicNavigationMenuSchema
from .services import PublicNavigationService


def serialize_public_menu(menu):
    items = list(
        PublicNavigationRepository.items_for_menu(
            menu.id
        )
    )

    return {
        "id": menu.id,
        "name": menu.name,
        "slug": menu.slug,
        "location": menu.location,
        "description": menu.description,
        "metadata": menu.metadata,
        "items": PublicNavigationService.build_tree(
            items
        ),
    }


@router.get(
    "/public/menus/{slug}",
    auth=None,
    response={
        200: PublicNavigationMenuSchema,
        404: ErrorSchema,
    },
)
def public_menu_by_slug(request, slug: str):
    menu = PublicNavigationRepository.menu_by_slug(
        slug
    )

    if menu is None:
        raise ApiHttpError(
            404,
            "Public navigation menu not found.",
            code="public_navigation_menu_not_found",
        )

    return serialize_public_menu(menu)


@router.get(
    "/public/locations/{location}",
    auth=None,
    response={
        200: list[PublicNavigationMenuSchema],
    },
)
def public_menus_by_location(
    request,
    location: str,
):
    return [
        serialize_public_menu(menu)
        for menu in (
            PublicNavigationRepository
            .menus_by_location(location)
        )
    ]
