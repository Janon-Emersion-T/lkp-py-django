from django.contrib import admin

from .models import (
    Account,
    Expense,
    Invoice,
    InvoiceItem,
    LedgerEntry,
    Payment,
    RecurringTransaction,
    Transaction,
)


class LedgerEntryInline(admin.TabularInline):
    model = LedgerEntry
    extra = 0


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "account_code",
        "name",
        "account_type",
        "currency",
        "opening_balance",
        "current_balance",
        "is_active",
    )
    list_filter = (
        "account_type",
        "currency",
        "is_active",
        "is_system",
    )
    search_fields = (
        "account_code",
        "name",
        "description",
    )
    readonly_fields = (
        "current_balance",
        "created_at",
        "updated_at",
        "deleted_at",
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_number",
        "transaction_type",
        "transaction_date",
        "description",
        "total_amount",
    )
    list_filter = (
        "transaction_type",
        "transaction_date",
    )
    search_fields = (
        "transaction_number",
        "description",
        "reference",
    )
    readonly_fields = (
        "transaction_number",
        "total_amount",
        "created_at",
        "updated_at",
    )
    inlines = (LedgerEntryInline,)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "client",
        "status",
        "issue_date",
        "due_date",
        "currency",
        "total_amount",
        "paid_amount",
        "balance_due",
    )
    list_filter = (
        "status",
        "currency",
        "issue_date",
        "due_date",
    )
    search_fields = (
        "invoice_number",
        "client__company_name",
        "client__client_code",
    )
    readonly_fields = (
        "invoice_number",
        "subtotal",
        "tax_amount",
        "total_amount",
        "paid_amount",
        "balance_due",
        "sent_at",
        "paid_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (InvoiceItemInline,)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_number",
        "invoice",
        "client",
        "payment_date",
        "amount",
        "currency",
        "method",
        "status",
    )
    list_filter = (
        "status",
        "method",
        "currency",
        "payment_date",
    )
    search_fields = (
        "payment_number",
        "invoice__invoice_number",
        "reference",
    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "expense_number",
        "expense_date",
        "vendor",
        "description",
        "category",
        "amount",
        "currency",
        "status",
    )
    list_filter = (
        "category",
        "status",
        "currency",
        "expense_date",
    )
    search_fields = (
        "expense_number",
        "vendor",
        "description",
        "reference",
    )


admin.site.register(RecurringTransaction)
