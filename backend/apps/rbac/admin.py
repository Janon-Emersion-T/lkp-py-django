from django.contrib import admin

from .models import Role, UserRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "priority",
        "is_system",
        "is_active",
    )
    list_filter = (
        "is_system",
        "is_active",
    )
    search_fields = (
        "name",
        "slug",
        "description",
    )
    filter_horizontal = ("permissions",)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "is_active",
        "valid_from",
        "valid_until",
    )
    list_filter = (
        "role",
        "is_active",
    )
    search_fields = (
        "user__email",
        "role__name",
    )
