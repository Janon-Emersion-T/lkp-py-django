from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import User

from .models import (
    EmploymentType,
    ExperienceLevel,
    JobDepartment,
    JobListing,
    JobListingStatus,
    JobPosition,
    RemotePolicy,
)
from .repositories import (
    JobDepartmentRepository,
    JobListingRepository,
    JobPositionRepository,
)
from .services import JobListingService


class RequestStub:
    def __init__(self, user):
        self.auth = user
        self.user = user
        self.META = {}
        self.headers = {}


class CareersFixtureMixin:
    def create_foundation(self):
        department = JobDepartment.objects.create(
            name="Engineering",
            slug="engineering",
            description="Software engineering department.",
        )

        employment_type = EmploymentType.objects.create(
            name="Full Time",
            code="full-time",
        )

        position = JobPosition.objects.create(
            department=department,
            employment_type=employment_type,
            title="Backend Developer",
            slug="backend-developer",
            summary="Develop enterprise backend systems.",
            location="Jaffna",
            remote_policy=RemotePolicy.HYBRID,
            experience_level=ExperienceLevel.MID,
            salary_min=Decimal("100000.00"),
            salary_max=Decimal("180000.00"),
        )

        return department, employment_type, position


class CareersModelTests(
    CareersFixtureMixin,
    TestCase,
):
    def test_department_and_employment_type(self):
        department, employment_type, _ = (
            self.create_foundation()
        )

        self.assertEqual(
            str(department),
            "Engineering",
        )
        self.assertEqual(
            str(employment_type),
            "Full Time",
        )

    def test_position_uses_title(self):
        _, _, position = self.create_foundation()

        self.assertEqual(
            position.title,
            "Backend Developer",
        )
        self.assertEqual(
            str(position),
            "Backend Developer",
        )

    def test_position_rejects_invalid_salary_range(self):
        department, employment_type, _ = (
            self.create_foundation()
        )

        position = JobPosition(
            department=department,
            employment_type=employment_type,
            title="Invalid Salary Position",
            slug="invalid-salary-position",
            salary_min=Decimal("200000.00"),
            salary_max=Decimal("100000.00"),
        )

        with self.assertRaises(ValidationError):
            position.full_clean()

    def test_published_listing_is_public(self):
        _, _, position = self.create_foundation()

        listing = JobListing.objects.create(
            position=position,
            reference_code="LKP-CAREER-001",
            status=JobListingStatus.PUBLISHED,
            published_at=timezone.now(),
        )

        self.assertTrue(
            listing.is_publicly_available
        )

    def test_expired_listing_is_not_public(self):
        _, _, position = self.create_foundation()

        listing = JobListing.objects.create(
            position=position,
            reference_code="LKP-CAREER-002",
            status=JobListingStatus.PUBLISHED,
            published_at=timezone.now(),
            application_deadline=(
                timezone.now() - timedelta(minutes=1)
            ),
        )

        self.assertFalse(
            listing.is_publicly_available
        )


class CareersRepositoryTests(
    CareersFixtureMixin,
    TestCase,
):
    def setUp(self):
        (
            self.department,
            self.employment_type,
            self.position,
        ) = self.create_foundation()

        self.listing = JobListing.objects.create(
            position=self.position,
            reference_code="LKP-CAREER-003",
            status=JobListingStatus.PUBLISHED,
            published_at=timezone.now(),
            is_featured=True,
        )

    def test_search_department(self):
        queryset = JobDepartmentRepository.search(
            search="Engineer"
        )

        self.assertEqual(queryset.count(), 1)

    def test_search_position_by_department(self):
        queryset = JobPositionRepository.search(
            department_id=self.department.id,
            remote_policy=RemotePolicy.HYBRID,
        )

        self.assertEqual(queryset.count(), 1)

    def test_public_listing_queryset(self):
        queryset = (
            JobListingRepository.public_queryset()
        )

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(
            queryset.first().reference_code,
            "LKP-CAREER-003",
        )


class JobListingServiceTests(
    CareersFixtureMixin,
    TestCase,
):
    def setUp(self):
        self.user = User.objects.create_user(
            username="careers_admin",
            email="careers@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.user)

        _, _, position = self.create_foundation()

        self.listing = JobListing.objects.create(
            position=position,
            reference_code="LKP-CAREER-004",
        )

    def test_publish_listing(self):
        listing = JobListingService.publish_listing(
            request=self.request,
            listing=self.listing,
        )

        self.assertEqual(
            listing.status,
            JobListingStatus.PUBLISHED,
        )
        self.assertIsNotNone(listing.published_at)
        self.assertIsNone(listing.scheduled_for)

    def test_schedule_listing(self):
        scheduled_for = (
            timezone.now() + timedelta(days=2)
        )

        listing = JobListingService.schedule_listing(
            request=self.request,
            listing=self.listing,
            scheduled_for=scheduled_for,
        )

        self.assertEqual(
            listing.status,
            JobListingStatus.SCHEDULED,
        )
        self.assertEqual(
            listing.scheduled_for,
            scheduled_for,
        )

    def test_schedule_rejects_past_datetime(self):
        with self.assertRaises(ValueError):
            JobListingService.schedule_listing(
                request=self.request,
                listing=self.listing,
                scheduled_for=(
                    timezone.now()
                    - timedelta(minutes=1)
                ),
            )



from .models import (
    ApplicationAnswer,
    ApplicationNote,
    ApplicationQuestion,
    ApplicationQuestionType,
    JobApplication,
    JobApplicationSource,
    JobApplicationStatus,
)
from .repositories import JobApplicationRepository
from .services import JobApplicationService


class JobApplicationWorkflowTests(
    CareersFixtureMixin,
    TestCase,
):
    def setUp(self):
        self.user = User.objects.create_user(
            username="recruitment_admin",
            email="recruitment@example.com",
            password="StrongPassword123!",
        )
        self.request = RequestStub(self.user)

        _, _, position = self.create_foundation()

        self.listing = JobListing.objects.create(
            position=position,
            reference_code="LKP-CAREER-100",
            status=JobListingStatus.PUBLISHED,
            published_at=timezone.now(),
        )

        self.question = (
            ApplicationQuestion.objects.create(
                listing=self.listing,
                question=(
                    "Why are you interested in this role?"
                ),
                question_type=(
                    ApplicationQuestionType.LONG_TEXT
                ),
                is_required=True,
            )
        )

    def create_application(self):
        return JobApplicationService.create_application(
            request=self.request,
            values={
                "listing": self.listing,
                "applicant_name": "Example Applicant",
                "email": "applicant@example.com",
                "phone": "+94770000000",
                "source": (
                    JobApplicationSource.CAREERS_PAGE
                ),
                "consent_to_process": True,
            },
            answers=[
                {
                    "question": self.question,
                    "answer": {
                        "value": (
                            "The role matches my experience."
                        ),
                    },
                },
            ],
        )

    def test_create_application_with_answer(self):
        application = self.create_application()

        self.assertEqual(
            application.status,
            JobApplicationStatus.NEW,
        )
        self.assertEqual(
            application.answers.count(),
            1,
        )
        self.assertEqual(
            application.answers.first().question,
            self.question,
        )

    def test_application_string_uses_position_title(self):
        application = self.create_application()

        self.assertIn(
            "Backend Developer",
            str(application),
        )

    def test_application_repository_search(self):
        application = self.create_application()

        queryset = JobApplicationRepository.search(
            search="Example Applicant",
            listing_id=self.listing.id,
            status=JobApplicationStatus.NEW,
        )

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(
            queryset.first().id,
            application.id,
        )

    def test_update_application_status(self):
        application = self.create_application()

        application = (
            JobApplicationService.update_status(
                request=self.request,
                application=application,
                status=(
                    JobApplicationStatus.SHORTLISTED
                ),
            )
        )

        self.assertEqual(
            application.status,
            JobApplicationStatus.SHORTLISTED,
        )
        self.assertIsNotNone(
            application.reviewed_at,
        )

    def test_rejected_application_records_reason(self):
        application = self.create_application()

        application = (
            JobApplicationService.update_status(
                request=self.request,
                application=application,
                status=JobApplicationStatus.REJECTED,
                rejection_reason=(
                    "Required experience was not met."
                ),
            )
        )

        self.assertEqual(
            application.status,
            JobApplicationStatus.REJECTED,
        )
        self.assertEqual(
            application.rejection_reason,
            "Required experience was not met.",
        )

    def test_non_rejected_status_clears_reason(self):
        application = self.create_application()
        application.status = (
            JobApplicationStatus.REJECTED
        )
        application.rejection_reason = "Previous reason"
        application.save()

        application = (
            JobApplicationService.update_status(
                request=self.request,
                application=application,
                status=(
                    JobApplicationStatus.SCREENING
                ),
            )
        )

        self.assertEqual(
            application.rejection_reason,
            "",
        )

    def test_add_application_note(self):
        application = self.create_application()

        note = JobApplicationService.add_note(
            request=self.request,
            application=application,
            note="Strong backend experience.",
        )

        self.assertEqual(
            note.author,
            self.user,
        )
        self.assertTrue(note.is_private)
        self.assertEqual(
            ApplicationNote.objects.filter(
                application=application,
            ).count(),
            1,
        )

    def test_duplicate_application_is_constrained(self):
        self.create_application()

        with self.assertRaises(Exception):
            JobApplication.objects.create(
                listing=self.listing,
                applicant_name="Duplicate Applicant",
                email="applicant@example.com",
            )

    def test_answer_is_linked_to_application(self):
        application = self.create_application()

        answer = ApplicationAnswer.objects.get(
            application=application,
            question=self.question,
        )

        self.assertEqual(
            answer.answer["value"],
            "The role matches my experience.",
        )



from .models import (
    ApplicationEvaluation,
    EvaluationRecommendation,
    Interview,
    InterviewParticipant,
    InterviewStatus,
    InterviewType,
)
from .repositories import (
    ApplicationEvaluationRepository,
    InterviewRepository,
)
from .services import (
    ApplicationEvaluationService,
    InterviewService,
)


class InterviewAndEvaluationTests(
    CareersFixtureMixin,
    TestCase,
):
    def setUp(self):
        self.organizer = User.objects.create_user(
            username="interview_organizer",
            email="organizer@example.com",
            password="StrongPassword123!",
        )

        self.interviewer = User.objects.create_user(
            username="technical_interviewer",
            email="interviewer@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.organizer)

        _, _, position = self.create_foundation()

        self.listing = JobListing.objects.create(
            position=position,
            reference_code="LKP-CAREER-200",
            status=JobListingStatus.PUBLISHED,
            published_at=timezone.now(),
        )

        self.application = JobApplication.objects.create(
            listing=self.listing,
            applicant_name="Interview Candidate",
            email="candidate@example.com",
            consent_to_process=True,
        )

        self.start = (
            timezone.now() + timedelta(days=1)
        )

        self.end = (
            self.start + timedelta(hours=1)
        )

    def create_interview(self):
        return InterviewService.create_interview(
            request=self.request,
            values={
                "application": self.application,
                "title": "Technical Interview",
                "interview_type": (
                    InterviewType.TECHNICAL
                ),
                "scheduled_start": self.start,
                "scheduled_end": self.end,
                "organizer": self.organizer,
            },
            participants=[
                {
                    "user": self.interviewer,
                    "is_lead": True,
                },
            ],
        )

    def test_interview_rejects_invalid_time_range(self):
        interview = Interview(
            application=self.application,
            scheduled_start=self.end,
            scheduled_end=self.start,
        )

        with self.assertRaises(ValidationError):
            interview.full_clean()

    def test_create_interview_with_participant(self):
        interview = self.create_interview()

        self.assertEqual(
            interview.participants.count(),
            1,
        )

        participant = (
            interview.participants.first()
        )

        self.assertEqual(
            participant.user,
            self.interviewer,
        )
        self.assertTrue(participant.is_lead)

    def test_interview_moves_application_to_interview(self):
        self.create_interview()

        self.application.refresh_from_db()

        self.assertEqual(
            self.application.status,
            JobApplicationStatus.INTERVIEW,
        )
        self.assertIsNotNone(
            self.application.reviewed_at,
        )

    def test_interview_repository_search(self):
        interview = self.create_interview()

        queryset = InterviewRepository.search(
            application_id=self.application.id,
            status=InterviewStatus.SCHEDULED,
            interview_type=InterviewType.TECHNICAL,
        )

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(
            queryset.first().id,
            interview.id,
        )

    def test_complete_interview(self):
        interview = self.create_interview()

        interview = InterviewService.update_status(
            request=self.request,
            interview=interview,
            status=InterviewStatus.COMPLETED,
        )

        self.assertEqual(
            interview.status,
            InterviewStatus.COMPLETED,
        )
        self.assertIsNotNone(
            interview.completed_at,
        )

    def test_cancel_interview_records_reason(self):
        interview = self.create_interview()

        interview = InterviewService.update_status(
            request=self.request,
            interview=interview,
            status=InterviewStatus.CANCELLED,
            cancellation_reason=(
                "Candidate requested another date."
            ),
        )

        self.assertEqual(
            interview.status,
            InterviewStatus.CANCELLED,
        )
        self.assertEqual(
            interview.cancellation_reason,
            "Candidate requested another date.",
        )

    def test_create_candidate_evaluation(self):
        interview = self.create_interview()

        evaluation = (
            ApplicationEvaluationService
            .create_evaluation(
                request=self.request,
                values={
                    "application": self.application,
                    "interview": interview,
                    "evaluator": self.interviewer,
                    "technical_score": 9,
                    "communication_score": 8,
                    "culture_score": 8,
                    "overall_score": 9,
                    "recommendation": (
                        EvaluationRecommendation.HIRE
                    ),
                    "strengths": (
                        "Strong backend architecture skills."
                    ),
                },
            )
        )

        self.assertEqual(
            evaluation.overall_score,
            9,
        )
        self.assertEqual(
            evaluation.recommendation,
            EvaluationRecommendation.HIRE,
        )

    def test_evaluation_repository_for_application(self):
        interview = self.create_interview()

        evaluation = (
            ApplicationEvaluation.objects.create(
                application=self.application,
                interview=interview,
                evaluator=self.interviewer,
                overall_score=8,
                recommendation=(
                    EvaluationRecommendation.HIRE
                ),
            )
        )

        queryset = (
            ApplicationEvaluationRepository
            .for_application(self.application.id)
        )

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(
            queryset.first().id,
            evaluation.id,
        )

    def test_evaluation_score_validation(self):
        evaluation = ApplicationEvaluation(
            application=self.application,
            evaluator=self.interviewer,
            overall_score=11,
            recommendation=(
                EvaluationRecommendation.HIRE
            ),
        )

        with self.assertRaises(ValidationError):
            evaluation.full_clean()

    def test_duplicate_interview_participant_is_constrained(
        self,
    ):
        interview = self.create_interview()

        with self.assertRaises(Exception):
            InterviewParticipant.objects.create(
                interview=interview,
                user=self.interviewer,
            )



from .repositories import CareersDashboardRepository


class CareersFinalizationTests(
    CareersFixtureMixin,
    TestCase,
):
    def setUp(self):
        self.user = User.objects.create_user(
            username="careers_final_admin",
            email="careers-final@example.com",
            password="StrongPassword123!",
        )

        self.recruiter = User.objects.create_user(
            username="careers_recruiter",
            email="recruiter@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.user)

        _, _, position = self.create_foundation()

        self.listing = JobListing.objects.create(
            position=position,
            reference_code="LKP-CAREER-300",
        )

        self.application = JobApplication.objects.create(
            listing=self.listing,
            applicant_name="Final Candidate",
            email="final-candidate@example.com",
            consent_to_process=True,
        )

    def test_close_listing(self):
        self.listing.status = (
            JobListingStatus.PUBLISHED
        )
        self.listing.published_at = timezone.now()
        self.listing.save()

        listing = JobListingService.close_listing(
            request=self.request,
            listing=self.listing,
        )

        self.assertEqual(
            listing.status,
            JobListingStatus.CLOSED,
        )

    def test_archive_listing(self):
        listing = JobListingService.archive_listing(
            request=self.request,
            listing=self.listing,
        )

        self.assertEqual(
            listing.status,
            JobListingStatus.ARCHIVED,
        )
        self.assertFalse(listing.is_active)

    def test_review_application(self):
        application = (
            JobApplicationService.review_application(
                request=self.request,
                application=self.application,
                assigned_to=self.recruiter,
                rating=5,
                internal_summary=(
                    "Strong candidate for technical review."
                ),
            )
        )

        self.assertEqual(
            application.assigned_to,
            self.recruiter,
        )
        self.assertEqual(application.rating, 5)
        self.assertIsNotNone(
            application.reviewed_at,
        )

    def test_review_rejects_invalid_rating(self):
        with self.assertRaises(ValueError):
            JobApplicationService.review_application(
                request=self.request,
                application=self.application,
                assigned_to=self.recruiter,
                rating=6,
                internal_summary="",
            )

    def test_dashboard_statistics(self):
        self.listing.status = (
            JobListingStatus.PUBLISHED
        )
        self.listing.published_at = timezone.now()
        self.listing.is_featured = True
        self.listing.save()

        stats = CareersDashboardRepository.statistics()

        self.assertEqual(stats["open_listings"], 1)
        self.assertEqual(
            stats["featured_listings"],
            1,
        )
        self.assertEqual(
            stats["total_applications"],
            1,
        )
        self.assertEqual(
            stats["new_applications"],
            1,
        )
        self.assertEqual(
            stats["applications_by_status"]["new"],
            1,
        )
