from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class IndustryStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SCHEDULED = "scheduled", "Scheduled"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class Industry(BaseModel):
    name = models.CharField(
        max_length=250,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=250,
        unique=True,
        db_index=True,
    )

    short_description = models.CharField(
        max_length=350,
        blank=True,
    )

    description = models.JSONField(
        default=dict,
        blank=True,
    )

    hero_title = models.CharField(
        max_length=250,
        blank=True,
    )

    hero_description = models.TextField(blank=True)

    hero_image = models.ForeignKey(
        "media_library.MediaAsset",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="industry_hero_usages",
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=IndustryStatus.choices,
        default=IndustryStatus.DRAFT,
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

    challenges = models.JSONField(
        default=list,
        blank=True,
    )

    solutions = models.JSONField(
        default=list,
        blank=True,
    )

    benefits = models.JSONField(
        default=list,
        blank=True,
    )

    cta_title = models.CharField(
        max_length=200,
        blank=True,
    )

    cta_text = models.CharField(
        max_length=300,
        blank=True,
    )

    cta_label = models.CharField(
        max_length=100,
        blank=True,
    )

    cta_url = models.CharField(
        max_length=500,
        blank=True,
    )

    current_revision_number = models.PositiveIntegerField(
        default=1,
    )

    services = models.ManyToManyField(
        "services_catalog.Service",
        through="IndustryService",
        related_name="industries",
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "name",
        )
        indexes = [
            models.Index(
                fields=("status", "published_at"),
            ),
            models.Index(
                fields=("is_featured", "sort_order"),
            ),
            models.Index(
                fields=("is_active", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.name

    @property
    def is_publicly_available(self):
        return bool(
            self.is_active
            and self.status == IndustryStatus.PUBLISHED
            and self.published_at
            and self.published_at <= timezone.now()
        )


class IndustryService(BaseModel):
    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name="service_links",
    )

    service = models.ForeignKey(
        "services_catalog.Service",
        on_delete=models.CASCADE,
        related_name="industry_links",
    )

    description = models.TextField(blank=True)

    sort_order = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("industry", "service"),
                condition=models.Q(is_deleted=False),
                name="unique_active_industry_service",
            ),
        ]
        indexes = [
            models.Index(
                fields=("industry", "sort_order"),
            ),
        ]

    def __str__(self):
        return f"{self.industry}: {self.service}"


class IndustryFaq(BaseModel):
    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name="faqs",
    )

    question = models.CharField(max_length=300)

    answer = models.TextField()

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        indexes = [
            models.Index(
                fields=("industry", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.question


class IndustrySeo(BaseModel):
    industry = models.OneToOneField(
        Industry,
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
        related_name="industry_open_graph_usages",
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
        return f"SEO: {self.industry}"


class IndustryRevision(BaseModel):
    industry = models.ForeignKey(
        Industry,
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
                fields=("industry", "revision_number"),
                condition=models.Q(is_deleted=False),
                name="unique_active_industry_revision",
            ),
        ]
        indexes = [
            models.Index(
                fields=("industry", "revision_number"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.industry} — "
            f"Revision {self.revision_number}"
        )
