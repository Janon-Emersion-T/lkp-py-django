from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "actor",
        "event_type",
        "severity",
        "module",
        "target_type",
    )
    list_filter = (
        "event_type",
        "severity",
        "module",
        "created_at",
    )
    search_fields = (
        "message",
        "actor__email",
        "target_type",
        "target_id",
    )
    readonly_fields = (
        "actor",
        "event_type",
        "severity",
        "module",
        "target_type",
        "target_id",
        "message",
        "before",
        "after",
        "metadata",
        "ip_address",
        "user_agent",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
