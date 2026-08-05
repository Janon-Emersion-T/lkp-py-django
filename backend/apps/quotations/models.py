from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class QuotationStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    VIEWED = "viewed", "Viewed"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"
    EXPIRED = "expired", "Expired"
    CANCELLED = "cancelled", "Cancelled"


class Quotation(BaseModel):
    quotation_number = models.CharField(
        max_length=40,
        unique=True,
        db_index=True,
    )

    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.PROTECT,
        related_name="quotations",
    )
    lead = models.ForeignKey(
        "crm.Lead",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="quotations",
    )

    title = models.CharField(max_length=250)
    subject = models.CharField(
        max_length=250,
        blank=True,
    )
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=QuotationStatus.choices,
        default=QuotationStatus.DRAFT,
        db_index=True,
    )

    issue_date = models.DateField(
        default=timezone.localdate,
        db_index=True,
    )
    expiry_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    currency = models.CharField(
        max_length=3,
        default="LKR",
    )

    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    discount_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    tax_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    terms = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    accepted_by_name = models.CharField(
        max_length=200,
        blank=True,
    )
    accepted_by_email = models.EmailField(blank=True)

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    duplicated_from = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="duplicates",
    )

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("client", "status"),
            ),
            models.Index(
                fields=("status", "expiry_date"),
            ),
            models.Index(
                fields=("issue_date", "quotation_number"),
            ),
        ]

    def __str__(self):
        return self.quotation_number

    @property
    def is_expired(self):
        return bool(
            self.expiry_date
            and self.expiry_date < timezone.localdate()
            and self.status
            not in (
                QuotationStatus.ACCEPTED,
                QuotationStatus.REJECTED,
                QuotationStatus.CANCELLED,
            )
        )


class QuotationItem(BaseModel):
    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name="items",
    )

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("1.00"),
    )
    unit_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    discount_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    tax_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    tax_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        indexes = [
            models.Index(
                fields=("quotation", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.title


class QuotationEvent(BaseModel):
    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name="events",
    )

    event_type = models.CharField(
        max_length=50,
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
                fields=("quotation", "created_at"),
            ),
        ]

    def __str__(self):
        return f"{self.quotation}: {self.event_type}"


class QuotationRecipient(BaseModel):
    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name="recipients",
    )

    name = models.CharField(
        max_length=200,
        blank=True,
    )
    email = models.EmailField()

    is_primary = models.BooleanField(default=False)
    received_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    viewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("quotation", "email"),
            ),
        ]

    def __str__(self):
        return self.email
