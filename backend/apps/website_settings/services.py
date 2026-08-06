from django.db import transaction

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    WebsiteSetting,
    WebsiteSettingGroup,
)


class WebsiteSettingService:
    @staticmethod
    def group_snapshot(group):
        return {
            "id": str(group.id),
            "name": group.name,
            "slug": group.slug,
            "is_active": group.is_active,
            "sort_order": group.sort_order,
        }

    @staticmethod
    def setting_snapshot(setting):
        return {
            "id": str(setting.id),
            "group_id": str(setting.group_id),
            "key": setting.key,
            "label": setting.label,
            "value_type": setting.value_type,
            "environment": setting.environment,
            "value": setting.value,
            "json_value": setting.json_value,
            "media_asset_id": (
                str(setting.media_asset_id)
                if setting.media_asset_id
                else None
            ),
            "is_public": setting.is_public,
            "is_editable": setting.is_editable,
            "is_required": setting.is_required,
            "is_active": setting.is_active,
        }

    @classmethod
    @transaction.atomic
    def create_group(
        cls,
        *,
        request,
        values,
    ):
        group = WebsiteSettingGroup.objects.create(
            **values,
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="website_settings",
            message="Website setting group created.",
            target_type=(
                "website_settings.WebsiteSettingGroup"
            ),
            target_id=str(group.pk),
            metadata={
                "after": cls.group_snapshot(group),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="create_setting_group",
            module="website_settings",
            description=(
                f"Created website setting group "
                f"{group.name}."
            ),
            entity_type=(
                "website_settings.WebsiteSettingGroup"
            ),
            entity_id=str(group.pk),
        )

        return group

    @classmethod
    @transaction.atomic
    def update_group(
        cls,
        *,
        request,
        group,
        values,
    ):
        before = cls.group_snapshot(group)

        for field, value in values.items():
            setattr(group, field, value)

        group.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="website_settings",
            message="Website setting group updated.",
            target_type=(
                "website_settings.WebsiteSettingGroup"
            ),
            target_id=str(group.pk),
            metadata={
                "before": before,
                "after": cls.group_snapshot(group),
            },
        )

        return group

    @classmethod
    @transaction.atomic
    def create_setting(
        cls,
        *,
        request,
        values,
    ):
        setting = WebsiteSetting(**values)
        setting.full_clean()
        setting.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="website_settings",
            message="Website setting created.",
            target_type="website_settings.WebsiteSetting",
            target_id=str(setting.pk),
            metadata={
                "after": cls.setting_snapshot(setting),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="create_setting",
            module="website_settings",
            description=(
                f"Created website setting {setting.key}."
            ),
            entity_type="website_settings.WebsiteSetting",
            entity_id=str(setting.pk),
        )

        return setting

    @classmethod
    @transaction.atomic
    def update_setting(
        cls,
        *,
        request,
        setting,
        values,
    ):
        if not setting.is_editable:
            raise ValueError(
                "This website setting is not editable."
            )

        before = cls.setting_snapshot(setting)

        for field, value in values.items():
            setattr(setting, field, value)

        setting.full_clean()
        setting.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="website_settings",
            message="Website setting updated.",
            target_type="website_settings.WebsiteSetting",
            target_id=str(setting.pk),
            metadata={
                "before": before,
                "after": cls.setting_snapshot(setting),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="update_setting",
            module="website_settings",
            description=(
                f"Updated website setting {setting.key}."
            ),
            entity_type="website_settings.WebsiteSetting",
            entity_id=str(setting.pk),
        )

        return setting

    @classmethod
    @transaction.atomic
    def bulk_update_values(
        cls,
        *,
        request,
        updates,
    ):
        updated = []

        for item in updates:
            setting = item["setting"]

            if not setting.is_editable:
                raise ValueError(
                    f"Setting {setting.key} is not editable."
                )

            setting.value = item.get(
                "value",
                setting.value,
            )
            setting.json_value = item.get(
                "json_value",
                setting.json_value,
            )
            setting.media_asset = item.get(
                "media_asset",
                setting.media_asset,
            )

            setting.full_clean()

            updated.append(setting)

        for setting in updated:
            setting.save()

        log_activity(
            request=request,
            actor=request.auth,
            action="bulk_update_settings",
            module="website_settings",
            description=(
                f"Updated {len(updated)} website settings."
            ),
            entity_type="website_settings.WebsiteSetting",
            entity_id="bulk",
        )

        return updated
