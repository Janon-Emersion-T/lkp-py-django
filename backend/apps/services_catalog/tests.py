from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api

from .models import (
    Service,
    ServiceStatus,
)
from .services import ServiceCatalogService


User = get_user_model()


class ServiceCatalogApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="services-admin",
            email="services-admin@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(
            self.admin
        ).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

    def payload(self):
        return {
            "title": "Web Development",
            "slug": "web-development",
            "short_description": (
                "Professional website development."
            ),
            "description": {
                "introduction": (
                    "Enterprise website development."
                ),
            },
            "hero_title": "Web Development Services",
            "hero_description": (
                "Build a fast and reliable website."
            ),
            "status": "draft",
            "icon": "globe",
            "sort_order": 1,
            "is_featured": True,
            "is_active": True,
            "cta_title": "Start Your Project",
            "cta_text": "Request a quotation today.",
            "cta_label": "Get a Quote",
            "cta_url": "/request-quote",
            "features": [
                {
                    "title": "SEO Friendly",
                    "description": (
                        "Built for search visibility."
                    ),
                    "icon": "search",
                    "sort_order": 1,
                },
            ],
            "process_steps": [
                {
                    "title": "Discovery",
                    "description": (
                        "Understand business requirements."
                    ),
                    "step_number": 1,
                    "sort_order": 1,
                },
            ],
            "technologies": [
                {
                    "name": "Django",
                    "description": (
                        "Enterprise Python backend."
                    ),
                    "sort_order": 1,
                },
            ],
            "faqs": [
                {
                    "question": (
                        "How long does a website take?"
                    ),
                    "answer": (
                        "The timeline depends on scope."
                    ),
                    "sort_order": 1,
                },
            ],
            "seo": {
                "meta_title": (
                    "Web Development Services"
                ),
                "meta_description": (
                    "Professional web development."
                ),
                "robots_index": True,
                "robots_follow": True,
                "structured_data": {},
            },
        }

    def create_service(self):
        return self.client.post(
            "/services",
            json=self.payload(),
            headers=self.headers,
        )

    def test_superuser_can_create_service(self):
        response = self.create_service()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["slug"],
            "web-development",
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
        self.create_service()
        response = self.create_service()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "duplicate_service_slug",
        )

    def test_update_creates_new_revision(self):
        created = self.create_service().json()

        payload = self.payload()
        payload["title"] = "Enterprise Web Development"
        payload["change_summary"] = "Updated title."

        response = self.client.put(
            f"/services/{created['id']}",
            json=payload,
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["current_revision_number"],
            2,
        )
        self.assertEqual(
            response.json()["title"],
            "Enterprise Web Development",
        )

    def test_service_can_be_published(self):
        created = self.create_service().json()

        response = self.client.post(
            f"/services/{created['id']}/publish",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            ServiceStatus.PUBLISHED,
        )
        self.assertTrue(
            response.json()["is_publicly_available"]
        )

    def test_service_can_be_scheduled(self):
        created = self.create_service().json()

        response = self.client.post(
            f"/services/{created['id']}/schedule",
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
            ServiceStatus.SCHEDULED,
        )

    def test_past_schedule_is_rejected(self):
        created = self.create_service().json()

        response = self.client.post(
            f"/services/{created['id']}/schedule",
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

    def test_due_scheduled_services_are_published(self):
        service = Service.objects.create(
            title="Scheduled Service",
            slug="scheduled-service",
            status=ServiceStatus.SCHEDULED,
            scheduled_for=(
                timezone.now() - timedelta(minutes=1)
            ),
            created_by=self.admin,
            updated_by=self.admin,
        )

        count = (
            ServiceCatalogService
            .process_scheduled_services()
        )

        service.refresh_from_db()

        self.assertEqual(count, 1)
        self.assertEqual(
            service.status,
            ServiceStatus.PUBLISHED,
        )

    def test_service_can_be_soft_deleted(self):
        created = self.create_service().json()

        response = self.client.delete(
            f"/services/{created['id']}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Service.objects.filter(
                pk=created["id"],
            ).exists()
        )
        self.assertTrue(
            Service.all_objects.filter(
                pk=created["id"],
            ).exists()
        )

    def test_unauthenticated_request_is_rejected(self):
        response = self.client.get("/services")

        self.assertEqual(response.status_code, 401)
