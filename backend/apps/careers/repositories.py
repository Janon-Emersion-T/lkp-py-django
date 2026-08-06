from django.db.models import Count, Q
from django.utils import timezone

from .models import (
    ApplicationEvaluation,
    ApplicationNote,
    ApplicationQuestion,
    EmploymentType,
    Interview,
    JobApplication,
    JobDepartment,
    JobListing,
    JobListingStatus,
    JobPosition,
)


class JobDepartmentRepository:
    @staticmethod
    def queryset():
        return JobDepartment.objects.all()

    @classmethod
    def find_by_id(cls, department_id):
        return cls.queryset().filter(
            pk=department_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        is_active=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        return queryset


class EmploymentTypeRepository:
    @staticmethod
    def queryset():
        return EmploymentType.objects.all()

    @classmethod
    def find_by_id(cls, employment_type_id):
        return cls.queryset().filter(
            pk=employment_type_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        is_active=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(code__icontains=search)
                | Q(description__icontains=search)
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        return queryset


class JobPositionRepository:
    ALLOWED_ORDERING_FIELDS = {
        "title",
        "sort_order",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return JobPosition.objects.select_related(
            "department",
            "employment_type",
        )

    @classmethod
    def find_by_id(cls, position_id):
        return cls.queryset().filter(
            pk=position_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        department_id=None,
        employment_type_id=None,
        experience_level=None,
        remote_policy=None,
        is_active=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(summary__icontains=search)
                | Q(location__icontains=search)
            )

        if department_id:
            queryset = queryset.filter(
                department_id=department_id,
            )

        if employment_type_id:
            queryset = queryset.filter(
                employment_type_id=employment_type_id,
            )

        if experience_level:
            queryset = queryset.filter(
                experience_level=experience_level,
            )

        if remote_policy:
            queryset = queryset.filter(
                remote_policy=remote_policy,
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset


class JobListingRepository:
    ALLOWED_ORDERING_FIELDS = {
        "reference_code",
        "application_deadline",
        "published_at",
        "sort_order",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return JobListing.objects.select_related(
            "position",
            "position__department",
            "position__employment_type",
        )

    @classmethod
    def find_by_id(cls, listing_id):
        return cls.queryset().filter(
            pk=listing_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        status=None,
        department_id=None,
        employment_type_id=None,
        is_featured=None,
        is_active=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(reference_code__icontains=search)
                | Q(position__title__icontains=search)
                | Q(position__summary__icontains=search)
                | Q(position__location__icontains=search)
            )

        if status:
            queryset = queryset.filter(status=status)

        if department_id:
            queryset = queryset.filter(
                position__department_id=department_id,
            )

        if employment_type_id:
            queryset = queryset.filter(
                position__employment_type_id=(
                    employment_type_id
                ),
            )

        if is_featured is not None:
            queryset = queryset.filter(
                is_featured=is_featured,
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset

    @classmethod
    def public_queryset(cls):
        now = timezone.now()

        return cls.queryset().filter(
            status=JobListingStatus.PUBLISHED,
            is_active=True,
            position__is_active=True,
            position__department__is_active=True,
            position__employment_type__is_active=True,
            published_at__isnull=False,
            published_at__lte=now,
        ).filter(
            Q(application_deadline__isnull=True)
            | Q(application_deadline__gte=now)
        )



class ApplicationQuestionRepository:
    @staticmethod
    def queryset():
        return ApplicationQuestion.objects.select_related(
            "listing",
            "listing__position",
        )

    @classmethod
    def find_by_id(cls, question_id):
        return cls.queryset().filter(
            pk=question_id,
        ).first()

    @classmethod
    def for_listing(
        cls,
        listing_id,
        *,
        is_active=None,
    ):
        queryset = cls.queryset().filter(
            listing_id=listing_id,
        )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        return queryset


class JobApplicationRepository:
    ALLOWED_ORDERING_FIELDS = {
        "applicant_name",
        "email",
        "status",
        "submitted_at",
        "reviewed_at",
        "rating",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return JobApplication.objects.select_related(
            "listing",
            "listing__position",
            "listing__position__department",
            "listing__position__employment_type",
            "resume_asset",
            "assigned_to",
        ).prefetch_related(
            "answers",
            "answers__question",
            "notes",
            "notes__author",
        )

    @classmethod
    def find_by_id(cls, application_id):
        return cls.queryset().filter(
            pk=application_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        listing_id=None,
        status=None,
        source=None,
        assigned_to_id=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(applicant_name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
                | Q(current_company__icontains=search)
                | Q(current_position__icontains=search)
                | Q(
                    listing__position__title__icontains=(
                        search
                    )
                )
            )

        if listing_id:
            queryset = queryset.filter(
                listing_id=listing_id,
            )

        if status:
            queryset = queryset.filter(
                status=status,
            )

        if source:
            queryset = queryset.filter(
                source=source,
            )

        if assigned_to_id:
            queryset = queryset.filter(
                assigned_to_id=assigned_to_id,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset


class ApplicationNoteRepository:
    @staticmethod
    def for_application(application_id):
        return ApplicationNote.objects.select_related(
            "author",
        ).filter(
            application_id=application_id,
        )



class InterviewRepository:
    ALLOWED_ORDERING_FIELDS = {
        "scheduled_start",
        "scheduled_end",
        "status",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return Interview.objects.select_related(
            "application",
            "application__listing",
            "application__listing__position",
            "organizer",
        ).prefetch_related(
            "participants",
            "participants__user",
        )

    @classmethod
    def find_by_id(cls, interview_id):
        return cls.queryset().filter(
            pk=interview_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        application_id=None,
        status=None,
        interview_type=None,
        organizer_id=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if application_id:
            queryset = queryset.filter(
                application_id=application_id,
            )

        if status:
            queryset = queryset.filter(
                status=status,
            )

        if interview_type:
            queryset = queryset.filter(
                interview_type=interview_type,
            )

        if organizer_id:
            queryset = queryset.filter(
                organizer_id=organizer_id,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset


class ApplicationEvaluationRepository:
    @staticmethod
    def queryset():
        return ApplicationEvaluation.objects.select_related(
            "application",
            "application__listing",
            "application__listing__position",
            "interview",
            "evaluator",
        )

    @classmethod
    def find_by_id(cls, evaluation_id):
        return cls.queryset().filter(
            pk=evaluation_id,
        ).first()

    @classmethod
    def for_application(cls, application_id):
        return cls.queryset().filter(
            application_id=application_id,
        )



class CareersDashboardRepository:
    @staticmethod
    def statistics():
        now = timezone.now()

        listing_queryset = JobListing.objects.filter(
            is_active=True,
        )

        application_queryset = JobApplication.objects.all()

        interview_queryset = Interview.objects.all()

        applications_by_status = {
            item["status"]: item["total"]
            for item in (
                application_queryset.values(
                    "status"
                ).annotate(
                    total=Count("id")
                )
            )
        }

        applications_by_source = {
            item["source"]: item["total"]
            for item in (
                application_queryset.values(
                    "source"
                ).annotate(
                    total=Count("id")
                )
            )
        }

        return {
            "open_listings": listing_queryset.filter(
                status=JobListingStatus.PUBLISHED,
            ).filter(
                Q(application_deadline__isnull=True)
                | Q(application_deadline__gte=now)
            ).count(),
            "featured_listings": (
                listing_queryset.filter(
                    status=JobListingStatus.PUBLISHED,
                    is_featured=True,
                ).count()
            ),
            "total_applications": (
                application_queryset.count()
            ),
            "new_applications": (
                application_queryset.filter(
                    status="new",
                ).count()
            ),
            "screening_applications": (
                application_queryset.filter(
                    status="screening",
                ).count()
            ),
            "shortlisted_applications": (
                application_queryset.filter(
                    status="shortlisted",
                ).count()
            ),
            "interview_applications": (
                application_queryset.filter(
                    status="interview",
                ).count()
            ),
            "offered_applications": (
                application_queryset.filter(
                    status="offered",
                ).count()
            ),
            "hired_applications": (
                application_queryset.filter(
                    status="hired",
                ).count()
            ),
            "rejected_applications": (
                application_queryset.filter(
                    status="rejected",
                ).count()
            ),
            "upcoming_interviews": (
                interview_queryset.filter(
                    scheduled_start__gte=now,
                    status__in=[
                        "scheduled",
                        "confirmed",
                        "rescheduled",
                    ],
                ).count()
            ),
            "completed_interviews": (
                interview_queryset.filter(
                    status="completed",
                ).count()
            ),
            "applications_by_status": (
                applications_by_status
            ),
            "applications_by_source": (
                applications_by_source
            ),
        }
