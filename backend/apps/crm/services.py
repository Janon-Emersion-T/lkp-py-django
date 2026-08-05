from typing import Any

from django.db import transaction

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    Lead,
    LeadNote,
    LeadTimeline,
    LeadTimelineEvent,
)


class LeadService:
    @staticmethod
    def create_timeline(
        *,
        lead: Lead,
        event_type: str,
        description: str,
        actor=None,
        metadata: dict[str, Any] | None = None,
    ) -> LeadTimeline:
        return LeadTimeline.objects.create(
            lead=lead,
            event_type=event_type,
            description=description,
            metadata=metadata or {},
            created_by=actor,
            updated_by=actor,
        )

    @staticmethod
    @transaction.atomic
    def create_lead(
        *,
        request,
        values: dict[str, Any],
    ) -> Lead:
        lead = Lead.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        LeadService.create_timeline(
            lead=lead,
            event_type=LeadTimelineEvent.CREATED,
            description="Lead created.",
            actor=request.auth,
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="lead_created",
            module="crm",
            description="Lead created.",
            entity_type="crm.Lead",
            entity_id=str(lead.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="crm",
            message="Lead created.",
            target_type="crm.Lead",
            target_id=str(lead.pk),
            after={
                "name": lead.name,
                "company": lead.company,
                "email": lead.email,
                "source": lead.source,
                "status": lead.status,
                "assigned_to_id": lead.assigned_to_id,
            },
        )

        return lead

    @staticmethod
    @transaction.atomic
    def update_lead(
        *,
        request,
        lead: Lead,
        values: dict[str, Any],
    ) -> Lead:
        before = {
            "name": lead.name,
            "company": lead.company,
            "email": lead.email,
            "phone": lead.phone,
            "whatsapp": lead.whatsapp,
            "country": lead.country,
            "source": lead.source,
            "status": lead.status,
            "priority": lead.priority,
            "assigned_to_id": lead.assigned_to_id,
            "lead_score": lead.lead_score,
        }

        previous_status = lead.status
        previous_assignee = lead.assigned_to_id

        for field, value in values.items():
            setattr(lead, field, value)

        lead.updated_by = request.auth
        lead.save()

        if previous_status != lead.status:
            LeadService.create_timeline(
                lead=lead,
                event_type=LeadTimelineEvent.STATUS_CHANGED,
                description=(
                    f"Status changed from "
                    f"{previous_status} to {lead.status}."
                ),
                actor=request.auth,
                metadata={
                    "before": previous_status,
                    "after": lead.status,
                },
            )

        if previous_assignee != lead.assigned_to_id:
            LeadService.create_timeline(
                lead=lead,
                event_type=LeadTimelineEvent.ASSIGNED,
                description="Lead assignment changed.",
                actor=request.auth,
                metadata={
                    "before": previous_assignee,
                    "after": lead.assigned_to_id,
                },
            )

        LeadService.create_timeline(
            lead=lead,
            event_type=LeadTimelineEvent.UPDATED,
            description="Lead details updated.",
            actor=request.auth,
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="lead_updated",
            module="crm",
            description="Lead updated.",
            entity_type="crm.Lead",
            entity_id=str(lead.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="crm",
            message="Lead updated.",
            target_type="crm.Lead",
            target_id=str(lead.pk),
            before=before,
            after={
                "name": lead.name,
                "company": lead.company,
                "email": lead.email,
                "phone": lead.phone,
                "whatsapp": lead.whatsapp,
                "country": lead.country,
                "source": lead.source,
                "status": lead.status,
                "priority": lead.priority,
                "assigned_to_id": lead.assigned_to_id,
                "lead_score": lead.lead_score,
            },
        )

        return lead

    @staticmethod
    @transaction.atomic
    def add_note(
        *,
        request,
        lead: Lead,
        content: str,
        is_pinned: bool = False,
    ) -> LeadNote:
        note = LeadNote.objects.create(
            lead=lead,
            content=content,
            is_pinned=is_pinned,
            created_by=request.auth,
            updated_by=request.auth,
        )

        LeadService.create_timeline(
            lead=lead,
            event_type=LeadTimelineEvent.NOTE_ADDED,
            description="Lead note added.",
            actor=request.auth,
            metadata={
                "note_id": str(note.pk),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="lead_note_added",
            module="crm",
            description="Note added to lead.",
            entity_type="crm.Lead",
            entity_id=str(lead.pk),
        )

        return note

    @staticmethod
    @transaction.atomic
    def soft_delete_lead(
        *,
        request,
        lead: Lead,
    ) -> None:
        lead_id = str(lead.pk)

        lead.delete()

        log_activity(
            request=request,
            actor=request.auth,
            action="lead_deleted",
            module="crm",
            description="Lead soft deleted.",
            entity_type="crm.Lead",
            entity_id=lead_id,
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="crm",
            message="Lead soft deleted.",
            target_type="crm.Lead",
            target_id=lead_id,
            after={
                "is_deleted": True,
            },
        )
