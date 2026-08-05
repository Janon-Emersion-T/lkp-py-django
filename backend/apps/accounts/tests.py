from django.test import TestCase

# Create your tests here.


from django.contrib.auth import get_user_model
from django.test import TestCase
from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api
from apps.audit.models import AuditEventType, AuditLog
from apps.rbac.models import Role, UserRole


User = get_user_model()


class UsersApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="users-api-admin",
            email="users-api-admin@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(self.admin).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

    def test_superuser_can_list_users(self):
        response = self.client.get(
            "/users",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_superuser_can_create_user(self):
        role = Role.objects.create(
            name="API Developer",
            slug="api-developer",
        )

        response = self.client.post(
            "/users",
            json={
                "email": "created-user@example.com",
                "username": "created-user",
                "password": "StrongPassword123!",
                "first_name": "Created",
                "last_name": "User",
                "phone": "+94770000000",
                "job_title": "Developer",
                "department": "Engineering",
                "role_ids": [str(role.id)],
                "is_active": True,
                "is_staff": False,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)

        created_user = User.objects.get(
            email="created-user@example.com",
        )

        self.assertTrue(
            UserRole.objects.filter(
                user=created_user,
                role=role,
                is_active=True,
            ).exists()
        )

        self.assertTrue(
            AuditLog.objects.filter(
                actor=self.admin,
                event_type=AuditEventType.RECORD_CREATED,
                target_id=str(created_user.pk),
            ).exists()
        )

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(
            username="existing-user",
            email="existing@example.com",
            password="StrongPassword123!",
        )

        response = self.client.post(
            "/users",
            json={
                "email": "existing@example.com",
                "username": "different-username",
                "password": "StrongPassword123!",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "invalid_user",
        )

    def test_superuser_can_update_user(self):
        user = User.objects.create_user(
            username="update-user",
            email="update@example.com",
            password="StrongPassword123!",
        )

        response = self.client.put(
            f"/users/{user.pk}",
            json={
                "first_name": "Updated",
                "last_name": "Person",
                "phone": "+94771111111",
                "job_title": "Senior Developer",
                "department": "Engineering",
                "timezone": "Asia/Colombo",
                "preferred_language": "en",
                "is_active": True,
                "is_staff": True,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()

        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.job_title, "Senior Developer")
        self.assertTrue(user.is_staff)

    def test_superuser_can_soft_delete_another_user(self):
        user = User.objects.create_user(
            username="delete-user",
            email="delete@example.com",
            password="StrongPassword123!",
        )

        response = self.client.delete(
            f"/users/{user.pk}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()

        self.assertTrue(user.is_deleted)
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user.deleted_at)

    def test_user_cannot_delete_own_account(self):
        response = self.client.delete(
            f"/users/{self.admin.pk}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "invalid_user_operation",
        )

    def test_unauthenticated_request_is_rejected(self):
        response = self.client.get("/users")

        self.assertEqual(response.status_code, 401)


import pyotp
from datetime import timedelta
from django.utils import timezone

from apps.accounts.security_services import (
    LOCKOUT_MINUTES,
    MAX_FAILED_ATTEMPTS,
)


class AccountSecurityApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.user = User.objects.create_user(
            username="security-user",
            email="security@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(self.user).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

    def test_authenticated_user_can_change_password(self):
        response = self.client.post(
            "/security/change-password",
            json={
                "current_password": "StrongPassword123!",
                "new_password": "NewStrongPassword456!",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.check_password(
                "NewStrongPassword456!",
            )
        )
        self.assertFalse(self.user.must_change_password)
        self.assertIsNotNone(
            self.user.last_password_change_at
        )

    def test_incorrect_current_password_is_rejected(self):
        response = self.client.post(
            "/security/change-password",
            json={
                "current_password": "incorrect",
                "new_password": "NewStrongPassword456!",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "invalid_current_password",
        )

    def test_two_factor_setup_returns_secret_and_uri(self):
        response = self.client.post(
            "/security/two-factor/setup",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["secret"])
        self.assertIn(
            "otpauth://totp/",
            response.json()["provisioning_uri"],
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.two_factor_secret,
            response.json()["secret"],
        )

    def test_two_factor_can_be_enabled_and_disabled(self):
        setup_response = self.client.post(
            "/security/two-factor/setup",
            headers=self.headers,
        )

        secret = setup_response.json()["secret"]
        code = pyotp.TOTP(secret).now()

        enable_response = self.client.post(
            "/security/two-factor/enable",
            json={"code": code},
            headers=self.headers,
        )

        self.assertEqual(enable_response.status_code, 200)
        self.assertTrue(enable_response.json()["enabled"])

        self.user.refresh_from_db()
        self.assertTrue(self.user.two_factor_enabled)

        disable_code = pyotp.TOTP(
            self.user.two_factor_secret
        ).now()

        disable_response = self.client.post(
            "/security/two-factor/disable",
            json={"code": disable_code},
            headers=self.headers,
        )

        self.assertEqual(
            disable_response.status_code,
            200,
        )
        self.assertFalse(
            disable_response.json()["enabled"]
        )

        self.user.refresh_from_db()
        self.assertFalse(self.user.two_factor_enabled)
        self.assertEqual(self.user.two_factor_secret, "")

    def test_standard_login_requires_two_factor_code(self):
        self.user.two_factor_enabled = True
        self.user.two_factor_secret = pyotp.random_base32()
        self.user.save(
            update_fields=[
                "two_factor_enabled",
                "two_factor_secret",
            ],
        )

        response = self.client.post(
            "/auth/login",
            json={
                "email": self.user.email,
                "password": "StrongPassword123!",
            },
            headers={
                "X-Forwarded-For": "192.0.2.80",
            },
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()["code"],
            "two_factor_required",
        )
        self.assertNotIn("access", response.json())

    def test_two_factor_login_returns_tokens(self):
        secret = pyotp.random_base32()

        self.user.two_factor_enabled = True
        self.user.two_factor_secret = secret
        self.user.save(
            update_fields=[
                "two_factor_enabled",
                "two_factor_secret",
            ],
        )

        response = self.client.post(
            "/security/two-factor/login",
            json={
                "email": self.user.email,
                "password": "StrongPassword123!",
                "code": pyotp.TOTP(secret).now(),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_failed_logins_lock_account(self):
        for attempt in range(MAX_FAILED_ATTEMPTS):
            response = self.client.post(
                "/auth/login",
                json={
                    "email": self.user.email,
                    "password": "incorrect-password",
                },
                headers={
                    "X-Forwarded-For": (
                        f"198.51.100.{attempt + 1}"
                    ),
                },
            )

            self.assertEqual(response.status_code, 401)

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.failed_login_attempts,
            MAX_FAILED_ATTEMPTS,
        )
        self.assertIsNotNone(self.user.locked_until)
        self.assertGreater(
            self.user.locked_until,
            timezone.now(),
        )

        locked_response = self.client.post(
            "/auth/login",
            json={
                "email": self.user.email,
                "password": "StrongPassword123!",
            },
            headers={
                "X-Forwarded-For": "203.0.113.90",
            },
        )

        self.assertEqual(locked_response.status_code, 423)
        self.assertEqual(
            locked_response.json()["code"],
            "account_locked",
        )

    def test_expired_lock_is_cleared_on_successful_login(self):
        self.user.failed_login_attempts = MAX_FAILED_ATTEMPTS
        self.user.locked_until = (
            timezone.now()
            - timedelta(
                minutes=LOCKOUT_MINUTES,
            )
        )
        self.user.save(
            update_fields=[
                "failed_login_attempts",
                "locked_until",
            ],
        )

        response = self.client.post(
            "/auth/login",
            json={
                "email": self.user.email,
                "password": "StrongPassword123!",
            },
            headers={
                "X-Forwarded-For": "203.0.113.91",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.failed_login_attempts,
            0,
        )
        self.assertIsNone(self.user.locked_until)
