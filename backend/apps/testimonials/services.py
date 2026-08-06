from django.db import transaction
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import TestimonialStatus
from .repositories import TestimonialRepository


class TestimonialService:
    @staticmethod
    def audit_snapshot(testimonial):
        return {
            "id": str(testimonial.id),
            "client_id": (
                str(testimonial.client_id)
                if testimonial.client_id
                else None
            ),
            "project_id": (
                str(testimonial.project_id)
                if testimonial.project_id
                else None
            ),
            "author_name": testimonial.author_name,
            "author_position": testimonial.author_position,
            "company_name": testimonial.company_name,
            "content": testimonial.content,
            "short_content": testimonial.short_content,
            "rating": testimonial.rating,
            "source": testimonial.source,
            "source_url": testimonial.source_url,
            "status": testimonial.status,
            "published_at": (
                testimonial.published_at.isoformat()
                if testimonial.published_at
                else None
            ),
            "scheduled_for": (
                testimonial.scheduled_for.isoformat()
                if testimonial.scheduled_for
                else None
            ),
            "is_featured": testimonial.is_featured,
            "is_verified": testimonial.is_verified,
            "is_active": testimonial.is_active,
            "sort_order": testimonial.sort_order,
        }

    @classmethod
    @transaction.atomic
    def create_testimonial(cls, *, request, values):
        testimonial = TestimonialRepository.create(**values)

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="testimonials",
            message="Testimonial created.",
            target_type="testimonials.Testimonial",
            target_id=str(testimonial.pk),
            metadata={
                "after": cls.audit_snapshot(testimonial),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="create",
            module="testimonials",
            description=(
                f"Created testimonial from "
                f"{testimonial.author_name}."
            ),
            entity_type="testimonials.Testimonial",
            entity_id=str(testimonial.pk),
        )

        return testimonial

    @classmethod
    @transaction.atomic
    def update_testimonial(
        cls,
        *,
        request,
        testimonial,
        values,
    ):
        before = cls.audit_snapshot(testimonial)

        testimonial = TestimonialRepository.update(
            testimonial,
            **values,
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="testimonials",
            message="Testimonial updated.",
            target_type="testimonials.Testimonial",
            target_id=str(testimonial.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(testimonial),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="update",
            module="testimonials",
            description=(
                f"Updated testimonial from "
                f"{testimonial.author_name}."
            ),
            entity_type="testimonials.Testimonial",
            entity_id=str(testimonial.pk),
        )

        return testimonial

    @classmethod
    @transaction.atomic
    def publish_testimonial(
        cls,
        *,
        request,
        testimonial,
    ):
        before = cls.audit_snapshot(testimonial)

        testimonial.status = TestimonialStatus.PUBLISHED
        testimonial.published_at = timezone.now()
        testimonial.scheduled_for = None
        testimonial.save(
            update_fields=[
                "status",
                "published_at",
                "scheduled_for",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="testimonials",
            message="Testimonial published.",
            target_type="testimonials.Testimonial",
            target_id=str(testimonial.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(testimonial),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="publish",
            module="testimonials",
            description=(
                f"Published testimonial from "
                f"{testimonial.author_name}."
            ),
            entity_type="testimonials.Testimonial",
            entity_id=str(testimonial.pk),
        )

        return testimonial

    @classmethod
    @transaction.atomic
    def schedule_testimonial(
        cls,
        *,
        request,
        testimonial,
        scheduled_for,
    ):
        if scheduled_for <= timezone.now():
            raise ValueError(
                "Scheduled publication must be in the future."
            )

        before = cls.audit_snapshot(testimonial)

        testimonial.status = TestimonialStatus.SCHEDULED
        testimonial.scheduled_for = scheduled_for
        testimonial.published_at = None
        testimonial.save(
            update_fields=[
                "status",
                "scheduled_for",
                "published_at",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="testimonials",
            message="Testimonial scheduled.",
            target_type="testimonials.Testimonial",
            target_id=str(testimonial.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(testimonial),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="schedule",
            module="testimonials",
            description=(
                f"Scheduled testimonial from "
                f"{testimonial.author_name}."
            ),
            entity_type="testimonials.Testimonial",
            entity_id=str(testimonial.pk),
        )

        return testimonial

    @classmethod
    @transaction.atomic
    def soft_delete(
        cls,
        *,
        request,
        testimonial,
    ):
        snapshot = cls.audit_snapshot(testimonial)

        TestimonialRepository.soft_delete(testimonial)

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="testimonials",
            message="Testimonial deleted.",
            target_type="testimonials.Testimonial",
            target_id=str(testimonial.pk),
            metadata={
                "before": snapshot,
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="delete",
            module="testimonials",
            description=(
                f"Deleted testimonial from "
                f"{testimonial.author_name}."
            ),
            entity_type="testimonials.Testimonial",
            entity_id=str(testimonial.pk),
        )
