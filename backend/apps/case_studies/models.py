from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class CaseStudyStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    REVIEW = "review", "Review"
    SCHEDULED = "scheduled", "Scheduled"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class CaseStudy(BaseModel):
    title = models.CharField(
        max_length=300,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=320,
        unique=True,
        db_index=True,
    )

    client = models.ForeignKey(
        "clients.Client",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="case_studies",
    )

    project = models.ForeignKey(
        "projects.Project",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="case_studies",
    )

    industry = models.ForeignKey(
        "industries.Industry",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="case_studies",
    )

    services = models.ManyToManyField(
        "services_catalog.Service",
        through="CaseStudyService",
        related_name="case_studies",
    )

    client_name = models.CharField(
        max_length=250,
        blank=True,
    )

    location = models.CharField(
        max_length=200,
        blank=True,
    )

    website_url = models.URLField(blank=True)

    short_description = models.CharField(
        max_length=400,
        blank=True,
    )

    overview = models.JSONField(
        default=dict,
        blank=True,
    )

    challenge = models.JSONField(
        default=dict,
        blank=True,
    )

    solution = models.JSONField(
        default=dict,
        blank=True,
    )

    implementation = models.JSONField(
        default=dict,
        blank=True,
    )

    results = models.JSONField(
        default=dict,
        blank=True,
    )

    testimonial = models.TextField(blank=True)

    testimonial_author = models.CharField(
        max_length=200,
        blank=True,
    )

    testimonial_position = models.CharField(
        max_length=200,
        blank=True,
    )

    featured_image = models.ForeignKey(
        "media_library.MediaAsset",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="featured_case_study_usages",
    )

    status = models.CharField(
        max_length=20,
        choices=CaseStudyStatus.choices,
        default=CaseStudyStatus.DRAFT,
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

    project_start_date = models.DateField(
        null=True,
        blank=True,
    )

    project_completion_date = models.DateField(
        null=True,
        blank=True,
    )

    project_duration = models.CharField(
        max_length=150,
        blank=True,
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

    view_count = models.PositiveBigIntegerField(default=0)

    current_revision_number = models.PositiveIntegerField(
        default=1,
    )

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
                fields=("client", "status"),
            ),
            models.Index(
                fields=("project", "status"),
            ),
            models.Index(
                fields=("industry", "status"),
            ),
            models.Index(
                fields=("is_featured", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.title

    @property
    def is_publicly_available(self):
        return bool(
            self.is_active
            and self.status == CaseStudyStatus.PUBLISHED
            and self.published_at
            and self.published_at <= timezone.now()
        )


class CaseStudyService(BaseModel):
    case_study = models.ForeignKey(
        CaseStudy,
        on_delete=models.CASCADE,
        related_name="service_links",
    )

    service = models.ForeignKey(
        "services_catalog.Service",
        on_delete=models.CASCADE,
        related_name="case_study_links",
    )

    description = models.TextField(blank=True)

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("case_study", "service"),
                condition=models.Q(is_deleted=False),
                name="unique_active_case_study_service",
            ),
        ]
        indexes = [
            models.Index(
                fields=("case_study", "sort_order"),
            ),
        ]

    def __str__(self):
        return f"{self.case_study}: {self.service}"


class CaseStudyTechnology(BaseModel):
    case_study = models.ForeignKey(
        CaseStudy,
        on_delete=models.CASCADE,
        related_name="technologies",
    )

    name = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    logo = models.ForeignKey(
        "media_library.MediaAsset",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="case_study_technology_usages",
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "name",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("case_study", "name"),
                condition=models.Q(is_deleted=False),
                name="unique_active_case_study_technology",
            ),
        ]

    def __str__(self):
        return self.name


class CaseStudyMedia(BaseModel):
    case_study = models.ForeignKey(
        CaseStudy,
        on_delete=models.CASCADE,
        related_name="media_items",
    )

    asset = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="case_study_media_usages",
    )

    title = models.CharField(
        max_length=200,
        blank=True,
    )

    caption = models.TextField(blank=True)

    media_role = models.CharField(
        max_length=50,
        default="gallery",
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
                fields=(
                    "case_study",
                    "media_role",
                    "sort_order",
                ),
            ),
        ]

    def __str__(self):
        return f"{self.case_study}: {self.asset}"


class CaseStudyMetric(BaseModel):
    case_study = models.ForeignKey(
        CaseStudy,
        on_delete=models.CASCADE,
        related_name="metrics",
    )

    label = models.CharField(max_length=150)

    value = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        indexes = [
            models.Index(
                fields=("case_study", "sort_order"),
            ),
        ]

    def __str__(self):
        return f"{self.label}: {self.value}"


class CaseStudyMilestone(BaseModel):
    case_study = models.ForeignKey(
        CaseStudy,
        on_delete=models.CASCADE,
        related_name="milestones",
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    milestone_date = models.DateField(
        null=True,
        blank=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "milestone_date",
        )
        indexes = [
            models.Index(
                fields=("case_study", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.title


class CaseStudySeo(BaseModel):
    case_study = models.OneToOneField(
        CaseStudy,
        on_delete=models.CASCADE,
        related_name="seo",
    )

    meta_title = models.CharField(
        max_length=70,
        blank=True,
    )

    meta_description = models.CharField(
        max_length=170,
        blank=True,
    )

    canonical_url = models.URLField(blank=True)

    robots_index = models.BooleanField(default=True)
    robots_follow = models.BooleanField(default=True)

    open_graph_title = models.CharField(
        max_length=100,
        blank=True,
    )

    open_graph_description = models.CharField(
        max_length=200,
        blank=True,
    )

    open_graph_image = models.ForeignKey(
        "media_library.MediaAsset",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="case_study_open_graph_usages",
    )

    twitter_title = models.CharField(
        max_length=100,
        blank=True,
    )

    twitter_description = models.CharField(
        max_length=200,
        blank=True,
    )

    structured_data = models.JSONField(
        default=dict,
        blank=True,
    )

    def __str__(self):
        return f"SEO: {self.case_study}"


class CaseStudyRevision(BaseModel):
    case_study = models.ForeignKey(
        CaseStudy,
        on_delete=models.CASCADE,
        related_name="revisions",
    )

    revision_number = models.PositiveIntegerField()

    snapshot = models.JSONField(default=dict)

    change_summary = models.CharField(
        max_length=300,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = ("-revision_number",)
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "case_study",
                    "revision_number",
                ),
                condition=models.Q(is_deleted=False),
                name="unique_active_case_study_revision",
            ),
        ]
        indexes = [
            models.Index(
                fields=(
                    "case_study",
                    "revision_number",
                ),
            ),
        ]

    def __str__(self):
        return (
            f"{self.case_study} — "
            f"Revision {self.revision_number}"
        )
