from django.contrib import admin

from .models import (
    WebsiteSetting,
    WebsiteSettingGroup,
)


class WebsiteSettingInline(admin.TabularInline):
    model = WebsiteSetting
    extra = 0
    fields = (
        "key",
        "label",
        "value_type",
        "environment",
        "value",
        "is_public",
        "is_editable",
        "is_active",
        "sort_order",
    )


@admin.register(WebsiteSettingGroup)
class WebsiteSettingGroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "icon",
        "is_active",
        "sort_order",
    )
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "slug",
        "description",
    )
    prepopulated_fields = {
        "slug": ("name",),
    }
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (WebsiteSettingInline,)


@admin.register(WebsiteSetting)
class WebsiteSettingAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "label",
        "group",
        "value_type",
        "environment",
        "is_public",
        "is_editable",
        "is_required",
        "is_active",
        "sort_order",
    )
    list_filter = (
        "group",
        "value_type",
        "environment",
        "is_public",
        "is_editable",
        "is_required",
        "is_active",
    )
    search_fields = (
        "key",
        "label",
        "description",
        "value",
    )
    autocomplete_fields = (
        "group",
        "media_asset",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )
