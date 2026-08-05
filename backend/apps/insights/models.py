from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class ArticleStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    REVIEW = "review", "Review"
    SCHEDULED = "scheduled", "Scheduled"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class InsightCategory(BaseModel):
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

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

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
        indexes = [
            models.Index(
                fields=("parent", "sort_order"),
            ),
            models.Index(
                fields=("is_active", "name"),
            ),
        ]

    def __str__(self):
        return self.name


class InsightTag(BaseModel):
    name = models.CharField(
        max_length=100,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        db_index=True,
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta(BaseModel.Meta):
        ordering = ("name",)

    def __str__(self):
        return self.name


class InsightArticle(BaseModel):
    title = models.CharField(
        max_length=300,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=320,
        unique=True,
        db_index=True,
    )

    excerpt = models.TextField(blank=True)

    content = models.JSONField(
        default=dict,
        blank=True,
    )

    category = models.ForeignKey(
        InsightCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articles",
    )

    tags = models.ManyToManyField(
        InsightTag,
        through="InsightArticleTag",
        related_name="articles",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="authored_insights",
    )

    featured_image = models.ForeignKey(
        "media_library.MediaAsset",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="featured_insight_usages",
    )

    status = models.CharField(
        max_length=20,
        choices=ArticleStatus.choices,
        default=ArticleStatus.DRAFT,
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

    reading_time_minutes = models.PositiveIntegerField(
        default=1,
    )

    word_count = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    allow_comments = models.BooleanField(default=False)

    view_count = models.PositiveBigIntegerField(default=0)

    current_revision_number = models.PositiveIntegerField(
        default=1,
    )

    related_articles = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="related_to_articles",
    )

    class Meta(BaseModel.Meta):
        ordering = ("-published_at", "-created_at")
        indexes = [
            models.Index(
                fields=("status", "published_at"),
            ),
            models.Index(
                fields=("category", "status"),
            ),
            models.Index(
                fields=("author", "status"),
            ),
            models.Index(
                fields=("is_featured", "published_at"),
            ),
        ]

    def __str__(self):
        return self.title

    @property
    def is_publicly_available(self):
        return bool(
            self.is_active
            and self.status == ArticleStatus.PUBLISHED
            and self.published_at
            and self.published_at <= timezone.now()
        )


class InsightArticleTag(BaseModel):
    article = models.ForeignKey(
        InsightArticle,
        on_delete=models.CASCADE,
        related_name="article_tags",
    )

    tag = models.ForeignKey(
        InsightTag,
        on_delete=models.CASCADE,
        related_name="tagged_articles",
    )

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("article", "tag"),
                condition=models.Q(is_deleted=False),
                name="unique_active_insight_article_tag",
            ),
        ]

    def __str__(self):
        return f"{self.article}: {self.tag}"


class InsightArticleSeo(BaseModel):
    article = models.OneToOneField(
        InsightArticle,
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
        related_name="insight_open_graph_usages",
    )

    twitter_title = models.CharField(
        max_length=100,
        blank=True,
    )

    twitter_description = models.CharField(
        max_length=200,
        blank=True,
    )

    article_schema = models.JSONField(
        default=dict,
        blank=True,
    )

    faq_schema = models.JSONField(
        default=list,
        blank=True,
    )

    def __str__(self):
        return f"SEO: {self.article}"


class InsightRevision(BaseModel):
    article = models.ForeignKey(
        InsightArticle,
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
                fields=("article", "revision_number"),
                condition=models.Q(is_deleted=False),
                name="unique_active_insight_revision",
            ),
        ]
        indexes = [
            models.Index(
                fields=("article", "revision_number"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.article} — "
            f"Revision {self.revision_number}"
        )


class InsightInternalLink(BaseModel):
    source_article = models.ForeignKey(
        InsightArticle,
        on_delete=models.CASCADE,
        related_name="outgoing_internal_links",
    )

    target_article = models.ForeignKey(
        InsightArticle,
        on_delete=models.CASCADE,
        related_name="incoming_internal_links",
    )

    anchor_text = models.CharField(max_length=250)

    context = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "source_article",
                    "target_article",
                    "anchor_text",
                ),
                condition=models.Q(is_deleted=False),
                name="unique_active_insight_internal_link",
            ),
            models.CheckConstraint(
                condition=~models.Q(
                    source_article=models.F("target_article")
                ),
                name="insight_internal_link_not_self",
            ),
        ]
        indexes = [
            models.Index(
                fields=("source_article", "is_active"),
            ),
            models.Index(
                fields=("target_article", "is_active"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.source_article} → "
            f"{self.target_article}"
        )


class InsightPublishingEventType(models.TextChoices):
    CREATED = "created", "Created"
    UPDATED = "updated", "Updated"
    SUBMITTED = "submitted", "Submitted for Review"
    SCHEDULED = "scheduled", "Scheduled"
    PUBLISHED = "published", "Published"
    UNPUBLISHED = "unpublished", "Unpublished"
    ARCHIVED = "archived", "Archived"
    RESTORED = "restored", "Revision Restored"


class InsightPublishingEvent(BaseModel):
    article = models.ForeignKey(
        InsightArticle,
        on_delete=models.CASCADE,
        related_name="publishing_events",
    )

    event_type = models.CharField(
        max_length=30,
        choices=InsightPublishingEventType.choices,
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
                fields=("article", "created_at"),
            ),
            models.Index(
                fields=("event_type", "created_at"),
            ),
        ]

    def __str__(self):
        return f"{self.article}: {self.event_type}"
