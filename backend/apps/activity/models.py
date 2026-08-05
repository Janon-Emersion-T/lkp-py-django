from django.conf import settings
from django.db import models


class ActivityLog(models.Model):
    id = models.BigAutoField(primary_key=True)

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="activity_logs",
    )

    action = models.CharField(
        max_length=100,
        db_index=True,
    )
    module = models.CharField(
        max_length=100,
        db_index=True,
    )

    entity_type = models.CharField(
        max_length=150,
        blank=True,
    )
    entity_id = models.CharField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )
    user_agent = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("module", "action"),
            ),
            models.Index(
                fields=("entity_type", "entity_id"),
            ),
        ]

    def __str__(self):
        return f"{self.module}: {self.action}"
