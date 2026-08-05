from django.conf import settings
from django.db import models


class AuditEventType(models.TextChoices):
    LOGIN_SUCCESS = "login_success", "Login success"
    LOGIN_FAILED = "login_failed", "Login failed"
    LOGOUT = "logout", "Logout"
    PASSWORD_CHANGED = "password_changed", "Password changed"
    ROLE_ASSIGNED = "role_assigned", "Role assigned"
    ROLE_REMOVED = "role_removed", "Role removed"
    PERMISSION_CHANGED = "permission_changed", "Permission changed"
    RECORD_CREATED = "record_created", "Record created"
    RECORD_UPDATED = "record_updated", "Record updated"
    RECORD_DELETED = "record_deleted", "Record deleted"
    SECURITY_EVENT = "security_event", "Security event"


class AuditSeverity(models.TextChoices):
    INFO = "info", "Information"
    WARNING = "warning", "Warning"
    CRITICAL = "critical", "Critical"


class AuditLog(models.Model):
    id = models.BigAutoField(primary_key=True)

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
    )

    event_type = models.CharField(
        max_length=50,
        choices=AuditEventType.choices,
        db_index=True,
    )
    severity = models.CharField(
        max_length=20,
        choices=AuditSeverity.choices,
        default=AuditSeverity.INFO,
        db_index=True,
    )

    module = models.CharField(
        max_length=100,
        db_index=True,
    )
    target_type = models.CharField(
        max_length=150,
        blank=True,
    )
    target_id = models.CharField(
        max_length=100,
        blank=True,
    )

    message = models.TextField()
    before = models.JSONField(
        null=True,
        blank=True,
    )
    after = models.JSONField(
        null=True,
        blank=True,
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

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
                fields=("module", "event_type"),
            ),
            models.Index(
                fields=("target_type", "target_id"),
            ),
            models.Index(
                fields=("severity", "created_at"),
            ),
        ]

    def __str__(self):
        return f"{self.event_type}: {self.message[:80]}"

    def save(self, *args, **kwargs):
        if self.pk and AuditLog.objects.filter(pk=self.pk).exists():
            raise RuntimeError("Audit log records are immutable")

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise RuntimeError("Audit log records cannot be deleted")
