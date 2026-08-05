from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api
from apps.clients.models import Client
from apps.industries.models import Industry
from apps.projects.models import Project
from apps.services_catalog.models import Service

from .models import (
    CaseStudy,
    CaseStudyStatus,
)
from .services import CaseStudyServiceLayer


User = get_user_model()


class CaseStudiesApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="case-study-admin",
            email="case-study-admin@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(
            self.admin
        ).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

        self.client_record = Client.objects.create(
            company_name="Example Client",
            client_code="LKP-CL-00800",
            created_by=self.admin,
            updated_by=self.admin,
        )

        self.project = Project.objects.create(
            project_code="LKP-PR-2026-00800",
            client=self.client_record,
            name="Example Website Project",
            created_by=self.admin,
            updated_by=self.admin,
        )

        self.industry = Industry.objects.create(
            name="Retail",
            slug="retail",
            created_by=self.admin,
            updated_by=self.admin,
        )

        self.service = Service.objects.create(
            title="Web Development",
            slug="web-development",
            created_by=self.admin,
            updated_by=self.admin,
        )

    def payload(self):
        return {
            "title": "Retail Website Transformation",
            "slug": "retail-website-transformation",
            "client_id": str(self.client_record.pk),
            "project_id": str(self.project.pk),
            "industry_id": str(self.industry.pk),
            "client_name": "Example Client",
            "location": "United Kingdom",
            "website_url": "https://example.com",
            "short_description": (
                "A complete retail website redesign."
            ),
            "overview": {
                "summary": "Retail website project.",
            },
            "challenge": {
                "summary": "Low conversion rate.",
            },
            "solution": {
                "summary": "Modern conversion-focused site.",
            },
            "implementation": {
                "summary": "Phased implementation.",
            },
            "results": {
                "summary": "Improved performance.",
            },
            "testimonial": "Excellent delivery.",
            "testimonial_author": "Example Director",
            "testimonial_position": "Managing Director",
            "status": "draft",
            "project_start_date": "2026-01-01",
            "project_completion_date": "2026-02-01",
            "project_duration": "One month",
            "is_featured": True,
            "is_active": True,
            "sort_order": 1,
            "services": [
                {
                    "service_id": str(self.service.pk),
                    "description": (
                        "Website design and development."
                    ),
                    "sort_order": 1,
                },
            ],
            "technologies": [
                {
                    "name": "Django",
                    "description": "Backend platform.",
                    "sort_order": 1,
                },
            ],
            "media_items": [],
            "metrics": [
                {
                    "label": "Performance",
                    "value": "95",
                    "description": "Lighthouse score.",
                    "icon": "gauge",
                    "sort_order": 1,
                },
            ],
            "milestones": [
                {
                    "title": "Launch",
                    "description": "Production launch.",
                    "milestone_date": "2026-02-01",
                    "sort_order": 1,
                },
            ],
            "seo": {
                "meta_title": (
                    "Retail Website Case Study"
                ),
                "meta_description": (
                    "A retail website transformation."
                ),
                "robots_index": True,
                "robots_follow": True,
                "structured_data": {},
            },
        }

    def create_case_study(self):
        return self.client.post(
            "/case-studies",
            json=self.payload(),
            headers=self.headers,
        )

    def test_create_case_study(self):
        response = self.create_case_study()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["slug"],
            "retail-website-transformation",
        )
        self.assertEqual(
            response.json()["current_revision_number"],
            1,
        )
        self.assertEqual(
            len(response.json()["services"]),
            1,
        )
        self.assertEqual(
            len(response.json()["metrics"]),
            1,
        )

    def test_duplicate_slug_is_rejected(self):
        self.create_case_study()
        response = self.create_case_study()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "duplicate_case_study_slug",
        )

    def test_update_creates_revision(self):
        created = self.create_case_study().json()

        payload = self.payload()
        payload["title"] = (
            "Retail Digital Transformation"
        )
        payload["change_summary"] = (
            "Improved case-study title."
        )

        response = self.client.put(
            f"/case-studies/{created['id']}",
            json=payload,
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["current_revision_number"],
            2,
        )

    def test_publish_case_study(self):
        created = self.create_case_study().json()

        response = self.client.post(
            f"/case-studies/{created['id']}/publish",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            CaseStudyStatus.PUBLISHED,
        )
        self.assertTrue(
            response.json()["is_publicly_available"]
        )

    def test_schedule_case_study(self):
        created = self.create_case_study().json()

        response = self.client.post(
            f"/case-studies/{created['id']}/schedule",
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
            CaseStudyStatus.SCHEDULED,
        )

    def test_past_schedule_is_rejected(self):
        created = self.create_case_study().json()

        response = self.client.post(
            f"/case-studies/{created['id']}/schedule",
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

    def test_due_case_study_is_published(self):
        case_study = CaseStudy.objects.create(
            title="Scheduled Case Study",
            slug="scheduled-case-study",
            status=CaseStudyStatus.SCHEDULED,
            scheduled_for=(
                timezone.now() - timedelta(minutes=1)
            ),
            created_by=self.admin,
            updated_by=self.admin,
        )

        count = (
            CaseStudyServiceLayer.process_scheduled()
        )

        case_study.refresh_from_db()

        self.assertEqual(count, 1)
        self.assertEqual(
            case_study.status,
            CaseStudyStatus.PUBLISHED,
        )

    def test_soft_delete_case_study(self):
        created = self.create_case_study().json()

        response = self.client.delete(
            f"/case-studies/{created['id']}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            CaseStudy.objects.filter(
                pk=created["id"],
            ).exists()
        )
        self.assertTrue(
            CaseStudy.all_objects.filter(
                pk=created["id"],
            ).exists()
        )

    def test_unauthenticated_request_is_rejected(self):
        response = self.client.get("/case-studies")

        self.assertEqual(response.status_code, 401)
