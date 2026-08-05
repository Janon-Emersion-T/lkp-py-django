from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.rbac.models import Role


User = get_user_model()


class BaseModelSoftDeleteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="soft-delete-admin",
            email="soft-delete@example.com",
            password="StrongPassword123!",
        )

    def test_soft_delete_hides_record_from_default_manager(self):
        role = Role.objects.create(
            name="Temporary Role",
            slug="temporary-role",
            created_by=self.user,
        )

        role.delete()

        self.assertFalse(Role.objects.filter(pk=role.pk).exists())
        self.assertTrue(Role.all_objects.filter(pk=role.pk).exists())

    def test_restore_returns_record_to_default_manager(self):
        role = Role.objects.create(
            name="Restorable Role",
            slug="restorable-role",
            created_by=self.user,
        )

        role.delete()
        role.restore()

        self.assertTrue(Role.objects.filter(pk=role.pk).exists())
        self.assertFalse(role.is_deleted)
        self.assertIsNone(role.deleted_at)
