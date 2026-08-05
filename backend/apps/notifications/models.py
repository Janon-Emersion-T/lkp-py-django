from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class NotificationType(models.TextChoices):
    INFO = "info", "Information"
    SUCCESS = "success", "Success"
    WARNING = "warning", "Warning"
    ERROR = "error", "Error"
    ACTION_REQUIRED = "action_required", "Action required"


class NotificationChannel(models.TextChoices):
    DASHBOARD = "dashboard", "Dashboard"
    EMAIL = "email", "Email"
    BROWSER = "browser", "Browser"


class Notification(BaseModel):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        default=NotificationType.INFO,
        db_index=True,
    )
    channel = models.CharField(
        max_length=20,
        choices=NotificationChannel.choices,
        default=NotificationChannel.DASHBOARD,
        db_index=True,
    )

    title = models.CharField(max_length=200)
    message = models.TextField()
    action_url = models.CharField(
        max_length=500,
        blank=True,
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    is_read = models.BooleanField(
        default=False,
        db_index=True,
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("recipient", "is_read"),
            ),
            models.Index(
                fields=("recipient", "created_at"),
            ),
        ]

    def __str__(self):
        return self.title
