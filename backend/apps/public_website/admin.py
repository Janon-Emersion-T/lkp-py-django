from django.contrib import admin

from .models import PublicWebsiteSnapshot


@admin.register(PublicWebsiteSnapshot)
class PublicWebsiteSnapshotAdmin(
    admin.ModelAdmin
):
    list_display = (
        "snapshot_type",
        "environment",
        "version",
        "generated_at",
        "expires_at",
        "is_active",
        "checksum",
    )
    list_filter = (
        "snapshot_type",
        "environment",
        "is_active",
        "generated_at",
    )
    search_fields = (
        "checksum",
        "snapshot_type",
        "environment",
    )
    readonly_fields = (
        "id",
        "version",
        "payload",
        "generated_at",
        "checksum",
        "created_at",
        "updated_at",
        "deleted_at",
    )
