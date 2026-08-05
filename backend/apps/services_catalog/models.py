from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class ServiceStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SCHEDULED = "scheduled", "Scheduled"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class Service(BaseModel):
    title = models.CharField(
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
        related_name="service_hero_usages",
    )

    status = models.CharField(
        max_length=20,
        choices=ServiceStatus.choices,
        default=ServiceStatus.DRAFT,
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

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    cta_title = models.CharField(
        max_length=200,
        blank=True,
    )

    cta_text = models.CharField(
        max_length=250,
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

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "title",
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
        return self.title

    @property
    def is_publicly_available(self):
        return bool(
            self.is_active
            and self.status == ServiceStatus.PUBLISHED
            and self.published_at
            and self.published_at <= timezone.now()
        )


class ServiceFeature(BaseModel):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="features",
    )

    title = models.CharField(max_length=200)
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
                fields=("service", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.title


class ServiceProcessStep(BaseModel):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="process_steps",
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    step_number = models.PositiveIntegerField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "step_number",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("service", "step_number"),
                condition=models.Q(is_deleted=False),
                name="unique_active_service_process_step",
            ),
        ]

    def __str__(self):
        return f"{self.service}: {self.title}"


class ServiceTechnology(BaseModel):
    service = models.ForeignKey(
        Service,
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
        related_name="service_technology_usages",
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "name",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("service", "name"),
                condition=models.Q(is_deleted=False),
                name="unique_active_service_technology",
            ),
        ]

    def __str__(self):
        return self.name


class ServiceFaq(BaseModel):
    service = models.ForeignKey(
        Service,
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
                fields=("service", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.question


class ServiceSeo(BaseModel):
    service = models.OneToOneField(
        Service,
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
        related_name="service_open_graph_usages",
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
        return f"SEO: {self.service}"


class ServiceRevision(BaseModel):
    service = models.ForeignKey(
        Service,
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
                fields=("service", "revision_number"),
                condition=models.Q(is_deleted=False),
                name="unique_active_service_revision",
            ),
        ]
        indexes = [
            models.Index(
                fields=("service", "revision_number"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.service} — "
            f"Revision {self.revision_number}"
        )
