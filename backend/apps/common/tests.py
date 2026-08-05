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


from apps.common.pagination import paginate_queryset
from apps.common.query import (
    apply_ordering,
    apply_search,
)


class PaginationTests(TestCase):
    def setUp(self):
        for index in range(7):
            Role.objects.create(
                name=f"Pagination Role {index}",
                slug=f"pagination-role-{index}",
                priority=index,
            )

    def test_queryset_is_paginated(self):
        result = paginate_queryset(
            Role.objects.order_by("priority"),
            page=2,
            page_size=3,
        )

        self.assertEqual(len(result.items), 3)
        self.assertEqual(result.page, 2)
        self.assertEqual(result.page_size, 3)
        self.assertEqual(result.total_items, 7)
        self.assertEqual(result.total_pages, 3)

    def test_page_size_is_limited_to_one_hundred(self):
        result = paginate_queryset(
            Role.objects.all(),
            page=1,
            page_size=500,
        )

        self.assertEqual(result.page_size, 100)


class QueryUtilityTests(TestCase):
    def setUp(self):
        Role.objects.create(
            name="Sales Manager",
            slug="sales-manager",
            priority=20,
        )
        Role.objects.create(
            name="Developer",
            slug="developer-query",
            priority=10,
        )

    def test_search_across_multiple_fields(self):
        queryset = apply_search(
            Role.objects.all(),
            search="sales",
            fields=("name", "slug"),
        )

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(
            queryset.first().slug,
            "sales-manager",
        )

    def test_invalid_ordering_uses_default(self):
        queryset = apply_ordering(
            Role.objects.all(),
            ordering="invalid",
            allowed_fields=("name", "priority"),
            default="priority",
        )

        self.assertEqual(
            queryset.first().slug,
            "developer-query",
        )

    def test_descending_ordering_is_supported(self):
        queryset = apply_ordering(
            Role.objects.all(),
            ordering="-priority",
            allowed_fields=("name", "priority"),
            default="priority",
        )

        self.assertEqual(
            queryset.first().slug,
            "sales-manager",
        )


from apps.audit.models import AuditEventType, AuditLog
from apps.common.repositories import BaseRepository
from apps.common.services import BaseService


class RoleTestRepository(BaseRepository[Role]):
    model = Role


class BaseRepositoryTests(TestCase):
    def test_repository_create_and_find(self):
        role = RoleTestRepository.create(
            name="Repository Role",
            slug="repository-role",
        )

        found = RoleTestRepository.find_by_id(role.pk)

        self.assertEqual(found, role)
        self.assertTrue(
            RoleTestRepository.exists(
                slug="repository-role",
            )
        )


class BaseServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="base-service-admin",
            email="base-service@example.com",
            password="StrongPassword123!",
        )

        self.request = type(
            "Request",
            (),
            {
                "auth": self.user,
                "META": {},
            },
        )()

    def test_service_create_generates_audit_log(self):
        role = BaseService.create(
            request=self.request,
            model=Role,
            module="rbac",
            values={
                "name": "Service Role",
                "slug": "service-role",
            },
            audit_fields=[
                "name",
                "slug",
            ],
        )

        self.assertTrue(
            AuditLog.objects.filter(
                event_type=AuditEventType.RECORD_CREATED,
                target_id=str(role.pk),
            ).exists()
        )

    def test_service_update_generates_audit_log(self):
        role = Role.objects.create(
            name="Original Role",
            slug="original-role",
        )

        BaseService.update(
            request=self.request,
            instance=role,
            module="rbac",
            values={
                "name": "Updated Role",
            },
            audit_fields=[
                "name",
                "slug",
            ],
        )

        role.refresh_from_db()

        self.assertEqual(role.name, "Updated Role")

        self.assertTrue(
            AuditLog.objects.filter(
                event_type=AuditEventType.RECORD_UPDATED,
                target_id=str(role.pk),
            ).exists()
        )

    def test_service_soft_delete_generates_audit_log(self):
        role = Role.objects.create(
            name="Deleted Role",
            slug="deleted-role",
        )

        BaseService.soft_delete(
            request=self.request,
            instance=role,
            module="rbac",
            audit_fields=[
                "name",
                "slug",
            ],
        )

        self.assertFalse(
            Role.objects.filter(pk=role.pk).exists()
        )
        self.assertTrue(
            Role.all_objects.filter(pk=role.pk).exists()
        )

        self.assertTrue(
            AuditLog.objects.filter(
                event_type=AuditEventType.RECORD_DELETED,
                target_id=str(role.pk),
            ).exists()
        )
