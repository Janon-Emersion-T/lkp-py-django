from django.contrib.auth import get_user_model
from django.test import TestCase
from ninja.testing import TestClient

from apps.activity.models import ActivityLog
from apps.audit.models import AuditEventType, AuditLog

from .api import api


User = get_user_model()


class AuthenticationAuditTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.user = User.objects.create_user(
            username="api-user",
            email="api@example.com",
            password="StrongPassword123!",
        )

    def test_successful_login_creates_activity_and_audit_records(self):
        response = self.client.post(
            "/auth/login",
            json={
                "email": self.user.email,
                "password": "StrongPassword123!",
            },
            headers={
                "User-Agent": "LKProfessionals Test Client",
                "X-Forwarded-For": "192.0.2.10",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            AuditLog.objects.filter(
                actor=self.user,
                event_type=AuditEventType.LOGIN_SUCCESS,
            ).exists()
        )

        self.assertTrue(
            ActivityLog.objects.filter(
                actor=self.user,
                action="login",
            ).exists()
        )

    def test_failed_login_creates_security_audit_record(self):
        response = self.client.post(
            "/auth/login",
            json={
                "email": self.user.email,
                "password": "incorrect-password",
            },
        )

        self.assertEqual(response.status_code, 401)

        event = AuditLog.objects.get(
            event_type=AuditEventType.LOGIN_FAILED,
        )

        self.assertEqual(
            event.metadata["email"],
            self.user.email,
        )


class SystemEndpointTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(
            response.json()["service"],
            "lkprofessionals-api",
        )

    def test_readiness_endpoint(self):
        response = self.client.get("/ready")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["database"], "ok")


class ApiErrorResponseTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.user = User.objects.create_user(
            username="error-user",
            email="error@example.com",
            password="StrongPassword123!",
        )

    def test_invalid_login_uses_standard_error_response(self):
        response = self.client.post(
            "/auth/login",
            json={
                "email": self.user.email,
                "password": "incorrect",
            },
        )

        self.assertEqual(response.status_code, 401)

        body = response.json()

        self.assertEqual(body["status"], "error")
        self.assertEqual(body["code"], "invalid_credentials")
        self.assertIn("message", body)


class AuthenticationRateLimitTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

    def test_login_rate_limit(self):
        for index in range(10):
            response = self.client.post(
                "/auth/login",
                json={
                    "email": f"user{index}@example.com",
                    "password": "incorrect",
                },
                headers={
                    "X-Forwarded-For": "192.0.2.50",
                },
            )

            self.assertEqual(response.status_code, 401)

        response = self.client.post(
            "/auth/login",
            json={
                "email": "blocked@example.com",
                "password": "incorrect",
            },
            headers={
                "X-Forwarded-For": "192.0.2.50",
            },
        )

        self.assertEqual(response.status_code, 429)
        self.assertEqual(
            response.json()["code"],
            "rate_limit_exceeded",
        )
