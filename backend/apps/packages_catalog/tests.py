from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api
from apps.services_catalog.models import Service

from .models import (
    Package,
    PackageStatus,
)
from .services import PackageCatalogService


User = get_user_model()


class PackageCatalogApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="packages-admin",
            email="packages-admin@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(
            self.admin
        ).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

        self.service = Service.objects.create(
            title="Web Development",
            slug="web-development",
            created_by=self.admin,
            updated_by=self.admin,
        )

    def payload(self):
        return {
            "name": "Business Website Package",
            "slug": "business-website-package",
            "category": "website",
            "service_id": str(self.service.pk),
            "short_description": (
                "Complete website package for businesses."
            ),
            "description": {
                "summary": "Business website package.",
            },
            "pricing_type": "fixed",
            "price": "30000.00",
            "compare_at_price": "35000.00",
            "currency": "LKR",
            "billing_cycle": "one_time",
            "delivery_time": "3 to 5 working days",
            "revisions_included": 3,
            "support_period_days": 180,
            "status": "draft",
            "is_featured": True,
            "is_popular": True,
            "is_active": True,
            "sort_order": 1,
            "badge_text": "Most Popular",
            "cta_label": "Get Started",
            "cta_url": "/request-quote",
            "features": [
                {
                    "title": "Six Pages",
                    "description": (
                        "Up to six professionally designed pages."
                    ),
                    "is_included": True,
                    "value": "6",
                    "icon": "file",
                    "sort_order": 1,
                },
            ],
            "addons": [
                {
                    "name": "Additional Page",
                    "description": (
                        "Add another website page."
                    ),
                    "price": "5000.00",
                    "currency": "LKR",
                    "billing_cycle": "one_time",
                    "is_active": True,
                    "sort_order": 1,
                },
            ],
            "target_audiences": [
                {
                    "title": "Small Businesses",
                    "description": (
                        "Suitable for growing businesses."
                    ),
                    "sort_order": 1,
                },
            ],
            "faqs": [
                {
                    "question": (
                        "Does the package include hosting?"
                    ),
                    "answer": (
                        "Yes, one year of hosting is included."
                    ),
                    "sort_order": 1,
                },
            ],
            "seo": {
                "meta_title": (
                    "Business Website Package"
                ),
                "meta_description": (
                    "Affordable business website package."
                ),
                "robots_index": True,
                "robots_follow": True,
                "structured_data": {},
            },
        }

    def create_package(self):
        return self.client.post(
            "/packages",
            json=self.payload(),
            headers=self.headers,
        )

    def test_superuser_can_create_package(self):
        response = self.create_package()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["slug"],
            "business-website-package",
        )
        self.assertEqual(
            response.json()["price"],
            "30000.00",
        )
        self.assertEqual(
            response.json()["current_revision_number"],
            1,
        )
        self.assertEqual(
            len(response.json()["features"]),
            1,
        )

    def test_duplicate_slug_is_rejected(self):
        self.create_package()
        response = self.create_package()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "duplicate_package_slug",
        )

    def test_update_creates_revision(self):
        created = self.create_package().json()

        payload = self.payload()
        payload["name"] = (
            "Premium Business Website Package"
        )
        payload["price"] = "45000.00"
        payload["change_summary"] = (
            "Updated package pricing."
        )

        response = self.client.put(
            f"/packages/{created['id']}",
            json=payload,
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["current_revision_number"],
            2,
        )
        self.assertEqual(
            response.json()["price"],
            "45000.00",
        )

    def test_package_can_be_published(self):
        created = self.create_package().json()

        response = self.client.post(
            f"/packages/{created['id']}/publish",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            PackageStatus.PUBLISHED,
        )
        self.assertTrue(
            response.json()["is_publicly_available"]
        )

    def test_package_can_be_scheduled(self):
        created = self.create_package().json()

        response = self.client.post(
            f"/packages/{created['id']}/schedule",
            json={
                "scheduled_for": (
                    timezone.now()
                    + timedelta(days=1)
                ).isoformat(),
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            PackageStatus.SCHEDULED,
        )

    def test_past_schedule_is_rejected(self):
        created = self.create_package().json()

        response = self.client.post(
            f"/packages/{created['id']}/schedule",
            json={
                "scheduled_for": (
                    timezone.now()
                    - timedelta(minutes=5)
                ).isoformat(),
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "invalid_publish_schedule",
        )

    def test_due_scheduled_packages_are_published(self):
        package = Package.objects.create(
            name="Scheduled Package",
            slug="scheduled-package",
            status=PackageStatus.SCHEDULED,
            scheduled_for=(
                timezone.now() - timedelta(minutes=1)
            ),
            created_by=self.admin,
            updated_by=self.admin,
        )

        count = (
            PackageCatalogService
            .process_scheduled_packages()
        )

        package.refresh_from_db()

        self.assertEqual(count, 1)
        self.assertEqual(
            package.status,
            PackageStatus.PUBLISHED,
        )

    def test_package_can_be_soft_deleted(self):
        created = self.create_package().json()

        response = self.client.delete(
            f"/packages/{created['id']}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Package.objects.filter(
                pk=created["id"],
            ).exists()
        )
        self.assertTrue(
            Package.all_objects.filter(
                pk=created["id"],
            ).exists()
        )

    def test_unauthenticated_request_is_rejected(self):
        response = self.client.get("/packages")

        self.assertEqual(response.status_code, 401)
