from django.contrib import admin

from .models import (
    Client,
    ClientContact,
    ClientDocument,
    ClientWebsite,
)


class ClientContactInline(admin.TabularInline):
    model = ClientContact
    extra = 0


class ClientWebsiteInline(admin.TabularInline):
    model = ClientWebsite
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "client_code",
        "company_name",
        "client_type",
        "status",
        "country",
        "default_currency",
        "created_at",
    )
    list_filter = (
        "client_type",
        "status",
        "country",
        "industry",
    )
    search_fields = (
        "client_code",
        "company_name",
        "legal_name",
        "email",
        "phone",
        "whatsapp",
    )
    readonly_fields = (
        "client_code",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        ClientContactInline,
        ClientWebsiteInline,
    )


@admin.register(ClientContact)
class ClientContactAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "client",
        "email",
        "phone",
        "is_primary",
        "created_at",
    )
    list_filter = (
        "is_primary",
        "receives_quotations",
        "receives_invoices",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "client__company_name",
    )


@admin.register(ClientWebsite)
class ClientWebsiteAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "client",
        "url",
        "platform",
        "is_primary",
        "is_active",
    )
    list_filter = (
        "is_primary",
        "is_active",
        "platform",
    )
    search_fields = (
        "name",
        "url",
        "client__company_name",
    )


@admin.register(ClientDocument)
class ClientDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "document_type",
        "is_confidential",
        "created_at",
    )
    list_filter = (
        "document_type",
        "is_confidential",
    )
    search_fields = (
        "title",
        "client__company_name",
        "original_name",
    )
