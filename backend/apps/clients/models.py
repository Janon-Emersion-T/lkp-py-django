from django.db import models

from apps.common.models import BaseModel


class ClientStatus(models.TextChoices):
    PROSPECT = "prospect", "Prospect"
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    SUSPENDED = "suspended", "Suspended"
    ARCHIVED = "archived", "Archived"


class ClientType(models.TextChoices):
    COMPANY = "company", "Company"
    INDIVIDUAL = "individual", "Individual"
    NON_PROFIT = "non_profit", "Non-profit"
    GOVERNMENT = "government", "Government"


class Client(BaseModel):
    company_name = models.CharField(
        max_length=250,
        db_index=True,
    )
    legal_name = models.CharField(
        max_length=250,
        blank=True,
    )
    client_code = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
    )

    client_type = models.CharField(
        max_length=30,
        choices=ClientType.choices,
        default=ClientType.COMPANY,
        db_index=True,
    )
    status = models.CharField(
        max_length=30,
        choices=ClientStatus.choices,
        default=ClientStatus.ACTIVE,
        db_index=True,
    )

    industry = models.CharField(
        max_length=150,
        blank=True,
        db_index=True,
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )
    timezone = models.CharField(
        max_length=64,
        default="Asia/Colombo",
    )

    email = models.EmailField(blank=True)
    phone = models.CharField(
        max_length=40,
        blank=True,
    )
    whatsapp = models.CharField(
        max_length=40,
        blank=True,
    )
    website = models.URLField(blank=True)

    tax_number = models.CharField(
        max_length=100,
        blank=True,
    )
    registration_number = models.CharField(
        max_length=100,
        blank=True,
    )

    billing_address = models.TextField(blank=True)
    shipping_address = models.TextField(blank=True)

    default_currency = models.CharField(
        max_length=3,
        default="LKR",
    )
    payment_terms_days = models.PositiveSmallIntegerField(
        default=14,
    )

    notes = models.TextField(blank=True)
    tags = models.JSONField(
        default=list,
        blank=True,
    )

    source_lead = models.OneToOneField(
        "crm.Lead",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="converted_client",
    )

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("status", "company_name"),
            ),
            models.Index(
                fields=("country", "industry"),
            ),
        ]

    def __str__(self):
        return self.company_name


class ClientContact(BaseModel):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="contacts",
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    position = models.CharField(
        max_length=150,
        blank=True,
    )
    department = models.CharField(
        max_length=150,
        blank=True,
    )

    email = models.EmailField(blank=True)
    phone = models.CharField(
        max_length=40,
        blank=True,
    )
    whatsapp = models.CharField(
        max_length=40,
        blank=True,
    )

    is_primary = models.BooleanField(default=False)
    receives_quotations = models.BooleanField(default=True)
    receives_invoices = models.BooleanField(default=True)
    receives_project_updates = models.BooleanField(default=True)

    notes = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("client", "is_primary"),
            ),
            models.Index(
                fields=("client", "email"),
            ),
        ]

    @property
    def full_name(self):
        return " ".join(
            value
            for value in (
                self.first_name,
                self.last_name,
            )
            if value
        )

    def __str__(self):
        return self.full_name


class ClientWebsite(BaseModel):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="websites",
    )

    name = models.CharField(max_length=200)
    url = models.URLField()
    platform = models.CharField(
        max_length=100,
        blank=True,
    )
    admin_url = models.URLField(blank=True)

    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    notes = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("client", "is_active"),
            ),
        ]

    def __str__(self):
        return self.name


class ClientDocument(BaseModel):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    title = models.CharField(max_length=250)
    file = models.FileField(
        upload_to="clients/documents/%Y/%m/",
    )
    document_type = models.CharField(
        max_length=100,
        blank=True,
    )
    original_name = models.CharField(
        max_length=255,
    )
    content_type = models.CharField(
        max_length=150,
        blank=True,
    )
    size = models.PositiveBigIntegerField(default=0)

    description = models.TextField(blank=True)
    is_confidential = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("client", "document_type"),
            ),
        ]

    def __str__(self):
        return self.title
