from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class MediaType(models.TextChoices):
    IMAGE = "image", "Image"
    VIDEO = "video", "Video"
    DOCUMENT = "document", "Document"
    PDF = "pdf", "PDF"
    ICON = "icon", "Icon"
    LOGO = "logo", "Logo"
    OTHER = "other", "Other"


class MediaFolder(BaseModel):
    name = models.CharField(max_length=200)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    slug = models.SlugField(
        max_length=220,
        db_index=True,
    )

    description = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("parent", "slug"),
                condition=models.Q(is_deleted=False),
                name="unique_active_media_folder_slug",
            ),
        ]
        indexes = [
            models.Index(
                fields=("parent", "name"),
            ),
        ]

    def __str__(self):
        return self.name


class MediaAsset(BaseModel):
    folder = models.ForeignKey(
        MediaFolder,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assets",
    )

    title = models.CharField(
        max_length=250,
        db_index=True,
    )

    file = models.FileField(
        upload_to="media-library/%Y/%m/",
    )

    original_name = models.CharField(max_length=255)

    media_type = models.CharField(
        max_length=30,
        choices=MediaType.choices,
        default=MediaType.OTHER,
        db_index=True,
    )

    mime_type = models.CharField(
        max_length=150,
        blank=True,
    )

    extension = models.CharField(
        max_length=20,
        blank=True,
    )

    size = models.PositiveBigIntegerField(default=0)

    width = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    height = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    duration_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    alt_text = models.CharField(
        max_length=250,
        blank=True,
    )
    caption = models.TextField(blank=True)
    description = models.TextField(blank=True)

    tags = models.JSONField(
        default=list,
        blank=True,
    )

    checksum = models.CharField(
        max_length=128,
        blank=True,
        db_index=True,
    )

    is_optimized = models.BooleanField(default=False)
    optimized_file = models.FileField(
        upload_to="media-library/optimized/%Y/%m/",
        null=True,
        blank=True,
    )

    webp_file = models.ImageField(
        upload_to="media-library/webp/%Y/%m/",
        null=True,
        blank=True,
    )

    is_public = models.BooleanField(
        default=True,
        db_index=True,
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="uploaded_media_assets",
    )

    class Meta(BaseModel.Meta):
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("folder", "media_type"),
            ),
            models.Index(
                fields=("media_type", "created_at"),
            ),
            models.Index(
                fields=("is_public", "created_at"),
            ),
        ]

    def __str__(self):
        return self.title


class MediaUsage(BaseModel):
    asset = models.ForeignKey(
        MediaAsset,
        on_delete=models.CASCADE,
        related_name="usages",
    )

    application = models.CharField(
        max_length=100,
        db_index=True,
    )

    model_name = models.CharField(
        max_length=100,
        db_index=True,
    )

    object_id = models.CharField(
        max_length=100,
        db_index=True,
    )

    field_name = models.CharField(
        max_length=100,
        blank=True,
    )

    usage_context = models.CharField(
        max_length=200,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "asset",
                    "application",
                    "model_name",
                    "object_id",
                    "field_name",
                ),
                condition=models.Q(is_deleted=False),
                name="unique_active_media_usage",
            ),
        ]
        indexes = [
            models.Index(
                fields=(
                    "application",
                    "model_name",
                    "object_id",
                ),
            ),
            models.Index(
                fields=("asset", "created_at"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.asset} used by "
            f"{self.application}.{self.model_name}"
        )
