import secrets

from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class SubscriberStatus(models.TextChoices):
    PENDING = "pending", "Pending confirmation"
    ACTIVE = "active", "Active"
    UNSUBSCRIBED = "unsubscribed", "Unsubscribed"
    BOUNCED = "bounced", "Bounced"
    COMPLAINED = "complained", "Complained"
    SUPPRESSED = "suppressed", "Suppressed"


class SubscriptionSource(models.TextChoices):
    WEBSITE = "website", "Website"
    MANUAL = "manual", "Manual"
    IMPORT = "import", "Import"
    CONTACT_FORM = "contact_form", "Contact form"
    QUOTE_FORM = "quote_form", "Quote form"
    CAREERS = "careers", "Careers"
    CLIENT_PORTAL = "client_portal", "Client portal"
    OTHER = "other", "Other"


class NewsletterList(BaseModel):
    name = models.CharField(
        max_length=150,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=170,
        unique=True,
        db_index=True,
    )

    description = models.TextField(blank=True)

    is_default = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_public = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "name",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("name",),
                condition=models.Q(is_deleted=False),
                name="unique_active_newsletter_list_name",
            ),
        ]
        indexes = [
            models.Index(
                fields=("is_active", "is_public"),
            ),
            models.Index(
                fields=("is_default", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.name


class NewsletterTag(BaseModel):
    name = models.CharField(
        max_length=100,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        db_index=True,
    )

    description = models.TextField(blank=True)

    color = models.CharField(
        max_length=20,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta(BaseModel.Meta):
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("name",),
                condition=models.Q(is_deleted=False),
                name="unique_active_newsletter_tag_name",
            ),
        ]

    def __str__(self):
        return self.name


class Subscriber(BaseModel):
    email = models.EmailField(
        unique=True,
        db_index=True,
    )

    first_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
    )

    company_name = models.CharField(
        max_length=200,
        blank=True,
        db_index=True,
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    language = models.CharField(
        max_length=10,
        default="en",
        db_index=True,
    )

    status = models.CharField(
        max_length=30,
        choices=SubscriberStatus.choices,
        default=SubscriberStatus.PENDING,
        db_index=True,
    )

    source = models.CharField(
        max_length=30,
        choices=SubscriptionSource.choices,
        default=SubscriptionSource.WEBSITE,
        db_index=True,
    )

    source_reference = models.CharField(
        max_length=200,
        blank=True,
    )

    consent_given = models.BooleanField(default=False)

    consent_ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    consent_user_agent = models.TextField(blank=True)

    subscribed_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    unsubscribed_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    confirmation_token = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        editable=False,
    )

    unsubscribe_token = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        editable=False,
    )

    bounce_count = models.PositiveIntegerField(default=0)

    last_bounced_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    last_email_sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    lists = models.ManyToManyField(
        NewsletterList,
        through="SubscriberListMembership",
        related_name="subscribers",
    )

    tags = models.ManyToManyField(
        NewsletterTag,
        through="SubscriberTagAssignment",
        related_name="subscribers",
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "-subscribed_at",
            "email",
        )
        indexes = [
            models.Index(
                fields=("status", "subscribed_at"),
            ),
            models.Index(
                fields=("source", "status"),
            ),
            models.Index(
                fields=("country", "status"),
            ),
            models.Index(
                fields=("language", "status"),
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.confirmation_token:
            self.confirmation_token = secrets.token_urlsafe(48)

        if not self.unsubscribe_token:
            self.unsubscribe_token = secrets.token_urlsafe(48)

        self.email = self.email.strip().lower()

        return super().save(*args, **kwargs)

    @property
    def full_name(self):
        return " ".join(
            part
            for part in (
                self.first_name,
                self.last_name,
            )
            if part
        )

    @property
    def can_receive_email(self):
        return bool(
            self.status == SubscriberStatus.ACTIVE
            and self.confirmed_at
            and self.consent_given
            and not self.is_deleted
        )

    def __str__(self):
        return self.full_name or self.email


class SubscriberListMembership(BaseModel):
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        related_name="list_memberships",
    )

    newsletter_list = models.ForeignKey(
        NewsletterList,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    joined_at = models.DateTimeField(
        default=timezone.now,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "newsletter_list__sort_order",
            "joined_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "subscriber",
                    "newsletter_list",
                ),
                condition=models.Q(is_deleted=False),
                name="unique_active_subscriber_list_membership",
            ),
        ]
        indexes = [
            models.Index(
                fields=(
                    "newsletter_list",
                    "joined_at",
                ),
            ),
        ]

    def __str__(self):
        return (
            f"{self.subscriber.email} — "
            f"{self.newsletter_list.name}"
        )


class SubscriberTagAssignment(BaseModel):
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        related_name="tag_assignments",
    )

    tag = models.ForeignKey(
        NewsletterTag,
        on_delete=models.CASCADE,
        related_name="assignments",
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "tag__name",
            "created_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("subscriber", "tag"),
                condition=models.Q(is_deleted=False),
                name="unique_active_subscriber_tag_assignment",
            ),
        ]

    def __str__(self):
        return (
            f"{self.subscriber.email} — "
            f"{self.tag.name}"
        )



class CampaignStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    REVIEW = "review", "Review"
    SCHEDULED = "scheduled", "Scheduled"
    QUEUED = "queued", "Queued"
    SENDING = "sending", "Sending"
    SENT = "sent", "Sent"
    PAUSED = "paused", "Paused"
    CANCELLED = "cancelled", "Cancelled"
    FAILED = "failed", "Failed"
    ARCHIVED = "archived", "Archived"


class CampaignRecipientStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    QUEUED = "queued", "Queued"
    SENT = "sent", "Sent"
    DELIVERED = "delivered", "Delivered"
    OPENED = "opened", "Opened"
    CLICKED = "clicked", "Clicked"
    BOUNCED = "bounced", "Bounced"
    COMPLAINED = "complained", "Complained"
    UNSUBSCRIBED = "unsubscribed", "Unsubscribed"
    FAILED = "failed", "Failed"
    SKIPPED = "skipped", "Skipped"


class NewsletterCampaign(BaseModel):
    name = models.CharField(
        max_length=200,
        db_index=True,
    )

    subject = models.CharField(max_length=255)

    preview_text = models.CharField(
        max_length=255,
        blank=True,
    )

    from_name = models.CharField(
        max_length=150,
        default="LKProfessionals",
    )

    from_email = models.EmailField()

    reply_to_email = models.EmailField(blank=True)

    html_content = models.TextField(blank=True)

    text_content = models.TextField(blank=True)

    status = models.CharField(
        max_length=30,
        choices=CampaignStatus.choices,
        default=CampaignStatus.DRAFT,
        db_index=True,
    )

    scheduled_for = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    queued_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    sending_started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    failure_reason = models.TextField(blank=True)

    lists = models.ManyToManyField(
        NewsletterList,
        through="CampaignListTarget",
        related_name="campaigns",
    )

    tags = models.ManyToManyField(
        NewsletterTag,
        through="CampaignTagTarget",
        related_name="campaigns",
    )

    recipient_count = models.PositiveIntegerField(
        default=0,
    )

    queued_count = models.PositiveIntegerField(
        default=0,
    )

    sent_count = models.PositiveIntegerField(
        default=0,
    )

    delivered_count = models.PositiveIntegerField(
        default=0,
    )

    opened_count = models.PositiveIntegerField(
        default=0,
    )

    clicked_count = models.PositiveIntegerField(
        default=0,
    )

    bounced_count = models.PositiveIntegerField(
        default=0,
    )

    complained_count = models.PositiveIntegerField(
        default=0,
    )

    unsubscribed_count = models.PositiveIntegerField(
        default=0,
    )

    failed_count = models.PositiveIntegerField(
        default=0,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "-created_at",
            "name",
        )
        indexes = [
            models.Index(
                fields=("status", "scheduled_for"),
            ),
            models.Index(
                fields=("status", "sent_at"),
            ),
            models.Index(
                fields=("created_at", "status"),
            ),
        ]

    def __str__(self):
        return self.name

    @property
    def open_rate(self):
        if not self.delivered_count:
            return 0.0

        return round(
            self.opened_count
            / self.delivered_count
            * 100,
            2,
        )

    @property
    def click_rate(self):
        if not self.delivered_count:
            return 0.0

        return round(
            self.clicked_count
            / self.delivered_count
            * 100,
            2,
        )


class CampaignListTarget(BaseModel):
    campaign = models.ForeignKey(
        NewsletterCampaign,
        on_delete=models.CASCADE,
        related_name="list_targets",
    )

    newsletter_list = models.ForeignKey(
        NewsletterList,
        on_delete=models.PROTECT,
        related_name="campaign_targets",
    )

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("campaign", "newsletter_list"),
                condition=models.Q(is_deleted=False),
                name="unique_active_campaign_list_target",
            ),
        ]

    def __str__(self):
        return (
            f"{self.campaign.name} — "
            f"{self.newsletter_list.name}"
        )


class CampaignTagTarget(BaseModel):
    campaign = models.ForeignKey(
        NewsletterCampaign,
        on_delete=models.CASCADE,
        related_name="tag_targets",
    )

    tag = models.ForeignKey(
        NewsletterTag,
        on_delete=models.PROTECT,
        related_name="campaign_targets",
    )

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("campaign", "tag"),
                condition=models.Q(is_deleted=False),
                name="unique_active_campaign_tag_target",
            ),
        ]

    def __str__(self):
        return (
            f"{self.campaign.name} — "
            f"{self.tag.name}"
        )


class CampaignRecipient(BaseModel):
    campaign = models.ForeignKey(
        NewsletterCampaign,
        on_delete=models.CASCADE,
        related_name="recipients",
    )

    subscriber = models.ForeignKey(
        Subscriber,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="campaign_recipients",
    )

    email = models.EmailField(db_index=True)

    first_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=CampaignRecipientStatus.choices,
        default=CampaignRecipientStatus.PENDING,
        db_index=True,
    )

    queued_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    opened_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    clicked_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    bounced_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    complained_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    unsubscribed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    failed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    failure_reason = models.TextField(blank=True)

    provider_message_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    open_count = models.PositiveIntegerField(default=0)

    click_count = models.PositiveIntegerField(default=0)

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "email",
            "created_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("campaign", "email"),
                condition=models.Q(is_deleted=False),
                name="unique_active_campaign_recipient_email",
            ),
        ]
        indexes = [
            models.Index(
                fields=("campaign", "status"),
            ),
            models.Index(
                fields=("campaign", "sent_at"),
            ),
            models.Index(
                fields=("subscriber", "status"),
            ),
        ]

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.campaign.name} — {self.email}"
