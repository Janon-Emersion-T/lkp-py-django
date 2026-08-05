from django.contrib import admin

from .models import (
    ContentBlock,
    Page,
    PageContentBlock,
    PageRevision,
    PageSeo,
    PublishingEvent,
    Redirect,
)


class PageSeoInline(admin.StackedInline):
    model = PageSeo
    extra = 0
    max_num = 1


class PageContentBlockInline(admin.TabularInline):
    model = PageContentBlock
    extra = 0


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "page_type",
        "status",
        "published_at",
        "scheduled_for",
        "is_indexable",
        "is_visible_in_navigation",
    )
    list_filter = (
        "page_type",
        "status",
        "is_indexable",
        "is_visible_in_navigation",
    )
    search_fields = (
        "title",
        "slug",
        "excerpt",
    )
    readonly_fields = (
        "current_revision_number",
        "published_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        PageSeoInline,
        PageContentBlockInline,
    )


@admin.register(PageRevision)
class PageRevisionAdmin(admin.ModelAdmin):
    list_display = (
        "page",
        "revision_number",
        "status",
        "created_by",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = (
        "page__title",
        "change_summary",
    )


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = (
        "source_path",
        "destination_url",
        "redirect_type",
        "is_active",
        "hit_count",
    )
    list_filter = (
        "redirect_type",
        "is_active",
    )
    search_fields = (
        "source_path",
        "destination_url",
    )


admin.site.register(ContentBlock)
admin.site.register(PublishingEvent)
