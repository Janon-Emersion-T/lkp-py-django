from typing import Any

from django.db import models, transaction
from django.forms.models import model_to_dict

from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event


class BaseService:
    @staticmethod
    def snapshot(
        instance: models.Model,
        *,
        fields: list[str] | None = None,
    ) -> dict[str, Any]:
        return model_to_dict(
            instance,
            fields=fields,
        )

    @staticmethod
    @transaction.atomic
    def create(
        *,
        request,
        model: type[models.Model],
        module: str,
        values: dict[str, Any],
        audit_fields: list[str] | None = None,
    ) -> models.Model:
        instance = model.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module=module,
            message=f"{model.__name__} created.",
            target_type=(
                f"{model._meta.app_label}."
                f"{model.__name__}"
            ),
            target_id=str(instance.pk),
            after=BaseService.snapshot(
                instance,
                fields=audit_fields,
            ),
        )

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        request,
        instance: models.Model,
        module: str,
        values: dict[str, Any],
        audit_fields: list[str] | None = None,
    ) -> models.Model:
        before = BaseService.snapshot(
            instance,
            fields=audit_fields,
        )

        for field, value in values.items():
            setattr(instance, field, value)

        if hasattr(instance, "updated_by"):
            instance.updated_by = request.auth

        instance.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module=module,
            message=(
                f"{instance.__class__.__name__} updated."
            ),
            target_type=(
                f"{instance._meta.app_label}."
                f"{instance.__class__.__name__}"
            ),
            target_id=str(instance.pk),
            before=before,
            after=BaseService.snapshot(
                instance,
                fields=audit_fields,
            ),
        )

        return instance

    @staticmethod
    @transaction.atomic
    def soft_delete(
        *,
        request,
        instance: models.Model,
        module: str,
        audit_fields: list[str] | None = None,
    ) -> None:
        before = BaseService.snapshot(
            instance,
            fields=audit_fields,
        )

        instance.delete()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module=module,
            message=(
                f"{instance.__class__.__name__} deleted."
            ),
            target_type=(
                f"{instance._meta.app_label}."
                f"{instance.__class__.__name__}"
            ),
            target_id=str(instance.pk),
            before=before,
            after={
                "is_deleted": True,
            },
        )
