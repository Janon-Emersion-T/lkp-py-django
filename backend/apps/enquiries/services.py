from django.db import transaction
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    ContactEnquiry,
    EnquiryNote,
    EnquiryStatus,
    QuoteEnquiry,
    QuoteEnquiryService,
)


class EnquiryService:
    @staticmethod
    def snapshot(enquiry):
        return {
            "id": str(enquiry.id),
            "reference_code": enquiry.reference_code,
            "name": enquiry.name,
            "email": enquiry.email,
            "phone": enquiry.phone,
            "company_name": enquiry.company_name,
            "status": enquiry.status,
            "priority": enquiry.priority,
            "source": enquiry.source,
            "assigned_to_id": (
                str(enquiry.assigned_to_id)
                if enquiry.assigned_to_id
                else None
            ),
            "client_id": (
                str(enquiry.client_id)
                if enquiry.client_id
                else None
            ),
            "lead_id": (
                str(enquiry.lead_id)
                if enquiry.lead_id
                else None
            ),
            "submitted_at": (
                enquiry.submitted_at.isoformat()
                if enquiry.submitted_at
                else None
            ),
        }

    @classmethod
    @transaction.atomic
    def create_contact_enquiry(
        cls,
        *,
        request,
        values,
    ):
        enquiry = ContactEnquiry.objects.create(
            **values,
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="enquiries",
            message="Contact enquiry created.",
            target_type="enquiries.ContactEnquiry",
            target_id=str(enquiry.pk),
            metadata={
                "after": cls.snapshot(enquiry),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="create_contact_enquiry",
            module="enquiries",
            description=(
                f"Created contact enquiry "
                f"{enquiry.reference_code}."
            ),
            entity_type="enquiries.ContactEnquiry",
            entity_id=str(enquiry.pk),
        )

        return enquiry

    @classmethod
    @transaction.atomic
    def create_quote_enquiry(
        cls,
        *,
        request,
        values,
        services,
    ):
        enquiry = QuoteEnquiry.objects.create(
            **values,
        )

        for item in services:
            QuoteEnquiryService.objects.create(
                quote_enquiry=enquiry,
                **item,
            )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="enquiries",
            message="Quote enquiry created.",
            target_type="enquiries.QuoteEnquiry",
            target_id=str(enquiry.pk),
            metadata={
                "after": cls.snapshot(enquiry),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="create_quote_enquiry",
            module="enquiries",
            description=(
                f"Created quote enquiry "
                f"{enquiry.reference_code}."
            ),
            entity_type="enquiries.QuoteEnquiry",
            entity_id=str(enquiry.pk),
        )

        return enquiry


    @classmethod
    @transaction.atomic
    def update_contact_enquiry(
        cls,
        *,
        request,
        enquiry,
        values,
    ):
        before = cls.snapshot(enquiry)

        for field, value in values.items():
            setattr(enquiry, field, value)

        enquiry.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="enquiries",
            message="Contact enquiry updated.",
            target_type="enquiries.ContactEnquiry",
            target_id=str(enquiry.pk),
            metadata={
                "before": before,
                "after": cls.snapshot(enquiry),
            },
        )

        return enquiry

    @classmethod
    @transaction.atomic
    def update_quote_enquiry(
        cls,
        *,
        request,
        enquiry,
        values,
        services,
    ):
        before = cls.snapshot(enquiry)

        for field, value in values.items():
            setattr(enquiry, field, value)

        enquiry.full_clean()
        enquiry.save()

        QuoteEnquiryService.objects.filter(
            quote_enquiry=enquiry,
        ).delete()

        for item in services:
            QuoteEnquiryService.objects.create(
                quote_enquiry=enquiry,
                **item,
            )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="enquiries",
            message="Quote enquiry updated.",
            target_type="enquiries.QuoteEnquiry",
            target_id=str(enquiry.pk),
            metadata={
                "before": before,
                "after": cls.snapshot(enquiry),
            },
        )

        return enquiry


    @classmethod
    @transaction.atomic
    def update_status(
        cls,
        *,
        request,
        enquiry,
        status,
        loss_reason="",
    ):
        before = cls.snapshot(enquiry)

        enquiry.status = status

        if status == EnquiryStatus.CONTACTED:
            enquiry.first_contacted_at = (
                enquiry.first_contacted_at
                or timezone.now()
            )

        if status in {
            EnquiryStatus.WON,
            EnquiryStatus.LOST,
            EnquiryStatus.SPAM,
            EnquiryStatus.ARCHIVED,
        }:
            enquiry.resolved_at = timezone.now()
        else:
            enquiry.resolved_at = None

        enquiry.loss_reason = (
            loss_reason
            if status == EnquiryStatus.LOST
            else ""
        )

        enquiry.save(
            update_fields=[
                "status",
                "first_contacted_at",
                "resolved_at",
                "loss_reason",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="enquiries",
            message="Enquiry status updated.",
            target_type=(
                f"enquiries.{enquiry.__class__.__name__}"
            ),
            target_id=str(enquiry.pk),
            metadata={
                "before": before,
                "after": cls.snapshot(enquiry),
            },
        )

        return enquiry

    @classmethod
    @transaction.atomic
    def assign_enquiry(
        cls,
        *,
        request,
        enquiry,
        assigned_to,
        priority,
        internal_summary,
        next_follow_up_at,
    ):
        before = cls.snapshot(enquiry)

        enquiry.assigned_to = assigned_to
        enquiry.priority = priority
        enquiry.internal_summary = internal_summary
        enquiry.next_follow_up_at = next_follow_up_at

        if (
            assigned_to
            and enquiry.status == EnquiryStatus.NEW
        ):
            enquiry.status = EnquiryStatus.ASSIGNED

        enquiry.save(
            update_fields=[
                "assigned_to",
                "priority",
                "internal_summary",
                "next_follow_up_at",
                "status",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="enquiries",
            message="Enquiry assignment updated.",
            target_type=(
                f"enquiries.{enquiry.__class__.__name__}"
            ),
            target_id=str(enquiry.pk),
            metadata={
                "before": before,
                "after": cls.snapshot(enquiry),
            },
        )

        return enquiry

    @classmethod
    @transaction.atomic
    def add_note(
        cls,
        *,
        request,
        contact_enquiry=None,
        quote_enquiry=None,
        note,
        is_private=True,
    ):
        enquiry_note = EnquiryNote(
            contact_enquiry=contact_enquiry,
            quote_enquiry=quote_enquiry,
            author=request.auth,
            note=note,
            is_private=is_private,
        )

        enquiry_note.full_clean()
        enquiry_note.save()

        enquiry = (
            contact_enquiry
            or quote_enquiry
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="add_enquiry_note",
            module="enquiries",
            description=(
                f"Added a note to enquiry "
                f"{enquiry.reference_code}."
            ),
            entity_type=(
                f"enquiries.{enquiry.__class__.__name__}"
            ),
            entity_id=str(enquiry.pk),
        )

        return enquiry_note


    @classmethod
    @transaction.atomic
    def complete_follow_up(
        cls,
        *,
        request,
        enquiry,
        next_follow_up_at=None,
    ):
        before = cls.snapshot(enquiry)

        enquiry.last_follow_up_at = timezone.now()
        enquiry.next_follow_up_at = next_follow_up_at

        enquiry.save(
            update_fields=[
                "last_follow_up_at",
                "next_follow_up_at",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="enquiries",
            message="Enquiry follow-up completed.",
            target_type=(
                f"enquiries.{enquiry.__class__.__name__}"
            ),
            target_id=str(enquiry.pk),
            metadata={
                "before": before,
                "after": cls.snapshot(enquiry),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="complete_follow_up",
            module="enquiries",
            description=(
                f"Completed follow-up for enquiry "
                f"{enquiry.reference_code}."
            ),
            entity_type=(
                f"enquiries.{enquiry.__class__.__name__}"
            ),
            entity_id=str(enquiry.pk),
        )

        return enquiry
