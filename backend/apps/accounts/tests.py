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
