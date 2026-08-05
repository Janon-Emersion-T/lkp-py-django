from django.contrib import admin

from .models import (
    Industry,
    IndustryFaq,
    IndustryRevision,
    IndustrySeo,
    IndustryService,
)


class IndustryServiceInline(admin.TabularInline):
    model = IndustryService
    extra = 0


class IndustryFaqInline(admin.TabularInline):
    model = IndustryFaq
    extra = 0


class IndustrySeoInline(admin.StackedInline):
    model = IndustrySeo
    extra = 0
    max_num = 1


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "status",
        "is_featured",
        "is_active",
        "sort_order",
        "published_at",
        "scheduled_for",
    )
    list_filter = (
        "status",
        "is_featured",
        "is_active",
    )
    search_fields = (
        "name",
        "slug",
        "short_description",
    )
    readonly_fields = (
        "current_revision_number",
        "published_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        IndustrySeoInline,
        IndustryServiceInline,
        IndustryFaqInline,
    )


@admin.register(IndustryRevision)
class IndustryRevisionAdmin(admin.ModelAdmin):
    list_display = (
        "industry",
        "revision_number",
        "change_summary",
        "created_at",
    )
    search_fields = (
        "industry__name",
        "change_summary",
    )
