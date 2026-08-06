from django.db import transaction
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    ApplicationAnswer,
    ApplicationEvaluation,
    ApplicationNote,
    Interview,
    InterviewParticipant,
    InterviewStatus,
    JobApplication,
    JobApplicationStatus,
    JobListingStatus,
)


class JobListingService:
    @staticmethod
    def audit_snapshot(listing):
        return {
            "id": str(listing.id),
            "position_id": str(listing.position_id),
            "reference_code": listing.reference_code,
            "status": listing.status,
            "number_of_openings": (
                listing.number_of_openings
            ),
            "application_deadline": (
                listing.application_deadline.isoformat()
                if listing.application_deadline
                else None
            ),
            "published_at": (
                listing.published_at.isoformat()
                if listing.published_at
                else None
            ),
            "scheduled_for": (
                listing.scheduled_for.isoformat()
                if listing.scheduled_for
                else None
            ),
            "is_featured": listing.is_featured,
            "is_active": listing.is_active,
            "sort_order": listing.sort_order,
        }

    @classmethod
    @transaction.atomic
    def publish_listing(
        cls,
        *,
        request,
        listing,
    ):
        before = cls.audit_snapshot(listing)

        listing.status = JobListingStatus.PUBLISHED
        listing.published_at = timezone.now()
        listing.scheduled_for = None
        listing.save(
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
            module="careers",
            message="Job listing published.",
            target_type="careers.JobListing",
            target_id=str(listing.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(listing),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="publish",
            module="careers",
            description=(
                f"Published job listing "
                f"{listing.reference_code}."
            ),
            entity_type="careers.JobListing",
            entity_id=str(listing.pk),
        )

        return listing

    @classmethod
    @transaction.atomic
    def schedule_listing(
        cls,
        *,
        request,
        listing,
        scheduled_for,
    ):
        if scheduled_for <= timezone.now():
            raise ValueError(
                "Scheduled publication must be in the future."
            )

        before = cls.audit_snapshot(listing)

        listing.status = JobListingStatus.SCHEDULED
        listing.scheduled_for = scheduled_for
        listing.published_at = None
        listing.save(
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
            module="careers",
            message="Job listing scheduled.",
            target_type="careers.JobListing",
            target_id=str(listing.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(listing),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="schedule",
            module="careers",
            description=(
                f"Scheduled job listing "
                f"{listing.reference_code}."
            ),
            entity_type="careers.JobListing",
            entity_id=str(listing.pk),
        )

        return listing



    @classmethod
    @transaction.atomic
    def close_listing(
        cls,
        *,
        request,
        listing,
    ):
        before = cls.audit_snapshot(listing)

        listing.status = JobListingStatus.CLOSED
        listing.scheduled_for = None
        listing.save(
            update_fields=[
                "status",
                "scheduled_for",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="careers",
            message="Job listing closed.",
            target_type="careers.JobListing",
            target_id=str(listing.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(listing),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="close_listing",
            module="careers",
            description=(
                f"Closed job listing "
                f"{listing.reference_code}."
            ),
            entity_type="careers.JobListing",
            entity_id=str(listing.pk),
        )

        return listing

    @classmethod
    @transaction.atomic
    def archive_listing(
        cls,
        *,
        request,
        listing,
    ):
        before = cls.audit_snapshot(listing)

        listing.status = JobListingStatus.ARCHIVED
        listing.is_active = False
        listing.scheduled_for = None
        listing.save(
            update_fields=[
                "status",
                "is_active",
                "scheduled_for",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="careers",
            message="Job listing archived.",
            target_type="careers.JobListing",
            target_id=str(listing.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(listing),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="archive_listing",
            module="careers",
            description=(
                f"Archived job listing "
                f"{listing.reference_code}."
            ),
            entity_type="careers.JobListing",
            entity_id=str(listing.pk),
        )

        return listing


class JobApplicationService:
    @staticmethod
    def audit_snapshot(application):
        return {
            "id": str(application.id),
            "listing_id": str(application.listing_id),
            "applicant_name": application.applicant_name,
            "email": application.email,
            "phone": application.phone,
            "status": application.status,
            "source": application.source,
            "assigned_to_id": (
                str(application.assigned_to_id)
                if application.assigned_to_id
                else None
            ),
            "rating": application.rating,
            "submitted_at": (
                application.submitted_at.isoformat()
                if application.submitted_at
                else None
            ),
            "reviewed_at": (
                application.reviewed_at.isoformat()
                if application.reviewed_at
                else None
            ),
        }

    @classmethod
    @transaction.atomic
    def create_application(
        cls,
        *,
        request,
        values,
        answers,
    ):
        application = JobApplication.objects.create(
            **values,
        )

        for answer in answers:
            ApplicationAnswer.objects.create(
                application=application,
                question=answer["question"],
                answer=answer["answer"],
            )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="careers",
            message="Job application created.",
            target_type="careers.JobApplication",
            target_id=str(application.pk),
            metadata={
                "after": cls.audit_snapshot(application),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="create",
            module="careers",
            description=(
                f"Created application for "
                f"{application.applicant_name}."
            ),
            entity_type="careers.JobApplication",
            entity_id=str(application.pk),
        )

        return application

    @classmethod
    @transaction.atomic
    def update_status(
        cls,
        *,
        request,
        application,
        status,
        rejection_reason="",
    ):
        before = cls.audit_snapshot(application)

        application.status = status

        if status != JobApplicationStatus.REJECTED:
            application.rejection_reason = ""
        else:
            application.rejection_reason = (
                rejection_reason
            )

        if status != JobApplicationStatus.NEW:
            application.reviewed_at = (
                application.reviewed_at
                or timezone.now()
            )

        application.save(
            update_fields=[
                "status",
                "rejection_reason",
                "reviewed_at",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="careers",
            message="Job application status updated.",
            target_type="careers.JobApplication",
            target_id=str(application.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(application),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="status_change",
            module="careers",
            description=(
                f"Changed {application.applicant_name}'s "
                f"application status to {status}."
            ),
            entity_type="careers.JobApplication",
            entity_id=str(application.pk),
        )

        return application

    @classmethod
    @transaction.atomic
    def add_note(
        cls,
        *,
        request,
        application,
        note,
        is_private=True,
    ):
        application_note = ApplicationNote.objects.create(
            application=application,
            author=request.auth,
            note=note,
            is_private=is_private,
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="careers",
            message="Job application note created.",
            target_type="careers.ApplicationNote",
            target_id=str(application_note.pk),
            metadata={
                "application_id": str(application.pk),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="add_note",
            module="careers",
            description=(
                f"Added a note to "
                f"{application.applicant_name}'s application."
            ),
            entity_type="careers.JobApplication",
            entity_id=str(application.pk),
        )

        return application_note



    @classmethod
    @transaction.atomic
    def review_application(
        cls,
        *,
        request,
        application,
        assigned_to,
        rating,
        internal_summary,
    ):
        if rating is not None and not 1 <= rating <= 5:
            raise ValueError(
                "Application rating must be between 1 and 5."
            )

        before = cls.audit_snapshot(application)

        application.assigned_to = assigned_to
        application.rating = rating
        application.internal_summary = internal_summary
        application.reviewed_at = (
            application.reviewed_at
            or timezone.now()
        )

        application.save(
            update_fields=[
                "assigned_to",
                "rating",
                "internal_summary",
                "reviewed_at",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="careers",
            message="Job application review updated.",
            target_type="careers.JobApplication",
            target_id=str(application.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(application),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="review_application",
            module="careers",
            description=(
                f"Reviewed application from "
                f"{application.applicant_name}."
            ),
            entity_type="careers.JobApplication",
            entity_id=str(application.pk),
        )

        return application


class InterviewService:
    @staticmethod
    def audit_snapshot(interview):
        return {
            "id": str(interview.id),
            "application_id": str(
                interview.application_id
            ),
            "title": interview.title,
            "interview_type": interview.interview_type,
            "status": interview.status,
            "scheduled_start": (
                interview.scheduled_start.isoformat()
            ),
            "scheduled_end": (
                interview.scheduled_end.isoformat()
            ),
            "timezone_name": interview.timezone_name,
            "location": interview.location,
            "meeting_url": interview.meeting_url,
            "organizer_id": (
                str(interview.organizer_id)
                if interview.organizer_id
                else None
            ),
        }

    @classmethod
    @transaction.atomic
    def create_interview(
        cls,
        *,
        request,
        values,
        participants,
    ):
        interview = Interview.objects.create(**values)

        for participant in participants:
            InterviewParticipant.objects.create(
                interview=interview,
                user=participant["user"],
                is_lead=participant.get(
                    "is_lead",
                    False,
                ),
            )

        application = interview.application

        if application.status in {
            JobApplicationStatus.NEW,
            JobApplicationStatus.SCREENING,
            JobApplicationStatus.SHORTLISTED,
        }:
            application.status = (
                JobApplicationStatus.INTERVIEW
            )
            application.reviewed_at = (
                application.reviewed_at
                or timezone.now()
            )
            application.save(
                update_fields=[
                    "status",
                    "reviewed_at",
                    "updated_at",
                ]
            )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="careers",
            message="Interview scheduled.",
            target_type="careers.Interview",
            target_id=str(interview.pk),
            metadata={
                "after": cls.audit_snapshot(interview),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="schedule_interview",
            module="careers",
            description=(
                f"Scheduled interview for "
                f"{application.applicant_name}."
            ),
            entity_type="careers.Interview",
            entity_id=str(interview.pk),
        )

        return interview

    @classmethod
    @transaction.atomic
    def update_status(
        cls,
        *,
        request,
        interview,
        status,
        cancellation_reason="",
    ):
        before = cls.audit_snapshot(interview)

        interview.status = status

        if status == InterviewStatus.CANCELLED:
            interview.cancellation_reason = (
                cancellation_reason
            )
        else:
            interview.cancellation_reason = ""

        if status == InterviewStatus.COMPLETED:
            interview.completed_at = timezone.now()
        else:
            interview.completed_at = None

        interview.save(
            update_fields=[
                "status",
                "cancellation_reason",
                "completed_at",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="careers",
            message="Interview status updated.",
            target_type="careers.Interview",
            target_id=str(interview.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(interview),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="interview_status_change",
            module="careers",
            description=(
                f"Changed interview status to {status}."
            ),
            entity_type="careers.Interview",
            entity_id=str(interview.pk),
        )

        return interview


class ApplicationEvaluationService:
    @classmethod
    @transaction.atomic
    def create_evaluation(
        cls,
        *,
        request,
        values,
    ):
        evaluation = (
            ApplicationEvaluation.objects.create(
                **values,
            )
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="careers",
            message="Candidate evaluation created.",
            target_type=(
                "careers.ApplicationEvaluation"
            ),
            target_id=str(evaluation.pk),
            metadata={
                "application_id": str(
                    evaluation.application_id
                ),
                "recommendation": (
                    evaluation.recommendation
                ),
                "overall_score": (
                    evaluation.overall_score
                ),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="evaluate_candidate",
            module="careers",
            description=(
                f"Evaluated candidate "
                f"{evaluation.application.applicant_name}."
            ),
            entity_type=(
                "careers.ApplicationEvaluation"
            ),
            entity_id=str(evaluation.pk),
        )

        return evaluation
