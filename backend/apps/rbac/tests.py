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
