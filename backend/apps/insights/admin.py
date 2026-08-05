from django.contrib import admin

from .models import (
    InsightArticle,
    InsightArticleSeo,
    InsightArticleTag,
    InsightCategory,
    InsightInternalLink,
    InsightPublishingEvent,
    InsightRevision,
    InsightTag,
)


class InsightArticleSeoInline(admin.StackedInline):
    model = InsightArticleSeo
    extra = 0
    max_num = 1


class InsightArticleTagInline(admin.TabularInline):
    model = InsightArticleTag
    extra = 0


class InsightInternalLinkInline(admin.TabularInline):
    model = InsightInternalLink
    fk_name = "source_article"
    extra = 0


@admin.register(InsightArticle)
class InsightArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "status",
        "is_featured",
        "is_active",
        "published_at",
        "scheduled_for",
        "view_count",
    )
    list_filter = (
        "status",
        "category",
        "is_featured",
        "is_active",
        "allow_comments",
    )
    search_fields = (
        "title",
        "slug",
        "excerpt",
        "author__email",
    )
    readonly_fields = (
        "word_count",
        "reading_time_minutes",
        "view_count",
        "current_revision_number",
        "published_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        InsightArticleSeoInline,
        InsightArticleTagInline,
        InsightInternalLinkInline,
    )


@admin.register(InsightCategory)
class InsightCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "parent",
        "is_active",
        "sort_order",
    )
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "slug",
        "description",
    )


@admin.register(InsightTag)
class InsightTagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "slug",
        "description",
    )


@admin.register(InsightRevision)
class InsightRevisionAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "revision_number",
        "change_summary",
        "created_at",
    )
    search_fields = (
        "article__title",
        "change_summary",
    )


@admin.register(InsightPublishingEvent)
class InsightPublishingEventAdmin(
    admin.ModelAdmin
):
    list_display = (
        "article",
        "event_type",
        "created_at",
    )
    list_filter = ("event_type",)
    search_fields = (
        "article__title",
        "description",
    )
