from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class ResourceType(models.TextChoices):
    DOWNLOAD = "download", "Download"
    GUIDE = "guide", "Guide"
    CHECKLIST = "checklist", "Checklist"
    TEMPLATE = "template", "Template"


class ResourceStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    REVIEW = "review", "Review"
    SCHEDULED = "scheduled", "Scheduled"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class Resource(BaseModel):
    title = models.CharField(
        max_length=250,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=250,
        unique=True,
        db_index=True,
    )

    resource_type = models.CharField(
        max_length=30,
        choices=ResourceType.choices,
        db_index=True,
    )

    excerpt = models.CharField(
        max_length=500,
        blank=True,
    )

    content = models.JSONField(
        default=dict,
        blank=True,
    )

    file = models.FileField(
        upload_to="resources/files/%Y/%m/",
        null=True,
        blank=True,
    )

    external_url = models.URLField(
        blank=True,
    )

    featured_image = models.ImageField(
        upload_to="resources/images/%Y/%m/",
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ResourceStatus.choices,
        default=ResourceStatus.DRAFT,
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

    download_count = models.PositiveBigIntegerField(
        default=0,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "-published_at",
            "-created_at",
        )

        indexes = [
            models.Index(
                fields=("resource_type", "status"),
            ),
            models.Index(
                fields=("status", "published_at"),
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
            and self.status == ResourceStatus.PUBLISHED
            and self.published_at
            and self.published_at <= timezone.now()
        )

    @property
    def resource_url(self):
        if self.file:
            return self.file.url

        return self.external_url or ""


class ResourceSeo(BaseModel):
    resource = models.OneToOneField(
        Resource,
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

    canonical_url = models.URLField(
        blank=True,
    )

    robots_index = models.BooleanField(
        default=True,
    )

    robots_follow = models.BooleanField(
        default=True,
    )

    open_graph_title = models.CharField(
        max_length=100,
        blank=True,
    )

    open_graph_description = models.CharField(
        max_length=200,
        blank=True,
    )

    structured_data = models.JSONField(
        default=dict,
        blank=True,
    )

    def __str__(self):
        return f"SEO: {self.resource.title}"
