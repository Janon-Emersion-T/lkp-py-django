from django.contrib import admin

from .models import (
    Resource,
    ResourceSeo,
)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "resource_type",
        "status",
        "is_featured",
        "download_count",
        "published_at",
    )

    list_filter = (
        "resource_type",
        "status",
        "is_featured",
        "is_active",
    )

    search_fields = (
        "title",
        "slug",
        "excerpt",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }


@admin.register(ResourceSeo)
class ResourceSeoAdmin(admin.ModelAdmin):
    list_display = (
        "resource",
        "meta_title",
        "robots_index",
    )

    search_fields = (
        "resource__title",
        "meta_title",
    )
