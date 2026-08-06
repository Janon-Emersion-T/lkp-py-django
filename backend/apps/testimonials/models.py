from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class TestimonialStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    REVIEW = "review", "Review"
    SCHEDULED = "scheduled", "Scheduled"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class TestimonialSource(models.TextChoices):
    DIRECT = "direct", "Direct"
    GOOGLE = "google", "Google"
    FACEBOOK = "facebook", "Facebook"
    LINKEDIN = "linkedin", "LinkedIn"
    WHATSAPP = "whatsapp", "WhatsApp"
    EMAIL = "email", "Email"
    OTHER = "other", "Other"


class Testimonial(BaseModel):
    client = models.ForeignKey(
        "clients.Client",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="testimonials",
    )

    project = models.ForeignKey(
        "projects.Project",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="testimonials",
    )

    author_name = models.CharField(
        max_length=200,
        db_index=True,
    )

    author_position = models.CharField(
        max_length=200,
        blank=True,
    )

    company_name = models.CharField(
        max_length=250,
        blank=True,
        db_index=True,
    )

    content = models.TextField()

    short_content = models.CharField(
        max_length=400,
        blank=True,
    )

    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    source = models.CharField(
        max_length=30,
        choices=TestimonialSource.choices,
        default=TestimonialSource.DIRECT,
        db_index=True,
    )

    source_url = models.URLField(blank=True)

    author_image = models.ForeignKey(
        "media_library.MediaAsset",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="testimonial_author_image_usages",
    )

    company_logo = models.ForeignKey(
        "media_library.MediaAsset",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="testimonial_company_logo_usages",
    )

    status = models.CharField(
        max_length=20,
        choices=TestimonialStatus.choices,
        default=TestimonialStatus.DRAFT,
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

    is_verified = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    internal_notes = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
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
                fields=("is_featured", "sort_order"),
            ),
            models.Index(
                fields=("is_verified", "status"),
            ),
            models.Index(
                fields=("client", "status"),
            ),
            models.Index(
                fields=("project", "status"),
            ),
            models.Index(
                fields=("source", "status"),
            ),
        ]

    def __str__(self):
        company = self.company_name or "Independent client"
        return f"{self.author_name} — {company}"

    @property
    def is_publicly_available(self):
        return bool(
            self.is_active
            and self.status == TestimonialStatus.PUBLISHED
            and self.published_at
            and self.published_at <= timezone.now()
        )
