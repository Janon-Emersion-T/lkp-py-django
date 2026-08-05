from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import AuditEventType, AuditLog, AuditSeverity


User = get_user_model()


class AuditLogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="audit-admin",
            email="audit@example.com",
            password="StrongPassword123!",
        )

    def test_audit_log_can_be_created(self):
        event = AuditLog.objects.create(
            actor=self.user,
            event_type=AuditEventType.SECURITY_EVENT,
            severity=AuditSeverity.WARNING,
            module="system",
            message="Test security event",
        )

        self.assertIsNotNone(event.pk)

    def test_audit_log_cannot_be_updated(self):
        event = AuditLog.objects.create(
            actor=self.user,
            event_type=AuditEventType.SECURITY_EVENT,
            severity=AuditSeverity.INFO,
            module="system",
            message="Original message",
        )

        event.message = "Changed message"

        with self.assertRaises(RuntimeError):
            event.save()

    def test_audit_log_cannot_be_deleted(self):
        event = AuditLog.objects.create(
            actor=self.user,
            event_type=AuditEventType.SECURITY_EVENT,
            severity=AuditSeverity.INFO,
            module="system",
            message="Protected event",
        )

        with self.assertRaises(RuntimeError):
            event.delete()
