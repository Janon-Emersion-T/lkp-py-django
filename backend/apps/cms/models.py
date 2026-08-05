from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class ContentStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SCHEDULED = "scheduled", "Scheduled"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class PageType(models.TextChoices):
    HOME = "home", "Home"
    ABOUT = "about", "About"
    GENERIC = "generic", "Generic"
    PRIVACY = "privacy", "Privacy Policy"
    TERMS = "terms", "Terms and Conditions"
    COOKIE = "cookie", "Cookie Policy"
    CONTACT = "contact", "Contact"


class Page(BaseModel):
    title = models.CharField(
        max_length=250,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=250,
        unique=True,
        db_index=True,
    )

    page_type = models.CharField(
        max_length=30,
        choices=PageType.choices,
        default=PageType.GENERIC,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ContentStatus.choices,
        default=ContentStatus.DRAFT,
        db_index=True,
    )

    excerpt = models.TextField(blank=True)
    content = models.JSONField(
        default=dict,
        blank=True,
    )

    template_name = models.CharField(
        max_length=150,
        default="pages/default.html",
    )

    featured_image = models.ImageField(
        upload_to="cms/pages/%Y/%m/",
        null=True,
        blank=True,
    )

    is_indexable = models.BooleanField(default=True)
    is_visible_in_navigation = models.BooleanField(
        default=False,
    )
    navigation_label = models.CharField(
        max_length=100,
        blank=True,
    )
    navigation_order = models.PositiveIntegerField(
        default=0,
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

    current_revision_number = models.PositiveIntegerField(
        default=1,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "navigation_order",
            "title",
        )
        indexes = [
            models.Index(
                fields=("status", "published_at"),
            ),
            models.Index(
                fields=("page_type", "status"),
            ),
            models.Index(
                fields=(
                    "is_visible_in_navigation",
                    "navigation_order",
                ),
            ),
        ]

    def __str__(self):
        return self.title

    @property
    def is_publicly_available(self):
        if self.status != ContentStatus.PUBLISHED:
            return False

        return bool(
            self.published_at
            and self.published_at <= timezone.now()
        )


class PageSeo(BaseModel):
    page = models.OneToOneField(
        Page,
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
    open_graph_image = models.ImageField(
        upload_to="cms/seo/open-graph/%Y/%m/",
        null=True,
        blank=True,
    )

    twitter_title = models.CharField(
        max_length=100,
        blank=True,
    )
    twitter_description = models.CharField(
        max_length=200,
        blank=True,
    )
    twitter_image = models.ImageField(
        upload_to="cms/seo/twitter/%Y/%m/",
        null=True,
        blank=True,
    )

    structured_data = models.JSONField(
        default=dict,
        blank=True,
    )

    def __str__(self):
        return f"SEO: {self.page}"


class PageRevision(BaseModel):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="revisions",
    )

    revision_number = models.PositiveIntegerField()

    title = models.CharField(max_length=250)
    excerpt = models.TextField(blank=True)
    content = models.JSONField(
        default=dict,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ContentStatus.choices,
    )

    change_summary = models.CharField(
        max_length=300,
        blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="cms_page_revisions",
    )

    class Meta(BaseModel.Meta):
        ordering = ("-revision_number",)
        constraints = [
            models.UniqueConstraint(
                fields=("page", "revision_number"),
                condition=models.Q(is_deleted=False),
                name="unique_active_page_revision_number",
            ),
        ]
        indexes = [
            models.Index(
                fields=("page", "revision_number"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.page.title} — "
            f"Revision {self.revision_number}"
        )


class RedirectType(models.IntegerChoices):
    PERMANENT = 301, "Permanent"
    TEMPORARY = 302, "Temporary"
    PERMANENT_PRESERVE_METHOD = 308, (
        "Permanent — Preserve Method"
    )


class Redirect(BaseModel):
    source_path = models.CharField(
        max_length=500,
        unique=True,
        db_index=True,
    )

    destination_url = models.CharField(
        max_length=1000,
    )

    redirect_type = models.PositiveSmallIntegerField(
        choices=RedirectType.choices,
        default=RedirectType.PERMANENT,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    hit_count = models.PositiveBigIntegerField(default=0)
    last_accessed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    notes = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        ordering = ("source_path",)
        indexes = [
            models.Index(
                fields=("is_active", "source_path"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.source_path} → "
            f"{self.destination_url}"
        )


class PublishingEventType(models.TextChoices):
    CREATED = "created", "Created"
    UPDATED = "updated", "Updated"
    SCHEDULED = "scheduled", "Scheduled"
    PUBLISHED = "published", "Published"
    UNPUBLISHED = "unpublished", "Unpublished"
    ARCHIVED = "archived", "Archived"
    RESTORED = "restored", "Revision Restored"


class PublishingEvent(BaseModel):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="publishing_events",
    )

    event_type = models.CharField(
        max_length=30,
        choices=PublishingEventType.choices,
        db_index=True,
    )

    description = models.TextField()
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("page", "created_at"),
            ),
            models.Index(
                fields=("event_type", "created_at"),
            ),
        ]

    def __str__(self):
        return f"{self.page}: {self.event_type}"


class ContentBlock(BaseModel):
    name = models.CharField(
        max_length=200,
        db_index=True,
    )

    key = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
    )

    description = models.TextField(blank=True)

    content = models.JSONField(
        default=dict,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    version = models.PositiveIntegerField(default=1)

    class Meta(BaseModel.Meta):
        ordering = ("name",)
        indexes = [
            models.Index(
                fields=("is_active", "name"),
            ),
        ]

    def __str__(self):
        return self.name


class PageContentBlock(BaseModel):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="content_blocks",
    )

    content_block = models.ForeignKey(
        ContentBlock,
        on_delete=models.PROTECT,
        related_name="page_placements",
    )

    section_key = models.CharField(
        max_length=150,
    )

    sort_order = models.PositiveIntegerField(default=0)
    is_enabled = models.BooleanField(default=True)

    configuration = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "page",
                    "content_block",
                    "section_key",
                ),
                condition=models.Q(is_deleted=False),
                name="unique_active_page_content_block",
            ),
        ]
        indexes = [
            models.Index(
                fields=(
                    "page",
                    "section_key",
                    "sort_order",
                ),
            ),
        ]

    def __str__(self):
        return (
            f"{self.page} — "
            f"{self.content_block}"
        )
