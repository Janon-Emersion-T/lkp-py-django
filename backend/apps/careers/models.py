from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class JobListingStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    REVIEW = "review", "Review"
    SCHEDULED = "scheduled", "Scheduled"
    PUBLISHED = "published", "Published"
    CLOSED = "closed", "Closed"
    ARCHIVED = "archived", "Archived"


class RemotePolicy(models.TextChoices):
    ONSITE = "onsite", "On-site"
    HYBRID = "hybrid", "Hybrid"
    REMOTE = "remote", "Remote"


class ExperienceLevel(models.TextChoices):
    INTERN = "intern", "Intern"
    ENTRY = "entry", "Entry level"
    JUNIOR = "junior", "Junior"
    MID = "mid", "Mid level"
    SENIOR = "senior", "Senior"
    LEAD = "lead", "Lead"
    EXECUTIVE = "executive", "Executive"


class JobDepartment(BaseModel):
    name = models.CharField(
        max_length=150,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=170,
        unique=True,
        db_index=True,
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "name",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("name",),
                condition=models.Q(is_deleted=False),
                name="unique_active_job_department_name",
            ),
        ]
        indexes = [
            models.Index(
                fields=("is_active", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.name


class EmploymentType(BaseModel):
    name = models.CharField(
        max_length=100,
        db_index=True,
    )

    code = models.SlugField(
        max_length=120,
        unique=True,
        db_index=True,
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "name",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("name",),
                condition=models.Q(is_deleted=False),
                name="unique_active_employment_type_name",
            ),
        ]
        indexes = [
            models.Index(
                fields=("is_active", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.name


class JobPosition(BaseModel):
    department = models.ForeignKey(
        JobDepartment,
        on_delete=models.PROTECT,
        related_name="positions",
    )

    employment_type = models.ForeignKey(
        EmploymentType,
        on_delete=models.PROTECT,
        related_name="positions",
    )

    title = models.CharField(
        max_length=200,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        db_index=True,
    )

    summary = models.CharField(
        max_length=500,
        blank=True,
    )

    description = models.JSONField(
        default=dict,
        blank=True,
    )

    responsibilities = models.JSONField(
        default=list,
        blank=True,
    )

    requirements = models.JSONField(
        default=list,
        blank=True,
    )

    preferred_qualifications = models.JSONField(
        default=list,
        blank=True,
    )

    benefits = models.JSONField(
        default=list,
        blank=True,
    )

    location = models.CharField(
        max_length=200,
        blank=True,
    )

    remote_policy = models.CharField(
        max_length=20,
        choices=RemotePolicy.choices,
        default=RemotePolicy.ONSITE,
        db_index=True,
    )

    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.ENTRY,
        db_index=True,
    )

    salary_min = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )

    salary_max = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )

    salary_currency = models.CharField(
        max_length=3,
        default="LKR",
    )

    salary_visible = models.BooleanField(default=False)

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "title",
        )
        indexes = [
            models.Index(
                fields=("department", "is_active"),
            ),
            models.Index(
                fields=("employment_type", "is_active"),
            ),
            models.Index(
                fields=("experience_level", "is_active"),
            ),
            models.Index(
                fields=("remote_policy", "is_active"),
            ),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()

        if (
            self.salary_min is not None
            and self.salary_max is not None
            and self.salary_min > self.salary_max
        ):
            from django.core.exceptions import ValidationError

            raise ValidationError(
                {
                    "salary_max": (
                        "Maximum salary must be greater than "
                        "or equal to minimum salary."
                    ),
                }
            )


class JobListing(BaseModel):
    position = models.ForeignKey(
        JobPosition,
        on_delete=models.PROTECT,
        related_name="listings",
    )

    reference_code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=JobListingStatus.choices,
        default=JobListingStatus.DRAFT,
        db_index=True,
    )

    number_of_openings = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )

    application_deadline = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    scheduled_for = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    is_featured = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "-published_at",
            "-created_at",
        )
        indexes = [
            models.Index(
                fields=("status", "published_at"),
            ),
            models.Index(
                fields=("position", "status"),
            ),
            models.Index(
                fields=("is_featured", "sort_order"),
            ),
            models.Index(
                fields=("application_deadline", "status"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.reference_code} — "
            f"{self.position.title}"
        )

    @property
    def is_publicly_available(self):
        now = timezone.now()

        deadline_open = (
            self.application_deadline is None
            or self.application_deadline >= now
        )

        return bool(
            self.is_active
            and self.position.is_active
            and self.position.department.is_active
            and self.position.employment_type.is_active
            and self.status == JobListingStatus.PUBLISHED
            and self.published_at
            and self.published_at <= now
            and deadline_open
        )



class JobApplicationStatus(models.TextChoices):
    NEW = "new", "New"
    SCREENING = "screening", "Screening"
    SHORTLISTED = "shortlisted", "Shortlisted"
    INTERVIEW = "interview", "Interview"
    ASSESSMENT = "assessment", "Assessment"
    OFFERED = "offered", "Offered"
    HIRED = "hired", "Hired"
    REJECTED = "rejected", "Rejected"
    WITHDRAWN = "withdrawn", "Withdrawn"
    ARCHIVED = "archived", "Archived"


class JobApplicationSource(models.TextChoices):
    CAREERS_PAGE = "careers_page", "Careers page"
    LINKEDIN = "linkedin", "LinkedIn"
    FACEBOOK = "facebook", "Facebook"
    REFERRAL = "referral", "Referral"
    EMAIL = "email", "Email"
    MANUAL = "manual", "Manual"
    OTHER = "other", "Other"


class ApplicationQuestionType(models.TextChoices):
    SHORT_TEXT = "short_text", "Short text"
    LONG_TEXT = "long_text", "Long text"
    NUMBER = "number", "Number"
    BOOLEAN = "boolean", "Yes or no"
    SINGLE_CHOICE = "single_choice", "Single choice"
    MULTIPLE_CHOICE = (
        "multiple_choice",
        "Multiple choice",
    )
    DATE = "date", "Date"


class ApplicationQuestion(BaseModel):
    listing = models.ForeignKey(
        JobListing,
        on_delete=models.CASCADE,
        related_name="application_questions",
    )

    question = models.CharField(max_length=500)

    question_type = models.CharField(
        max_length=30,
        choices=ApplicationQuestionType.choices,
        default=ApplicationQuestionType.SHORT_TEXT,
        db_index=True,
    )

    help_text = models.CharField(
        max_length=500,
        blank=True,
    )

    options = models.JSONField(
        default=list,
        blank=True,
    )

    is_required = models.BooleanField(default=False)

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        indexes = [
            models.Index(
                fields=("listing", "is_active", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.question


class JobApplication(BaseModel):
    listing = models.ForeignKey(
        JobListing,
        on_delete=models.PROTECT,
        related_name="applications",
    )

    applicant_name = models.CharField(
        max_length=200,
        db_index=True,
    )

    email = models.EmailField(db_index=True)

    phone = models.CharField(
        max_length=50,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        blank=True,
    )

    city = models.CharField(
        max_length=150,
        blank=True,
    )

    linkedin_url = models.URLField(blank=True)

    portfolio_url = models.URLField(blank=True)

    current_company = models.CharField(
        max_length=200,
        blank=True,
    )

    current_position = models.CharField(
        max_length=200,
        blank=True,
    )

    years_of_experience = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )

    expected_salary = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )

    expected_salary_currency = models.CharField(
        max_length=3,
        default="LKR",
    )

    availability_date = models.DateField(
        null=True,
        blank=True,
    )

    cover_letter = models.TextField(blank=True)

    resume_asset = models.ForeignKey(
        "media_library.MediaAsset",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="job_application_resume_usages",
    )

    status = models.CharField(
        max_length=30,
        choices=JobApplicationStatus.choices,
        default=JobApplicationStatus.NEW,
        db_index=True,
    )

    source = models.CharField(
        max_length=30,
        choices=JobApplicationSource.choices,
        default=JobApplicationSource.CAREERS_PAGE,
        db_index=True,
    )

    assigned_to = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_job_applications",
    )

    submitted_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    internal_summary = models.TextField(blank=True)

    rejection_reason = models.TextField(blank=True)

    consent_to_process = models.BooleanField(default=False)

    consent_to_retain = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        ordering = (
            "-submitted_at",
            "-created_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("listing", "email"),
                condition=models.Q(is_deleted=False),
                name="unique_active_job_application_email",
            ),
        ]
        indexes = [
            models.Index(
                fields=("listing", "status"),
            ),
            models.Index(
                fields=("status", "submitted_at"),
            ),
            models.Index(
                fields=("assigned_to", "status"),
            ),
            models.Index(
                fields=("source", "submitted_at"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.applicant_name} — "
            f"{self.listing.position.title}"
        )


class ApplicationAnswer(BaseModel):
    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    question = models.ForeignKey(
        ApplicationQuestion,
        on_delete=models.PROTECT,
        related_name="answers",
    )

    answer = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "question__sort_order",
            "created_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("application", "question"),
                condition=models.Q(is_deleted=False),
                name="unique_active_application_answer",
            ),
        ]
        indexes = [
            models.Index(
                fields=("application", "question"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.application.applicant_name}: "
            f"{self.question.question[:60]}"
        )


class ApplicationNote(BaseModel):
    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    author = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="job_application_notes",
    )

    note = models.TextField()

    is_private = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("application", "created_at"),
            ),
        ]

    def __str__(self):
        return (
            f"Note for {self.application.applicant_name}"
        )



class InterviewStatus(models.TextChoices):
    SCHEDULED = "scheduled", "Scheduled"
    CONFIRMED = "confirmed", "Confirmed"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    NO_SHOW = "no_show", "No show"
    RESCHEDULED = "rescheduled", "Rescheduled"


class InterviewType(models.TextChoices):
    PHONE = "phone", "Phone"
    VIDEO = "video", "Video"
    ONSITE = "onsite", "On-site"
    TECHNICAL = "technical", "Technical"
    HR = "hr", "HR"
    FINAL = "final", "Final"


class Interview(BaseModel):
    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="interviews",
    )

    title = models.CharField(
        max_length=200,
        default="Job Interview",
    )

    interview_type = models.CharField(
        max_length=30,
        choices=InterviewType.choices,
        default=InterviewType.VIDEO,
        db_index=True,
    )

    status = models.CharField(
        max_length=30,
        choices=InterviewStatus.choices,
        default=InterviewStatus.SCHEDULED,
        db_index=True,
    )

    scheduled_start = models.DateTimeField(db_index=True)

    scheduled_end = models.DateTimeField(db_index=True)

    timezone_name = models.CharField(
        max_length=100,
        default="Asia/Colombo",
    )

    location = models.CharField(
        max_length=300,
        blank=True,
    )

    meeting_url = models.URLField(blank=True)

    instructions = models.TextField(blank=True)

    organizer = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="organized_job_interviews",
    )

    interviewers = models.ManyToManyField(
        "accounts.User",
        through="InterviewParticipant",
        through_fields=("interview", "user"),
        related_name="job_interviews",
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    cancellation_reason = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        ordering = (
            "scheduled_start",
            "created_at",
        )
        indexes = [
            models.Index(
                fields=("application", "status"),
            ),
            models.Index(
                fields=("scheduled_start", "status"),
            ),
            models.Index(
                fields=("organizer", "scheduled_start"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.title} — "
            f"{self.application.applicant_name}"
        )

    def clean(self):
        super().clean()

        if (
            self.scheduled_start
            and self.scheduled_end
            and self.scheduled_end <= self.scheduled_start
        ):
            from django.core.exceptions import ValidationError

            raise ValidationError(
                {
                    "scheduled_end": (
                        "Interview end time must be after "
                        "the start time."
                    ),
                }
            )


class InterviewParticipant(BaseModel):
    interview = models.ForeignKey(
        Interview,
        on_delete=models.CASCADE,
        related_name="participants",
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="interview_participations",
    )

    is_lead = models.BooleanField(default=False)

    attendance_confirmed = models.BooleanField(
        default=False,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "-is_lead",
            "created_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("interview", "user"),
                condition=models.Q(is_deleted=False),
                name="unique_active_interview_participant",
            ),
        ]

    def __str__(self):
        return (
            f"{self.user} — {self.interview}"
        )


class EvaluationRecommendation(models.TextChoices):
    STRONG_HIRE = "strong_hire", "Strong hire"
    HIRE = "hire", "Hire"
    HOLD = "hold", "Hold"
    NO_HIRE = "no_hire", "No hire"
    STRONG_NO_HIRE = (
        "strong_no_hire",
        "Strong no hire",
    )


class ApplicationEvaluation(BaseModel):
    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="evaluations",
    )

    interview = models.ForeignKey(
        Interview,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="evaluations",
    )

    evaluator = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="job_application_evaluations",
    )

    technical_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )

    communication_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )

    culture_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )

    overall_score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )

    recommendation = models.CharField(
        max_length=30,
        choices=EvaluationRecommendation.choices,
        db_index=True,
    )

    strengths = models.TextField(blank=True)

    concerns = models.TextField(blank=True)

    comments = models.TextField(blank=True)

    submitted_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "-submitted_at",
            "-created_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "application",
                    "interview",
                    "evaluator",
                ),
                condition=models.Q(is_deleted=False),
                name="unique_active_application_evaluation",
            ),
        ]
        indexes = [
            models.Index(
                fields=("application", "recommendation"),
            ),
            models.Index(
                fields=("evaluator", "submitted_at"),
            ),
            models.Index(
                fields=("interview", "submitted_at"),
            ),
        ]

    def __str__(self):
        return (
            f"Evaluation: "
            f"{self.application.applicant_name} by "
            f"{self.evaluator}"
        )
