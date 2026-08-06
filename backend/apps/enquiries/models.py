from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class EnquiryStatus(models.TextChoices):
    NEW = "new", "New"
    ASSIGNED = "assigned", "Assigned"
    CONTACTED = "contacted", "Contacted"
    QUALIFIED = "qualified", "Qualified"
    PROPOSAL_SENT = "proposal_sent", "Proposal sent"
    WON = "won", "Won"
    LOST = "lost", "Lost"
    SPAM = "spam", "Spam"
    ARCHIVED = "archived", "Archived"


class EnquiryPriority(models.TextChoices):
    LOW = "low", "Low"
    NORMAL = "normal", "Normal"
    HIGH = "high", "High"
    URGENT = "urgent", "Urgent"


class EnquirySource(models.TextChoices):
    WEBSITE = "website", "Website"
    GOOGLE = "google", "Google"
    FACEBOOK = "facebook", "Facebook"
    INSTAGRAM = "instagram", "Instagram"
    LINKEDIN = "linkedin", "LinkedIn"
    TIKTOK = "tiktok", "TikTok"
    WHATSAPP = "whatsapp", "WhatsApp"
    REFERRAL = "referral", "Referral"
    EMAIL = "email", "Email"
    PHONE = "phone", "Phone"
    MANUAL = "manual", "Manual"
    OTHER = "other", "Other"


class ContactEnquiry(BaseModel):
    reference_code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    name = models.CharField(
        max_length=200,
        db_index=True,
    )

    email = models.EmailField(
        blank=True,
        db_index=True,
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        db_index=True,
    )

    company_name = models.CharField(
        max_length=200,
        blank=True,
        db_index=True,
    )

    subject = models.CharField(
        max_length=250,
        blank=True,
    )

    message = models.TextField()

    source = models.CharField(
        max_length=30,
        choices=EnquirySource.choices,
        default=EnquirySource.WEBSITE,
        db_index=True,
    )

    source_url = models.URLField(blank=True)

    status = models.CharField(
        max_length=30,
        choices=EnquiryStatus.choices,
        default=EnquiryStatus.NEW,
        db_index=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=EnquiryPriority.choices,
        default=EnquiryPriority.NORMAL,
        db_index=True,
    )

    assigned_to = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_contact_enquiries",
    )

    client = models.ForeignKey(
        "clients.Client",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="contact_enquiries",
    )

    lead = models.ForeignKey(
        "crm.Lead",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="contact_enquiries",
    )

    submitted_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    first_contacted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    last_follow_up_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    next_follow_up_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    internal_summary = models.TextField(blank=True)

    loss_reason = models.TextField(blank=True)

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "-submitted_at",
            "-created_at",
        )
        indexes = [
            models.Index(
                fields=("status", "submitted_at"),
            ),
            models.Index(
                fields=("priority", "status"),
            ),
            models.Index(
                fields=("assigned_to", "status"),
            ),
            models.Index(
                fields=("source", "submitted_at"),
            ),
            models.Index(
                fields=("next_follow_up_at", "status"),
            ),
        ]

    def __str__(self):
        return f"{self.reference_code} — {self.name}"


class QuoteEnquiry(BaseModel):
    reference_code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    name = models.CharField(
        max_length=200,
        db_index=True,
    )

    email = models.EmailField(
        blank=True,
        db_index=True,
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        db_index=True,
    )

    company_name = models.CharField(
        max_length=200,
        blank=True,
        db_index=True,
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    website_url = models.URLField(blank=True)

    project_title = models.CharField(
        max_length=250,
        blank=True,
    )

    project_description = models.TextField()

    required_services = models.ManyToManyField(
        "services_catalog.Service",
        through="QuoteEnquiryService",
        related_name="quote_enquiries",
    )

    preferred_package = models.ForeignKey(
        "packages_catalog.Package",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="quote_enquiries",
    )

    budget_min = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )

    budget_max = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )

    budget_currency = models.CharField(
        max_length=3,
        default="LKR",
    )

    desired_start_date = models.DateField(
        null=True,
        blank=True,
    )

    desired_completion_date = models.DateField(
        null=True,
        blank=True,
    )

    source = models.CharField(
        max_length=30,
        choices=EnquirySource.choices,
        default=EnquirySource.WEBSITE,
        db_index=True,
    )

    source_url = models.URLField(blank=True)

    status = models.CharField(
        max_length=30,
        choices=EnquiryStatus.choices,
        default=EnquiryStatus.NEW,
        db_index=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=EnquiryPriority.choices,
        default=EnquiryPriority.NORMAL,
        db_index=True,
    )

    assigned_to = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_quote_enquiries",
    )

    client = models.ForeignKey(
        "clients.Client",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="quote_enquiries",
    )

    lead = models.ForeignKey(
        "crm.Lead",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="quote_enquiries",
    )

    quotation = models.ForeignKey(
        "quotations.Quotation",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="source_quote_enquiries",
    )

    submitted_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    first_contacted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    last_follow_up_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    next_follow_up_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    internal_summary = models.TextField(blank=True)

    loss_reason = models.TextField(blank=True)

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "-submitted_at",
            "-created_at",
        )
        indexes = [
            models.Index(
                fields=("status", "submitted_at"),
            ),
            models.Index(
                fields=("priority", "status"),
            ),
            models.Index(
                fields=("assigned_to", "status"),
            ),
            models.Index(
                fields=("source", "submitted_at"),
            ),
            models.Index(
                fields=("next_follow_up_at", "status"),
            ),
            models.Index(
                fields=("country", "status"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.reference_code} — "
            f"{self.project_title or self.name}"
        )

    def clean(self):
        super().clean()

        from django.core.exceptions import ValidationError

        errors = {}

        if (
            self.budget_min is not None
            and self.budget_max is not None
            and self.budget_min > self.budget_max
        ):
            errors["budget_max"] = (
                "Maximum budget must be greater than "
                "or equal to minimum budget."
            )

        if (
            self.desired_start_date
            and self.desired_completion_date
            and self.desired_completion_date
            < self.desired_start_date
        ):
            errors["desired_completion_date"] = (
                "Desired completion date must not be "
                "before the desired start date."
            )

        if errors:
            raise ValidationError(errors)


class QuoteEnquiryService(BaseModel):
    quote_enquiry = models.ForeignKey(
        QuoteEnquiry,
        on_delete=models.CASCADE,
        related_name="service_links",
    )

    service = models.ForeignKey(
        "services_catalog.Service",
        on_delete=models.PROTECT,
        related_name="quote_enquiry_links",
    )

    notes = models.TextField(blank=True)

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("quote_enquiry", "service"),
                condition=models.Q(is_deleted=False),
                name="unique_active_quote_enquiry_service",
            ),
        ]

    def __str__(self):
        return (
            f"{self.quote_enquiry.reference_code} — "
            f"{self.service.title}"
        )


class EnquiryNote(BaseModel):
    contact_enquiry = models.ForeignKey(
        ContactEnquiry,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    quote_enquiry = models.ForeignKey(
        QuoteEnquiry,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    author = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="enquiry_notes",
    )

    note = models.TextField()

    is_private = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("contact_enquiry", "created_at"),
            ),
            models.Index(
                fields=("quote_enquiry", "created_at"),
            ),
        ]

    def clean(self):
        super().clean()

        from django.core.exceptions import ValidationError

        linked_count = sum(
            value is not None
            for value in (
                self.contact_enquiry_id,
                self.quote_enquiry_id,
            )
        )

        if linked_count != 1:
            raise ValidationError(
                "An enquiry note must belong to exactly "
                "one enquiry."
            )

    def __str__(self):
        enquiry = (
            self.contact_enquiry
            or self.quote_enquiry
        )

        return f"Note for {enquiry}"
