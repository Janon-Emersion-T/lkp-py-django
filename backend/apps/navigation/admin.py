from django.contrib import admin

from .models import (
    NavigationMenu,
    NavigationMenuItem,
)


class NavigationMenuItemInline(admin.TabularInline):
    model = NavigationMenuItem
    fk_name = "menu"
    extra = 0
    fields = (
        "label",
        "parent",
        "link_type",
        "url",
        "visibility",
        "is_active",
        "is_featured",
        "sort_order",
    )
    autocomplete_fields = (
        "parent",
    )


@admin.register(NavigationMenu)
class NavigationMenuAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "location",
        "is_active",
        "is_public",
        "sort_order",
    )
    list_filter = (
        "location",
        "is_active",
        "is_public",
    )
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
    inlines = (NavigationMenuItemInline,)


@admin.register(NavigationMenuItem)
class NavigationMenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "menu",
        "parent",
        "link_type",
        "visibility",
        "is_active",
        "is_featured",
        "sort_order",
    )
    list_filter = (
        "menu",
        "link_type",
        "visibility",
        "is_active",
        "is_featured",
    )
    search_fields = (
        "label",
        "url",
        "route_name",
        "menu__name",
    )
    autocomplete_fields = (
        "menu",
        "parent",
        "cms_page",
        "service",
        "package",
        "industry",
        "insight",
        "case_study",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )
