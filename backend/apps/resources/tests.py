from django.test import TestCase
from django.utils import timezone
from ninja.testing import TestClient

from .api import router
from .models import (
    Resource,
    ResourceStatus,
    ResourceType,
)


class PublicResourceApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(router)

    def create_resource(
        self,
        *,
        slug="business-guide",
        resource_type=ResourceType.GUIDE,
        status=ResourceStatus.PUBLISHED,
        published_at=None,
        is_active=True,
    ):
        return Resource.objects.create(
            title="Business Guide",
            slug=slug,
            resource_type=resource_type,
            excerpt="A practical business guide.",
            content={
                "intro": "Introduction",
                "sections": [],
            },
            status=status,
            published_at=(
                published_at
                if published_at is not None
                else timezone.now()
            ),
            is_active=is_active,
        )

    def test_public_list_returns_published_resource(self):
        self.create_resource()

        response = self.client.get("/public")

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(payload["count"], 1)
        self.assertEqual(
            payload["items"][0]["slug"],
            "business-guide",
        )

    def test_public_list_hides_drafts(self):
        self.create_resource(
            status=ResourceStatus.DRAFT,
        )

        response = self.client.get("/public")

        self.assertEqual(
            response.json()["count"],
            0,
        )

    def test_public_list_filters_resource_type(self):
        self.create_resource(
            resource_type=ResourceType.GUIDE,
        )

        self.create_resource(
            slug="sample-template",
            resource_type=ResourceType.TEMPLATE,
        )

        response = self.client.get(
            "/public?resource_type=template"
        )

        payload = response.json()

        self.assertEqual(payload["count"], 1)
        self.assertEqual(
            payload["items"][0]["resource_type"],
            "template",
        )

    def test_public_detail_returns_resource(self):
        self.create_resource()

        response = self.client.get(
            "/public/business-guide"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["slug"],
            "business-guide",
        )

    def test_public_detail_returns_404_for_missing_resource(self):
        response = self.client.get(
            "/public/not-found"
        )

        self.assertEqual(response.status_code, 404)
