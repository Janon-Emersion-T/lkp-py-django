from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Role, UserRole


User = get_user_model()


class RoleModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="rbac-admin",
            email="rbac@example.com",
            password="StrongPassword123!",
        )
        self.role = Role.objects.create(
            name="Manager",
            slug="manager",
            priority=20,
            is_system=True,
        )

    def test_role_string_representation(self):
        self.assertEqual(str(self.role), "Manager")

    def test_duplicate_active_assignment_is_rejected(self):
        UserRole.objects.create(
            user=self.user,
            role=self.role,
            assigned_by=self.user,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                UserRole.objects.create(
                    user=self.user,
                    role=self.role,
                    assigned_by=self.user,
                )

    def test_soft_deleted_assignment_can_be_recreated(self):
        assignment = UserRole.objects.create(
            user=self.user,
            role=self.role,
            assigned_by=self.user,
        )

        assignment.delete()

        recreated = UserRole.objects.create(
            user=self.user,
            role=self.role,
            assigned_by=self.user,
        )

        self.assertNotEqual(assignment.pk, recreated.pk)


class PermissionServiceTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import Permission

        from apps.rbac.services import user_has_permission

        self.user_has_permission = user_has_permission

        self.user = User.objects.create_user(
            username="permission-user",
            email="permission@example.com",
            password="StrongPassword123!",
        )

        self.role = Role.objects.create(
            name="Permission Test Role",
            slug="permission-test-role",
        )

        self.permission = Permission.objects.get(
            content_type__app_label="accounts",
            codename="view_user",
        )

    def test_role_permission_is_respected(self):
        self.role.permissions.add(self.permission)

        UserRole.objects.create(
            user=self.user,
            role=self.role,
        )

        self.assertTrue(
            self.user_has_permission(
                self.user,
                "accounts.view_user",
            )
        )

    def test_unassigned_permission_is_rejected(self):
        self.assertFalse(
            self.user_has_permission(
                self.user,
                "accounts.view_user",
            )
        )

    def test_superuser_bypasses_role_permissions(self):
        superuser = User.objects.create_superuser(
            username="permission-superuser",
            email="superuser@example.com",
            password="StrongPassword123!",
        )

        self.assertTrue(
            self.user_has_permission(
                superuser,
                "accounts.view_user",
            )
        )


class SeedRolesCommandTests(TestCase):
    def test_seed_roles_creates_all_default_roles(self):
        from django.core.management import call_command

        from apps.rbac.constants import DEFAULT_ROLES

        call_command("seed_roles")

        self.assertEqual(
            Role.objects.filter(is_system=True).count(),
            len(DEFAULT_ROLES),
        )

    def test_seed_roles_is_idempotent(self):
        from django.core.management import call_command

        from apps.rbac.constants import DEFAULT_ROLES

        call_command("seed_roles")
        call_command("seed_roles")

        self.assertEqual(
            Role.objects.filter(is_system=True).count(),
            len(DEFAULT_ROLES),
        )

    def test_super_admin_receives_all_permissions(self):
        from django.contrib.auth.models import Permission
        from django.core.management import call_command

        call_command("seed_roles")

        role = Role.objects.get(slug="super-admin")

        self.assertEqual(
            role.permissions.count(),
            Permission.objects.count(),
        )


from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api
from apps.audit.models import AuditEventType, AuditLog


class RbacApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="rbac-api-admin",
            email="rbac-api-admin@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(self.admin).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

        self.role = Role.objects.create(
            name="RBAC API Role",
            slug="rbac-api-role",
            priority=30,
        )

    def test_superuser_can_list_roles(self):
        response = self.client.get(
            "/rbac/roles",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        role_slugs = [
            role["slug"]
            for role in response.json()
        ]

        self.assertIn("rbac-api-role", role_slugs)

    def test_superuser_can_list_permissions(self):
        response = self.client.get(
            "/rbac/permissions",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

    def test_superuser_can_update_role_permissions(self):
        from django.contrib.auth.models import Permission

        permission = Permission.objects.get(
            content_type__app_label="accounts",
            codename="view_user",
        )

        response = self.client.put(
            f"/rbac/roles/{self.role.pk}",
            json={
                "description": "Updated role",
                "priority": 25,
                "is_active": True,
                "permission_ids": [permission.id],
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        self.role.refresh_from_db()

        self.assertEqual(
            self.role.description,
            "Updated role",
        )
        self.assertEqual(self.role.priority, 25)
        self.assertTrue(
            self.role.permissions.filter(
                pk=permission.pk,
            ).exists()
        )

        self.assertTrue(
            AuditLog.objects.filter(
                actor=self.admin,
                event_type=AuditEventType.PERMISSION_CHANGED,
                target_id=str(self.role.pk),
            ).exists()
        )

    def test_superuser_can_assign_role_to_user(self):
        user = User.objects.create_user(
            username="role-target",
            email="role-target@example.com",
            password="StrongPassword123!",
        )

        response = self.client.post(
            f"/rbac/users/{user.pk}/roles",
            json={
                "role_id": str(self.role.pk),
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            UserRole.objects.filter(
                user=user,
                role=self.role,
                is_active=True,
            ).exists()
        )

        self.assertTrue(
            AuditLog.objects.filter(
                actor=self.admin,
                event_type=AuditEventType.ROLE_ASSIGNED,
                target_id=str(user.pk),
            ).exists()
        )

    def test_unauthenticated_role_request_is_rejected(self):
        response = self.client.get("/rbac/roles")

        self.assertEqual(response.status_code, 401)
