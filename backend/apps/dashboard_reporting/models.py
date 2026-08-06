from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class DashboardReportType(models.TextChoices):
    EXECUTIVE = "executive", "Executive dashboard"
    CRM = "crm", "CRM reporting"
    SALES = "sales", "Sales and quotation reporting"
    PROJECTS = "projects", "Project reporting"
    TASKS = "tasks", "Task reporting"
    FINANCE = "finance", "Finance reporting"
    CONTENT_MARKETING = (
        "content_marketing",
        "Content and marketing reporting",
    )
    TEAM = "team", "Team reporting"
    COMPLETE = "complete", "Complete dashboard report"


class DashboardPeriodPreset(models.TextChoices):
    TODAY = "today", "Today"
    THIS_WEEK = "this_week", "This week"
    THIS_MONTH = "this_month", "This month"
    THIS_QUARTER = "this_quarter", "This quarter"
    THIS_YEAR = "this_year", "This year"
    LAST_7_DAYS = "last_7_days", "Last 7 days"
    LAST_30_DAYS = "last_30_days", "Last 30 days"
    LAST_90_DAYS = "last_90_days", "Last 90 days"
    CUSTOM = "custom", "Custom"


class DashboardReportSnapshot(BaseModel):
    report_type = models.CharField(
        max_length=40,
        choices=DashboardReportType.choices,
        db_index=True,
    )

    period_preset = models.CharField(
        max_length=30,
        choices=DashboardPeriodPreset.choices,
        default=DashboardPeriodPreset.THIS_MONTH,
        db_index=True,
    )

    date_from = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    date_to = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    environment = models.CharField(
        max_length=30,
        default="production",
        db_index=True,
    )

    version = models.PositiveBigIntegerField(
        default=1,
        db_index=True,
    )

    payload = models.JSONField(
        default=dict,
        blank=True,
    )

    checksum = models.CharField(
        max_length=64,
        blank=True,
        db_index=True,
    )

    generated_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "-version",
            "-generated_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "report_type",
                    "period_preset",
                    "date_from",
                    "date_to",
                    "environment",
                    "version",
                ),
                condition=models.Q(is_deleted=False),
                name="unique_dashboard_report_snapshot_version",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(date_from__isnull=True)
                    | models.Q(date_to__isnull=True)
                    | models.Q(date_to__gte=models.F("date_from"))
                ),
                name="dashboard_snapshot_valid_date_range",
            ),
        ]
        indexes = [
            models.Index(
                fields=(
                    "report_type",
                    "environment",
                    "is_active",
                ),
                name="dash_report_active_idx",
            ),
            models.Index(
                fields=(
                    "period_preset",
                    "date_from",
                    "date_to",
                ),
                name="dash_report_period_idx",
            ),
            models.Index(
                fields=(
                    "expires_at",
                    "is_active",
                ),
                name="dash_report_expiry_idx",
            ),
        ]

    @property
    def is_expired(self):
        return bool(
            self.expires_at
            and self.expires_at <= timezone.now()
        )

    def __str__(self):
        return (
            f"{self.report_type} — "
            f"{self.period_preset} — "
            f"{self.environment} — "
            f"v{self.version}"
        )
