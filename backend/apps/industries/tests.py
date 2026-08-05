from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api
from apps.services_catalog.models import Service

from .models import Industry, IndustryStatus
from .services import IndustryServiceLayer


User = get_user_model()


class IndustryApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="industry-admin",
            email="industry-admin@example.com",
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
            "name": "Healthcare",
            "slug": "healthcare",
            "short_description": (
                "Technology solutions for healthcare."
            ),
            "description": {
                "summary": "Healthcare technology.",
            },
            "hero_title": "Healthcare IT Solutions",
            "hero_description": (
                "Secure and scalable healthcare systems."
            ),
            "icon": "heart-pulse",
            "status": "draft",
            "is_featured": True,
            "is_active": True,
            "sort_order": 1,
            "challenges": [
                "Data security",
                "Regulatory compliance",
            ],
            "solutions": [
                "Secure software",
                "Workflow automation",
            ],
            "benefits": [
                "Improved efficiency",
                "Reliable operations",
            ],
            "cta_title": "Discuss Your Project",
            "cta_text": "Speak with our team.",
            "cta_label": "Contact Us",
            "cta_url": "/contact",
            "services": [
                {
                    "service_id": str(self.service.pk),
                    "description": (
                        "Healthcare website development."
                    ),
                    "sort_order": 1,
                    "is_featured": True,
                },
            ],
            "faqs": [
                {
                    "question": (
                        "Do you build healthcare systems?"
                    ),
                    "answer": (
                        "Yes, based on project requirements."
                    ),
                    "sort_order": 1,
                },
            ],
            "seo": {
                "meta_title": "Healthcare IT Solutions",
                "meta_description": (
                    "Technology services for healthcare."
                ),
                "robots_index": True,
                "robots_follow": True,
                "structured_data": {},
            },
        }

    def create_industry(self):
        return self.client.post(
            "/industries",
            json=self.payload(),
            headers=self.headers,
        )

    def test_create_industry(self):
        response = self.create_industry()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["slug"],
            "healthcare",
        )
        self.assertEqual(
            response.json()["current_revision_number"],
            1,
        )
        self.assertEqual(
            len(response.json()["services"]),
            1,
        )

    def test_duplicate_slug_is_rejected(self):
        self.create_industry()
        response = self.create_industry()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "duplicate_industry_slug",
        )

    def test_update_creates_revision(self):
        created = self.create_industry().json()

        payload = self.payload()
        payload["name"] = "Healthcare Technology"
        payload["change_summary"] = "Updated title."

        response = self.client.put(
            f"/industries/{created['id']}",
            json=payload,
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["current_revision_number"],
            2,
        )

    def test_publish_industry(self):
        created = self.create_industry().json()

        response = self.client.post(
            f"/industries/{created['id']}/publish",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            IndustryStatus.PUBLISHED,
        )
        self.assertTrue(
            response.json()["is_publicly_available"]
        )

    def test_schedule_industry(self):
        created = self.create_industry().json()

        response = self.client.post(
            f"/industries/{created['id']}/schedule",
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
            IndustryStatus.SCHEDULED,
        )

    def test_past_schedule_is_rejected(self):
        created = self.create_industry().json()

        response = self.client.post(
            f"/industries/{created['id']}/schedule",
            json={
                "scheduled_for": (
                    timezone.now()
                    - timedelta(minutes=5)
                ).isoformat(),
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)

    def test_due_industry_is_published(self):
        industry = Industry.objects.create(
            name="Scheduled Industry",
            slug="scheduled-industry",
            status=IndustryStatus.SCHEDULED,
            scheduled_for=(
                timezone.now() - timedelta(minutes=1)
            ),
            created_by=self.admin,
            updated_by=self.admin,
        )

        count = (
            IndustryServiceLayer
            .process_scheduled_industries()
        )

        industry.refresh_from_db()

        self.assertEqual(count, 1)
        self.assertEqual(
            industry.status,
            IndustryStatus.PUBLISHED,
        )

    def test_soft_delete_industry(self):
        created = self.create_industry().json()

        response = self.client.delete(
            f"/industries/{created['id']}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Industry.objects.filter(
                pk=created["id"],
            ).exists()
        )
        self.assertTrue(
            Industry.all_objects.filter(
                pk=created["id"],
            ).exists()
        )

    def test_unauthenticated_request_is_rejected(self):
        response = self.client.get("/industries")

        self.assertEqual(response.status_code, 401)
