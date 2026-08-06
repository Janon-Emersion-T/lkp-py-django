from django.core.exceptions import ValidationError
from django.utils.text import slugify
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.api.exceptions import ApiHttpError
from apps.media_library.models import MediaAsset
from apps.rbac.services import require_permissions

from .models import (
    SettingEnvironment,
    WebsiteSetting,
    WebsiteSettingGroup,
)
from .repositories import (
    PublicWebsiteSettingRepository,
    WebsiteSettingGroupRepository,
    WebsiteSettingRepository,
)
from .schemas import (
    PublicWebsiteSettingsSchema,
    WebsiteSettingBulkUpdateSchema,
    WebsiteSettingCreateSchema,
    WebsiteSettingGroupCreateSchema,
    WebsiteSettingGroupSchema,
    WebsiteSettingGroupUpdateSchema,
    WebsiteSettingSchema,
    WebsiteSettingUpdateSchema,
)
from .services import WebsiteSettingService


router = Router(
    tags=["Global Website Settings"],
    auth=jwt_auth,
)


def get_group(group_id):
    group = WebsiteSettingGroupRepository.find_by_id(
        group_id
    )

    if group is None:
        raise ApiHttpError(
            404,
            "Website setting group not found.",
            code="website_setting_group_not_found",
        )

    return group


def get_setting(setting_id):
    setting = WebsiteSettingRepository.find_by_id(
        setting_id
    )

    if setting is None:
        raise ApiHttpError(
            404,
            "Website setting not found.",
            code="website_setting_not_found",
        )

    return setting


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


def serialize_setting(setting):
    typed_value = setting.typed_value

    if hasattr(typed_value, "as_tuple"):
        typed_value = str(typed_value)

    if hasattr(typed_value, "hex"):
        typed_value = str(typed_value)

    return {
        "id": setting.id,
        "group_id": setting.group_id,
        "group_name": setting.group.name,
        "key": setting.key,
        "label": setting.label,
        "description": setting.description,
        "value_type": setting.value_type,
        "environment": setting.environment,
        "value": setting.value,
        "json_value": setting.json_value,
        "media_asset_id": setting.media_asset_id,
        "default_value": setting.default_value,
        "validation_rules": setting.validation_rules,
        "typed_value": typed_value,
        "is_public": setting.is_public,
        "is_editable": setting.is_editable,
        "is_required": setting.is_required,
        "is_active": setting.is_active,
        "sort_order": setting.sort_order,
    }


def serialize_group(group):
    settings = list(
        WebsiteSettingRepository.search(
            group_id=group.id,
        )
    )

    return {
        "id": group.id,
        "name": group.name,
        "slug": group.slug,
        "description": group.description,
        "icon": group.icon,
        "is_active": group.is_active,
        "sort_order": group.sort_order,
        "setting_count": len(settings),
        "settings": [
            serialize_setting(setting)
            for setting in settings
        ],
    }


def setting_values(payload):
    values = payload.dict()

    group_id = values.pop("group_id")
    media_asset_id = values.pop("media_asset_id")

    values["group"] = get_group(group_id)
    values["media_asset"] = resolve_media(
        media_asset_id
    )

    return values


@router.get(
    "/groups",
    response={
        200: list[WebsiteSettingGroupSchema],
        403: ErrorSchema,
    },
)
@require_permissions(
    "website_settings.view_websitesettinggroup"
)
def list_setting_groups(
    request,
    search: str | None = None,
    is_active: bool | None = None,
):
    return [
        serialize_group(group)
        for group in (
            WebsiteSettingGroupRepository.search(
                search=search,
                is_active=is_active,
            )
        )
    ]


@router.post(
    "/groups",
    response={
        201: WebsiteSettingGroupSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "website_settings.add_websitesettinggroup"
)
def create_setting_group(
    request,
    payload: WebsiteSettingGroupCreateSchema,
):
    values = payload.dict()
    values["slug"] = slugify(payload.slug)

    if WebsiteSettingGroup.all_objects.filter(
        slug=values["slug"],
    ).exists():
        raise ApiHttpError(
            400,
            "Website setting group slug already exists.",
            code="duplicate_website_setting_group_slug",
        )

    group = WebsiteSettingService.create_group(
        request=request,
        values=values,
    )

    return 201, serialize_group(
        get_group(group.id)
    )


@router.put(
    "/groups/{group_id}",
    response={
        200: WebsiteSettingGroupSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "website_settings.change_websitesettinggroup"
)
def update_setting_group(
    request,
    group_id: str,
    payload: WebsiteSettingGroupUpdateSchema,
):
    group = get_group(group_id)
    values = payload.dict()
    values["slug"] = slugify(payload.slug)

    if WebsiteSettingGroup.all_objects.exclude(
        pk=group.pk
    ).filter(
        slug=values["slug"],
    ).exists():
        raise ApiHttpError(
            400,
            "Website setting group slug already exists.",
            code="duplicate_website_setting_group_slug",
        )

    group = WebsiteSettingService.update_group(
        request=request,
        group=group,
        values=values,
    )

    return serialize_group(get_group(group.id))


@router.get(
    "/settings",
    response={
        200: list[WebsiteSettingSchema],
        403: ErrorSchema,
    },
)
@require_permissions(
    "website_settings.view_websitesetting"
)
def list_settings(
    request,
    search: str | None = None,
    group_id: str | None = None,
    value_type: str | None = None,
    environment: str | None = None,
    is_public: bool | None = None,
    is_editable: bool | None = None,
    is_active: bool | None = None,
    ordering: str | None = None,
):
    return [
        serialize_setting(setting)
        for setting in WebsiteSettingRepository.search(
            search=search,
            group_id=group_id,
            value_type=value_type,
            environment=environment,
            is_public=is_public,
            is_editable=is_editable,
            is_active=is_active,
            ordering=ordering,
        )
    ]


@router.post(
    "/settings",
    response={
        201: WebsiteSettingSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "website_settings.add_websitesetting"
)
def create_setting(
    request,
    payload: WebsiteSettingCreateSchema,
):
    if WebsiteSetting.all_objects.filter(
        key=payload.key,
        environment=payload.environment,
    ).exists():
        raise ApiHttpError(
            400,
            "Website setting key already exists "
            "for this environment.",
            code="duplicate_website_setting_key",
        )

    try:
        setting = WebsiteSettingService.create_setting(
            request=request,
            values=setting_values(payload),
        )
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Website setting validation failed.",
            code="invalid_website_setting",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    return 201, serialize_setting(
        get_setting(setting.id)
    )


@router.get(
    "/settings/{setting_id}",
    response={
        200: WebsiteSettingSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "website_settings.view_websitesetting"
)
def setting_detail(request, setting_id: str):
    return serialize_setting(
        get_setting(setting_id)
    )


@router.put(
    "/settings/{setting_id}",
    response={
        200: WebsiteSettingSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "website_settings.change_websitesetting"
)
def update_setting(
    request,
    setting_id: str,
    payload: WebsiteSettingUpdateSchema,
):
    setting = get_setting(setting_id)

    if WebsiteSetting.all_objects.exclude(
        pk=setting.pk
    ).filter(
        key=payload.key,
        environment=payload.environment,
    ).exists():
        raise ApiHttpError(
            400,
            "Website setting key already exists "
            "for this environment.",
            code="duplicate_website_setting_key",
        )

    try:
        setting = WebsiteSettingService.update_setting(
            request=request,
            setting=setting,
            values=setting_values(payload),
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="website_setting_not_editable",
        ) from exc
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Website setting validation failed.",
            code="invalid_website_setting",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    return serialize_setting(
        get_setting(setting.id)
    )


@router.put(
    "/settings/bulk",
    response={
        200: list[WebsiteSettingSchema],
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "website_settings.change_websitesetting"
)
def bulk_update_settings(
    request,
    payload: WebsiteSettingBulkUpdateSchema,
):
    updates = []

    for item in payload.settings:
        setting = get_setting(item.setting_id)

        update = {
            "setting": setting,
        }

        if item.value is not None:
            update["value"] = item.value

        if item.json_value is not None:
            update["json_value"] = item.json_value

        if item.media_asset_id is not None:
            update["media_asset"] = resolve_media(
                item.media_asset_id
            )

        updates.append(update)

    try:
        settings = (
            WebsiteSettingService.bulk_update_values(
                request=request,
                updates=updates,
            )
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="website_setting_not_editable",
        ) from exc
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Website setting validation failed.",
            code="invalid_website_setting",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    return [
        serialize_setting(
            get_setting(setting.id)
        )
        for setting in settings
    ]


@router.get(
    "/public",
    auth=None,
    response={
        200: PublicWebsiteSettingsSchema,
        400: ErrorSchema,
    },
)
def public_settings(
    request,
    environment: str = (
        SettingEnvironment.PRODUCTION
    ),
):
    valid_environments = {
        choice
        for choice, _ in SettingEnvironment.choices
    }

    if environment not in valid_environments:
        raise ApiHttpError(
            400,
            "Invalid website settings environment.",
            code="invalid_settings_environment",
        )

    resolved = (
        PublicWebsiteSettingRepository
        .values_for_environment(environment)
    )

    settings = {}

    for key, setting in resolved.items():
        value = setting.typed_value

        if hasattr(value, "as_tuple"):
            value = str(value)

        if setting.value_type == "media":
            value = (
                str(setting.media_asset_id)
                if setting.media_asset_id
                else None
            )

        settings[key] = value

    return {
        "environment": environment,
        "settings": settings,
    }
