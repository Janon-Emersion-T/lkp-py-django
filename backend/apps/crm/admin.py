from django.contrib import admin

from .models import (
    Lead,
    LeadAttachment,
    LeadNote,
    LeadTimeline,
)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "email",
        "source",
        "status",
        "priority",
        "assigned_to",
        "lead_score",
        "created_at",
    )
    list_filter = (
        "source",
        "status",
        "priority",
        "country",
    )
    search_fields = (
        "name",
        "company",
        "email",
        "phone",
        "whatsapp",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )


@admin.register(LeadNote)
class LeadNoteAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "is_pinned",
        "created_by",
        "created_at",
    )
    list_filter = ("is_pinned",)
    search_fields = (
        "lead__name",
        "lead__company",
        "content",
    )


@admin.register(LeadTimeline)
class LeadTimelineAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "event_type",
        "created_by",
        "created_at",
    )
    list_filter = ("event_type",)
    search_fields = (
        "lead__name",
        "description",
    )


@admin.register(LeadAttachment)
class LeadAttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "original_name",
        "content_type",
        "size",
        "created_at",
    )
    search_fields = (
        "lead__name",
        "original_name",
    )
