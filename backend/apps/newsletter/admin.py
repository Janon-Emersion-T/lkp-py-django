from django.contrib import admin

from .models import (
    CampaignListTarget,
    CampaignRecipient,
    CampaignTagTarget,
    NewsletterCampaign,
    NewsletterList,
    NewsletterTag,
    Subscriber,
    SubscriberListMembership,
    SubscriberTagAssignment,
)


class SubscriberListMembershipInline(admin.TabularInline):
    model = SubscriberListMembership
    extra = 0
    autocomplete_fields = ("newsletter_list",)


class SubscriberTagAssignmentInline(admin.TabularInline):
    model = SubscriberTagAssignment
    extra = 0
    autocomplete_fields = ("tag",)


@admin.register(NewsletterList)
class NewsletterListAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_default",
        "is_public",
        "is_active",
        "sort_order",
    )
    list_filter = (
        "is_default",
        "is_public",
        "is_active",
    )
    search_fields = (
        "name",
        "slug",
        "description",
    )
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(NewsletterTag)
class NewsletterTagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "color",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "slug",
        "description",
    )
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "company_name",
        "status",
        "source",
        "country",
        "language",
        "consent_given",
        "subscribed_at",
    )
    list_filter = (
        "status",
        "source",
        "country",
        "language",
        "consent_given",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "company_name",
        "phone",
    )
    readonly_fields = (
        "id",
        "confirmation_token",
        "unsubscribe_token",
        "subscribed_at",
        "confirmed_at",
        "unsubscribed_at",
        "last_bounced_at",
        "last_email_sent_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        SubscriberListMembershipInline,
        SubscriberTagAssignmentInline,
    )



class CampaignListTargetInline(admin.TabularInline):
    model = CampaignListTarget
    extra = 0
    autocomplete_fields = ("newsletter_list",)


class CampaignTagTargetInline(admin.TabularInline):
    model = CampaignTagTarget
    extra = 0
    autocomplete_fields = ("tag",)


@admin.register(NewsletterCampaign)
class NewsletterCampaignAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "subject",
        "status",
        "scheduled_for",
        "sent_at",
        "recipient_count",
        "sent_count",
        "delivered_count",
        "opened_count",
        "clicked_count",
    )
    list_filter = (
        "status",
        "scheduled_for",
        "sent_at",
    )
    search_fields = (
        "name",
        "subject",
        "preview_text",
        "from_email",
    )
    readonly_fields = (
        "id",
        "queued_at",
        "sending_started_at",
        "sent_at",
        "completed_at",
        "recipient_count",
        "queued_count",
        "sent_count",
        "delivered_count",
        "opened_count",
        "clicked_count",
        "bounced_count",
        "complained_count",
        "unsubscribed_count",
        "failed_count",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        CampaignListTargetInline,
        CampaignTagTargetInline,
    )


@admin.register(CampaignRecipient)
class CampaignRecipientAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "campaign",
        "status",
        "sent_at",
        "delivered_at",
        "opened_at",
        "clicked_at",
    )
    list_filter = (
        "status",
        "campaign",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "provider_message_id",
    )
    autocomplete_fields = (
        "campaign",
        "subscriber",
    )
    readonly_fields = (
        "id",
        "queued_at",
        "sent_at",
        "delivered_at",
        "opened_at",
        "clicked_at",
        "bounced_at",
        "complained_at",
        "unsubscribed_at",
        "failed_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
