from django.contrib import admin

from .models import (
    Quotation,
    QuotationEvent,
    QuotationItem,
    QuotationRecipient,
)


class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 0


class QuotationRecipientInline(admin.TabularInline):
    model = QuotationRecipient
    extra = 0


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = (
        "quotation_number",
        "client",
        "title",
        "status",
        "issue_date",
        "expiry_date",
        "currency",
        "total_amount",
    )
    list_filter = (
        "status",
        "currency",
        "issue_date",
        "expiry_date",
    )
    search_fields = (
        "quotation_number",
        "title",
        "client__company_name",
        "client__client_code",
    )
    readonly_fields = (
        "quotation_number",
        "subtotal",
        "total_amount",
        "accepted_at",
        "sent_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        QuotationItemInline,
        QuotationRecipientInline,
    )


@admin.register(QuotationEvent)
class QuotationEventAdmin(admin.ModelAdmin):
    list_display = (
        "quotation",
        "event_type",
        "created_by",
        "created_at",
    )
    list_filter = ("event_type",)
    search_fields = (
        "quotation__quotation_number",
        "description",
    )


@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    list_display = (
        "quotation",
        "title",
        "quantity",
        "unit_price",
        "total_amount",
        "sort_order",
    )


@admin.register(QuotationRecipient)
class QuotationRecipientAdmin(admin.ModelAdmin):
    list_display = (
        "quotation",
        "email",
        "is_primary",
        "received_at",
        "viewed_at",
    )
    search_fields = (
        "quotation__quotation_number",
        "email",
        "name",
    )
