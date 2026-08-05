from django.contrib import admin

from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "actor",
        "module",
        "action",
        "entity_type",
    )
    list_filter = (
        "module",
        "action",
        "created_at",
    )
    search_fields = (
        "description",
        "actor__email",
        "entity_type",
        "entity_id",
    )
    readonly_fields = (
        "actor",
        "action",
        "module",
        "entity_type",
        "entity_id",
        "description",
        "metadata",
        "ip_address",
        "user_agent",
        "created_at",
    )
