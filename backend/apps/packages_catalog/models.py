from decimal import Decimal

from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class PackageCategory(models.TextChoices):
    WEBSITE = "website", "Website"
    SEO = "seo", "SEO"
    MARKETING = "marketing", "Marketing"
    SOFTWARE = "software", "Software"
    MOBILE_APP = "mobile_app", "Mobile App"
    HOSTING = "hosting", "Hosting"
    MAINTENANCE = "maintenance", "Maintenance"
    CONSULTING = "consulting", "Consulting"
    OTHER = "other", "Other"


class PackageStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SCHEDULED = "scheduled", "Scheduled"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class PricingType(models.TextChoices):
    FIXED = "fixed", "Fixed"
    STARTING_FROM = "starting_from", "Starting From"
    CUSTOM_QUOTE = "custom_quote", "Custom Quote"
    FREE = "free", "Free"


class BillingCycle(models.TextChoices):
    ONE_TIME = "one_time", "One Time"
    MONTHLY = "monthly", "Monthly"
    QUARTERLY = "quarterly", "Quarterly"
    HALF_YEARLY = "half_yearly", "Half Yearly"
    YEARLY = "yearly", "Yearly"


class Package(BaseModel):
    name = models.CharField(
        max_length=250,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=250,
        unique=True,
        db_index=True,
    )

    category = models.CharField(
        max_length=30,
        choices=PackageCategory.choices,
        default=PackageCategory.OTHER,
        db_index=True,
    )

    service = models.ForeignKey(
        "services_catalog.Service",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="packages",
    )

    short_description = models.CharField(
        max_length=350,
        blank=True,
    )

    description = models.JSONField(
        default=dict,
        blank=True,
    )

    pricing_type = models.CharField(
        max_length=30,
        choices=PricingType.choices,
        default=PricingType.FIXED,
        db_index=True,
    )

    price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    compare_at_price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
    )

    currency = models.CharField(
        max_length=3,
        default="LKR",
        db_index=True,
    )

    billing_cycle = models.CharField(
        max_length=30,
        choices=BillingCycle.choices,
        default=BillingCycle.ONE_TIME,
        db_index=True,
    )

    delivery_time = models.CharField(
        max_length=150,
        blank=True,
    )

    revisions_included = models.PositiveIntegerField(
        default=0,
    )

    support_period_days = models.PositiveIntegerField(
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=PackageStatus.choices,
        default=PackageStatus.DRAFT,
        db_index=True,
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    scheduled_for = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    is_featured = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_popular = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    badge_text = models.CharField(
        max_length=100,
        blank=True,
    )

    cta_label = models.CharField(
        max_length=100,
        blank=True,
    )

    cta_url = models.CharField(
        max_length=500,
        blank=True,
    )

    current_revision_number = models.PositiveIntegerField(
        default=1,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "name",
        )
        indexes = [
            models.Index(
                fields=("category", "status"),
            ),
            models.Index(
                fields=("service", "status"),
            ),
            models.Index(
                fields=("is_featured", "sort_order"),
            ),
            models.Index(
                fields=("is_popular", "sort_order"),
            ),
            models.Index(
                fields=("status", "published_at"),
            ),
        ]

    def __str__(self):
        return self.name

    @property
    def is_publicly_available(self):
        return bool(
            self.is_active
            and self.status == PackageStatus.PUBLISHED
            and self.published_at
            and self.published_at <= timezone.now()
        )


class PackageFeature(BaseModel):
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="features",
    )

    title = models.CharField(max_length=250)

    description = models.TextField(blank=True)

    is_included = models.BooleanField(default=True)

    value = models.CharField(
        max_length=200,
        blank=True,
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        indexes = [
            models.Index(
                fields=("package", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.title


class PackageAddon(BaseModel):
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="addons",
    )

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    currency = models.CharField(
        max_length=3,
        default="LKR",
    )

    billing_cycle = models.CharField(
        max_length=30,
        choices=BillingCycle.choices,
        default=BillingCycle.ONE_TIME,
    )

    is_active = models.BooleanField(default=True)

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "name",
        )
        indexes = [
            models.Index(
                fields=("package", "is_active"),
            ),
        ]

    def __str__(self):
        return self.name


class PackageTargetAudience(BaseModel):
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="target_audiences",
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        indexes = [
            models.Index(
                fields=("package", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.title


class PackageFaq(BaseModel):
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="faqs",
    )

    question = models.CharField(max_length=300)

    answer = models.TextField()

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        indexes = [
            models.Index(
                fields=("package", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.question


class PackageSeo(BaseModel):
    package = models.OneToOneField(
        Package,
        on_delete=models.CASCADE,
        related_name="seo",
    )

    meta_title = models.CharField(
        max_length=70,
        blank=True,
    )

    meta_description = models.CharField(
        max_length=170,
        blank=True,
    )

    canonical_url = models.URLField(blank=True)

    robots_index = models.BooleanField(default=True)

    robots_follow = models.BooleanField(default=True)

    open_graph_title = models.CharField(
        max_length=100,
        blank=True,
    )

    open_graph_description = models.CharField(
        max_length=200,
        blank=True,
    )

    open_graph_image = models.ForeignKey(
        "media_library.MediaAsset",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="package_open_graph_usages",
    )

    twitter_title = models.CharField(
        max_length=100,
        blank=True,
    )

    twitter_description = models.CharField(
        max_length=200,
        blank=True,
    )

    structured_data = models.JSONField(
        default=dict,
        blank=True,
    )

    def __str__(self):
        return f"SEO: {self.package}"


class PackageRevision(BaseModel):
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="revisions",
    )

    revision_number = models.PositiveIntegerField()

    snapshot = models.JSONField(default=dict)

    change_summary = models.CharField(
        max_length=300,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = ("-revision_number",)
        constraints = [
            models.UniqueConstraint(
                fields=("package", "revision_number"),
                condition=models.Q(is_deleted=False),
                name="unique_active_package_revision",
            ),
        ]
        indexes = [
            models.Index(
                fields=("package", "revision_number"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.package} — "
            f"Revision {self.revision_number}"
        )


class PackageComparisonGroup(BaseModel):
    name = models.CharField(
        max_length=200,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        db_index=True,
    )

    description = models.TextField(blank=True)

    packages = models.ManyToManyField(
        Package,
        through="PackageComparisonItem",
        related_name="comparison_groups",
    )

    is_active = models.BooleanField(default=True)

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "name",
        )

    def __str__(self):
        return self.name


class PackageComparisonItem(BaseModel):
    comparison_group = models.ForeignKey(
        PackageComparisonGroup,
        on_delete=models.CASCADE,
        related_name="items",
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="comparison_items",
    )

    sort_order = models.PositiveIntegerField(default=0)

    is_recommended = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "comparison_group",
                    "package",
                ),
                condition=models.Q(is_deleted=False),
                name="unique_active_package_comparison",
            ),
        ]
        indexes = [
            models.Index(
                fields=(
                    "comparison_group",
                    "sort_order",
                ),
            ),
        ]

    def __str__(self):
        return (
            f"{self.comparison_group}: "
            f"{self.package}"
        )
