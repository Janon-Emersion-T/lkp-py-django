from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class PublicSnapshotType(models.TextChoices):
    BOOTSTRAP = "bootstrap", "Bootstrap"
    HOMEPAGE = "homepage", "Homepage"
    CATALOG = "catalog", "Catalog"
    CONTENT = "content", "Content"
    SITEMAP = "sitemap", "Sitemap"


class PublicWebsiteSnapshot(BaseModel):
    snapshot_type = models.CharField(
        max_length=30,
        choices=PublicSnapshotType.choices,
        db_index=True,
    )

    environment = models.CharField(
        max_length=30,
        default="production",
        db_index=True,
    )

    version = models.PositiveBigIntegerField(
        default=1,
        db_index=True,
    )

    payload = models.JSONField(
        default=dict,
        blank=True,
    )

    generated_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    checksum = models.CharField(
        max_length=64,
        blank=True,
        db_index=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "-version",
            "-generated_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "snapshot_type",
                    "environment",
                    "version",
                ),
                condition=models.Q(is_deleted=False),
                name="unique_public_snapshot_version",
            ),
        ]
        indexes = [
            models.Index(
                fields=(
                    "snapshot_type",
                    "environment",
                    "is_active",
                ),
            ),
            models.Index(
                fields=(
                    "expires_at",
                    "is_active",
                ),
            ),
        ]

    @property
    def is_expired(self):
        return bool(
            self.expires_at
            and self.expires_at <= timezone.now()
        )

    def __str__(self):
        return (
            f"{self.snapshot_type}:"
            f"{self.environment}:v{self.version}"
        )
