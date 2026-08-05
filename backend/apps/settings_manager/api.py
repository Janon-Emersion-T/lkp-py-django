from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.rbac.services import require_permissions

from .repositories import SystemSettingRepository
from .schemas import (
    SystemSettingSchema,
    SystemSettingUpsertSchema,
)
from .services import SystemSettingService


router = Router(
    tags=["System Settings"],
    auth=jwt_auth,
)


def serialize_setting(setting):
    return {
        "id": setting.id,
        "group": setting.group,
        "key": setting.key,
        "value": (
            None
            if setting.data_type == "secret"
            else setting.value
        ),
        "data_type": setting.data_type,
        "description": setting.description,
        "is_public": setting.is_public,
        "is_editable": setting.is_editable,
        "is_required": setting.is_required,
    }


@router.get(
    "",
    response={
        200: list[SystemSettingSchema],
        403: ErrorSchema,
    },
)
@require_permissions("settings_manager.view_systemsetting")
def list_settings(request, group: str | None = None):
    return [
        serialize_setting(setting)
        for setting in SystemSettingRepository.list_settings(
            group=group,
        )
    ]


@router.put(
    "",
    response={
        200: SystemSettingSchema,
        403: ErrorSchema,
    },
)
@require_permissions("settings_manager.change_systemsetting")
def upsert_setting(
    request,
    payload: SystemSettingUpsertSchema,
):
    setting = SystemSettingService.upsert(
        request=request,
        group=payload.group,
        key=payload.key,
        value=payload.value,
        data_type=payload.data_type,
        description=payload.description,
        is_public=payload.is_public,
        is_editable=payload.is_editable,
        is_required=payload.is_required,
    )

    return serialize_setting(setting)
