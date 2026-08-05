from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class LeadSource(models.TextChoices):
    GOOGLE = "google", "Google"
    ORGANIC_SEARCH = "organic_search", "Organic Search"
    FACEBOOK = "facebook", "Facebook"
    INSTAGRAM = "instagram", "Instagram"
    LINKEDIN = "linkedin", "LinkedIn"
    TIKTOK = "tiktok", "TikTok"
    REFERRAL = "referral", "Referral"
    WHATSAPP = "whatsapp", "WhatsApp"
    EMAIL = "email", "Email"
    MANUAL = "manual", "Manual"
    OTHER = "other", "Other"


class LeadStatus(models.TextChoices):
    NEW = "new", "New"
    CONTACTED = "contacted", "Contacted"
    FOLLOW_UP = "follow_up", "Follow Up"
    PROPOSAL_SENT = "proposal_sent", "Proposal Sent"
    NEGOTIATION = "negotiation", "Negotiation"
    WON = "won", "Won"
    LOST = "lost", "Lost"
    SPAM = "spam", "Spam"


class LeadPriority(models.TextChoices):
    LOW = "low", "Low"
    NORMAL = "normal", "Normal"
    HIGH = "high", "High"
    URGENT = "urgent", "Urgent"


class LeadTimelineEvent(models.TextChoices):
    CREATED = "created", "Created"
    UPDATED = "updated", "Updated"
    STATUS_CHANGED = "status_changed", "Status Changed"
    ASSIGNED = "assigned", "Assigned"
    NOTE_ADDED = "note_added", "Note Added"
    ATTACHMENT_ADDED = "attachment_added", "Attachment Added"
    EMAIL = "email", "Email"
    WHATSAPP = "whatsapp", "WhatsApp"
    PHONE_CALL = "phone_call", "Phone Call"
    PROPOSAL_SENT = "proposal_sent", "Proposal Sent"
    CONVERTED = "converted", "Converted"


class Lead(BaseModel):
    name = models.CharField(max_length=200)
    company = models.CharField(
        max_length=200,
        blank=True,
    )
    email = models.EmailField(
        blank=True,
        db_index=True,
    )
    phone = models.CharField(
        max_length=40,
        blank=True,
    )
    whatsapp = models.CharField(
        max_length=40,
        blank=True,
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )
    website = models.URLField(blank=True)

    source = models.CharField(
        max_length=30,
        choices=LeadSource.choices,
        default=LeadSource.MANUAL,
        db_index=True,
    )
    status = models.CharField(
        max_length=30,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
        db_index=True,
    )
    priority = models.CharField(
        max_length=20,
        choices=LeadPriority.choices,
        default=LeadPriority.NORMAL,
        db_index=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_leads",
    )

    lead_score = models.PositiveSmallIntegerField(
        default=0,
    )
    estimated_value = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )
    currency = models.CharField(
        max_length=3,
        default="LKR",
    )

    notes = models.TextField(blank=True)
    tags = models.JSONField(
        default=list,
        blank=True,
    )

    next_follow_up_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )
    last_contacted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("status", "priority"),
            ),
            models.Index(
                fields=("assigned_to", "status"),
            ),
            models.Index(
                fields=("source", "created_at"),
            ),
        ]

    def __str__(self):
        return self.company or self.name


class LeadNote(BaseModel):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="lead_notes",
    )
    content = models.TextField()

    is_pinned = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("lead", "created_at"),
            ),
        ]

    def __str__(self):
        return f"Note for {self.lead}"


class LeadTimeline(BaseModel):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="timeline_entries",
    )
    event_type = models.CharField(
        max_length=40,
        choices=LeadTimelineEvent.choices,
        db_index=True,
    )
    description = models.TextField()
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("lead", "created_at"),
            ),
            models.Index(
                fields=("lead", "event_type"),
            ),
        ]

    def __str__(self):
        return f"{self.lead}: {self.event_type}"


class LeadAttachment(BaseModel):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    file = models.FileField(
        upload_to="crm/leads/%Y/%m/",
    )
    original_name = models.CharField(
        max_length=255,
    )
    content_type = models.CharField(
        max_length=150,
        blank=True,
    )
    size = models.PositiveBigIntegerField(default=0)
    description = models.CharField(
        max_length=500,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("lead", "created_at"),
            ),
        ]

    def __str__(self):
        return self.original_name
