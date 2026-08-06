from django.contrib import admin

from .models import (
    ContactEnquiry,
    EnquiryNote,
    QuoteEnquiry,
    QuoteEnquiryService,
)


class ContactEnquiryNoteInline(admin.TabularInline):
    model = EnquiryNote
    fk_name = "contact_enquiry"
    extra = 0
    autocomplete_fields = ("author",)


class QuoteEnquiryServiceInline(admin.TabularInline):
    model = QuoteEnquiryService
    extra = 0
    autocomplete_fields = ("service",)


class QuoteEnquiryNoteInline(admin.TabularInline):
    model = EnquiryNote
    fk_name = "quote_enquiry"
    extra = 0
    autocomplete_fields = ("author",)


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "reference_code",
        "name",
        "company_name",
        "status",
        "priority",
        "source",
        "assigned_to",
        "submitted_at",
        "next_follow_up_at",
    )
    list_filter = (
        "status",
        "priority",
        "source",
        "submitted_at",
    )
    search_fields = (
        "reference_code",
        "name",
        "email",
        "phone",
        "company_name",
        "subject",
        "message",
    )
    autocomplete_fields = (
        "assigned_to",
        "client",
        "lead",
    )
    readonly_fields = (
        "id",
        "submitted_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (ContactEnquiryNoteInline,)


@admin.register(QuoteEnquiry)
class QuoteEnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "reference_code",
        "name",
        "company_name",
        "project_title",
        "country",
        "status",
        "priority",
        "source",
        "assigned_to",
        "submitted_at",
    )
    list_filter = (
        "status",
        "priority",
        "source",
        "country",
        "submitted_at",
    )
    search_fields = (
        "reference_code",
        "name",
        "email",
        "phone",
        "company_name",
        "project_title",
        "project_description",
    )
    autocomplete_fields = (
        "assigned_to",
        "client",
        "lead",
        "quotation",
        "preferred_package",
    )
    readonly_fields = (
        "id",
        "submitted_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        QuoteEnquiryServiceInline,
        QuoteEnquiryNoteInline,
    )


@admin.register(EnquiryNote)
class EnquiryNoteAdmin(admin.ModelAdmin):
    list_display = (
        "contact_enquiry",
        "quote_enquiry",
        "author",
        "is_private",
        "created_at",
    )
    list_filter = ("is_private",)
    search_fields = (
        "note",
        "contact_enquiry__reference_code",
        "quote_enquiry__reference_code",
    )
    autocomplete_fields = (
        "contact_enquiry",
        "quote_enquiry",
        "author",
    )
