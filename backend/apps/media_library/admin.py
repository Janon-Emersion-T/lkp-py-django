from django.contrib import admin

from .models import (
    MediaAsset,
    MediaFolder,
    MediaUsage,
)


@admin.register(MediaFolder)
class MediaFolderAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "parent",
        "created_at",
    )
    search_fields = (
        "name",
        "slug",
        "description",
    )


class MediaUsageInline(admin.TabularInline):
    model = MediaUsage
    extra = 0


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "media_type",
        "folder",
        "original_name",
        "mime_type",
        "size",
        "is_public",
        "is_optimized",
        "created_at",
    )
    list_filter = (
        "media_type",
        "is_public",
        "is_optimized",
        "created_at",
    )
    search_fields = (
        "title",
        "original_name",
        "alt_text",
        "caption",
        "description",
        "checksum",
    )
    readonly_fields = (
        "checksum",
        "size",
        "mime_type",
        "extension",
        "width",
        "height",
        "duration_seconds",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (MediaUsageInline,)


@admin.register(MediaUsage)
class MediaUsageAdmin(admin.ModelAdmin):
    list_display = (
        "asset",
        "application",
        "model_name",
        "object_id",
        "field_name",
        "created_at",
    )
    list_filter = (
        "application",
        "model_name",
    )
    search_fields = (
        "asset__title",
        "application",
        "model_name",
        "object_id",
        "field_name",
        "usage_context",
    )
