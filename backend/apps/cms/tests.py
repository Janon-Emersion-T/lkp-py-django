from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api

from .models import (
    ContentStatus,
    Page,
    PageRevision,
    Redirect,
)
from .services import CmsService


User = get_user_model()


class CmsApiTests(TestCase):
    def setUp(self):
        self.api_client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="cms-admin",
            email="cms-admin@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(
            self.admin
        ).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

    def create_page(self):
        return self.api_client.post(
            "/cms/pages",
            json={
                "title": "About LKProfessionals",
                "slug": "about",
                "page_type": "about",
                "status": "draft",
                "excerpt": "About the company.",
                "content": {
                    "hero": {
                        "heading": "About Us",
                    },
                },
                "template_name": "pages/about.html",
                "is_indexable": True,
                "is_visible_in_navigation": True,
                "navigation_label": "About",
                "navigation_order": 2,
                "seo": {
                    "meta_title": "About LKProfessionals",
                    "meta_description": (
                        "Learn about LKProfessionals."
                    ),
                    "robots_index": True,
                    "robots_follow": True,
                    "structured_data": {},
                },
            },
            headers=self.headers,
        )

    def test_superuser_can_create_page(self):
        response = self.create_page()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["slug"], "about")
        self.assertEqual(
            response.json()["current_revision_number"],
            1,
        )
        self.assertEqual(
            len(response.json()["revisions"]),
            1,
        )

    def test_duplicate_slug_is_rejected(self):
        self.create_page()

        response = self.create_page()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "duplicate_page_slug",
        )

    def test_page_update_creates_revision(self):
        created = self.create_page().json()

        response = self.api_client.put(
            f"/cms/pages/{created['id']}",
            json={
                "title": "About Our Company",
                "slug": "about",
                "page_type": "about",
                "status": "draft",
                "excerpt": "Updated company information.",
                "content": {
                    "hero": {
                        "heading": "Our Company",
                    },
                },
                "template_name": "pages/about.html",
                "is_indexable": True,
                "is_visible_in_navigation": True,
                "navigation_label": "About",
                "navigation_order": 2,
                "change_summary": "Updated hero content.",
                "seo": {
                    "meta_title": "About Our Company",
                    "meta_description": (
                        "Updated company information."
                    ),
                    "robots_index": True,
                    "robots_follow": True,
                    "structured_data": {},
                },
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["current_revision_number"],
            2,
        )
        self.assertEqual(
            len(response.json()["revisions"]),
            2,
        )

    def test_page_can_be_published(self):
        created = self.create_page().json()

        response = self.api_client.post(
            f"/cms/pages/{created['id']}/publish",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            ContentStatus.PUBLISHED,
        )
        self.assertTrue(
            response.json()["is_publicly_available"]
        )

    def test_future_publication_can_be_scheduled(self):
        created = self.create_page().json()

        scheduled_for = (
            timezone.now() + timedelta(days=1)
        )

        response = self.api_client.post(
            f"/cms/pages/{created['id']}/schedule",
            json={
                "scheduled_for": (
                    scheduled_for.isoformat()
                ),
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            ContentStatus.SCHEDULED,
        )

    def test_past_schedule_is_rejected(self):
        created = self.create_page().json()

        response = self.api_client.post(
            f"/cms/pages/{created['id']}/schedule",
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

    def test_revision_can_be_restored(self):
        created = self.create_page().json()

        original_revision = created["revisions"][0]

        self.api_client.put(
            f"/cms/pages/{created['id']}",
            json={
                "title": "Changed Title",
                "slug": "about",
                "page_type": "about",
                "status": "draft",
                "excerpt": "",
                "content": {},
                "template_name": "pages/about.html",
                "is_indexable": True,
                "is_visible_in_navigation": True,
                "navigation_label": "About",
                "navigation_order": 2,
                "change_summary": "Temporary change.",
                "seo": {
                    "robots_index": True,
                    "robots_follow": True,
                    "structured_data": {},
                },
            },
            headers=self.headers,
        )

        response = self.api_client.post(
            f"/cms/pages/{created['id']}/restore",
            json={
                "revision_id": original_revision["id"],
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["title"],
            "About LKProfessionals",
        )

    def test_scheduled_pages_are_processed(self):
        page = Page.objects.create(
            title="Scheduled Page",
            slug="scheduled-page",
            status=ContentStatus.SCHEDULED,
            scheduled_for=(
                timezone.now() - timedelta(minutes=1)
            ),
            created_by=self.admin,
            updated_by=self.admin,
        )

        count = CmsService.process_scheduled_pages()

        page.refresh_from_db()

        self.assertEqual(count, 1)
        self.assertEqual(
            page.status,
            ContentStatus.PUBLISHED,
        )
        self.assertIsNotNone(page.published_at)

    def test_redirect_can_be_created(self):
        response = self.api_client.post(
            "/cms/redirects",
            json={
                "source_path": "/portfolio",
                "destination_url": "/case-studies",
                "redirect_type": 308,
                "is_active": True,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Redirect.objects.filter(
                source_path="/portfolio",
            ).exists()
        )

    def test_page_can_be_soft_deleted(self):
        created = self.create_page().json()

        response = self.api_client.delete(
            f"/cms/pages/{created['id']}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Page.objects.filter(
                pk=created["id"],
            ).exists()
        )
        self.assertTrue(
            Page.all_objects.filter(
                pk=created["id"],
            ).exists()
        )

    def test_unauthenticated_request_is_rejected(self):
        response = self.api_client.get("/cms/pages")

        self.assertEqual(response.status_code, 401)


class CmsRevisionTests(TestCase):
    def test_revision_numbers_are_unique_per_page(self):
        user = User.objects.create_superuser(
            username="revision-admin",
            email="revision-admin@example.com",
            password="StrongPassword123!",
        )

        page = Page.objects.create(
            title="Revision Page",
            slug="revision-page",
            created_by=user,
            updated_by=user,
        )

        first = CmsService.create_revision(
            page=page,
            actor=user,
        )
        second = CmsService.create_revision(
            page=page,
            actor=user,
        )

        self.assertEqual(first.revision_number, 1)
        self.assertEqual(second.revision_number, 2)

        self.assertEqual(
            PageRevision.objects.filter(
                page=page,
            ).count(),
            2,
        )
