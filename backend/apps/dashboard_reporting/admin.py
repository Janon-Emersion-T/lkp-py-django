from django.contrib import admin

from .models import DashboardReportSnapshot


@admin.register(DashboardReportSnapshot)
class DashboardReportSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "report_type",
        "period_preset",
        "date_from",
        "date_to",
        "environment",
        "version",
        "generated_at",
        "expires_at",
        "is_active",
        "is_expired_display",
    )

    list_filter = (
        "report_type",
        "period_preset",
        "environment",
        "is_active",
        "generated_at",
        "expires_at",
        "is_deleted",
    )

    search_fields = (
        "report_type",
        "environment",
        "checksum",
    )

    readonly_fields = (
        "id",
        "version",
        "checksum",
        "generated_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    ordering = (
        "-generated_at",
        "-version",
    )

    date_hierarchy = "generated_at"

    @admin.display(
        boolean=True,
        description="Expired",
    )
    def is_expired_display(self, obj):
        return obj.is_expired
