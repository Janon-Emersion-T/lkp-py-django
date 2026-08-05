from django.db import transaction

from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import SystemSetting


class SystemSettingService:
    @staticmethod
    @transaction.atomic
    def upsert(
        *,
        request,
        group: str,
        key: str,
        value,
        data_type: str,
        description: str = "",
        is_public: bool = False,
        is_editable: bool = True,
        is_required: bool = False,
    ) -> SystemSetting:
        setting = SystemSetting.all_objects.filter(
            group=group,
            key=key,
        ).first()

        before = None

        if setting:
            before = {
                "value": setting.value,
                "data_type": setting.data_type,
                "is_public": setting.is_public,
                "is_editable": setting.is_editable,
                "is_required": setting.is_required,
            }

            setting.value = value
            setting.data_type = data_type
            setting.description = description
            setting.is_public = is_public
            setting.is_editable = is_editable
            setting.is_required = is_required
            setting.is_deleted = False
            setting.deleted_at = None
            setting.updated_by = request.auth
            setting.save()
        else:
            setting = SystemSetting.objects.create(
                group=group,
                key=key,
                value=value,
                data_type=data_type,
                description=description,
                is_public=is_public,
                is_editable=is_editable,
                is_required=is_required,
                created_by=request.auth,
                updated_by=request.auth,
            )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=(
                AuditEventType.RECORD_UPDATED
                if before
                else AuditEventType.RECORD_CREATED
            ),
            module="settings",
            message="System setting saved.",
            target_type="settings_manager.SystemSetting",
            target_id=str(setting.pk),
            before=before,
            after={
                "group": setting.group,
                "key": setting.key,
                "value": (
                    None
                    if setting.data_type == "secret"
                    else setting.value
                ),
                "data_type": setting.data_type,
                "is_public": setting.is_public,
                "is_editable": setting.is_editable,
                "is_required": setting.is_required,
            },
        )

        return setting
