from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api

from .models import (
    ArticleStatus,
    InsightArticle,
)
from .services import InsightService


User = get_user_model()


class InsightsApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="insights-admin",
            email="insights-admin@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(
            self.admin
        ).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

        category_response = self.client.post(
            "/insights/categories",
            json={
                "name": "Web Development",
                "slug": "web-development",
                "description": "Website articles.",
                "is_active": True,
                "sort_order": 1,
            },
            headers=self.headers,
        )

        self.category = category_response.json()

        tag_response = self.client.post(
            "/insights/tags",
            json={
                "name": "SEO",
                "slug": "seo",
                "description": "SEO articles.",
                "is_active": True,
            },
            headers=self.headers,
        )

        self.tag = tag_response.json()

    def payload(self):
        return {
            "title": (
                "Why Business Websites Fail to Generate Leads"
            ),
            "slug": (
                "why-business-websites-fail-to-generate-leads"
            ),
            "excerpt": (
                "Common reasons websites fail to convert."
            ),
            "content": {
                "introduction": (
                    "A website must support business goals."
                ),
                "sections": [
                    {
                        "heading": "Poor positioning",
                        "body": (
                            "Visitors need a clear reason "
                            "to choose the business."
                        ),
                    },
                ],
            },
            "category_id": self.category["id"],
            "tag_ids": [self.tag["id"]],
            "author_id": self.admin.pk,
            "status": "draft",
            "is_featured": True,
            "is_active": True,
            "allow_comments": False,
            "related_article_ids": [],
            "internal_links": [],
            "seo": {
                "meta_title": (
                    "Why Business Websites Fail"
                ),
                "meta_description": (
                    "Learn why websites fail to generate leads."
                ),
                "robots_index": True,
                "robots_follow": True,
                "article_schema": {},
                "faq_schema": [],
            },
        }

    def create_article(self):
        return self.client.post(
            "/insights",
            json=self.payload(),
            headers=self.headers,
        )

    def test_create_article(self):
        response = self.create_article()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["status"],
            ArticleStatus.DRAFT,
        )
        self.assertEqual(
            response.json()["current_revision_number"],
            1,
        )
        self.assertEqual(
            len(response.json()["tags"]),
            1,
        )
        self.assertGreater(
            response.json()["word_count"],
            0,
        )

    def test_duplicate_slug_is_rejected(self):
        self.create_article()
        response = self.create_article()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "duplicate_insight_slug",
        )

    def test_update_creates_revision(self):
        created = self.create_article().json()

        payload = self.payload()
        payload["title"] = (
            "Why Most Business Websites Fail"
        )
        payload["change_summary"] = (
            "Improved article headline."
        )

        response = self.client.put(
            f"/insights/{created['id']}",
            json=payload,
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["current_revision_number"],
            2,
        )

    def test_publish_article(self):
        created = self.create_article().json()

        response = self.client.post(
            f"/insights/{created['id']}/publish",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            ArticleStatus.PUBLISHED,
        )
        self.assertTrue(
            response.json()["is_publicly_available"]
        )

    def test_schedule_article(self):
        created = self.create_article().json()

        response = self.client.post(
            f"/insights/{created['id']}/schedule",
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
            ArticleStatus.SCHEDULED,
        )

    def test_past_schedule_is_rejected(self):
        created = self.create_article().json()

        response = self.client.post(
            f"/insights/{created['id']}/schedule",
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

    def test_due_article_is_published(self):
        article = InsightArticle.objects.create(
            title="Scheduled Article",
            slug="scheduled-article",
            status=ArticleStatus.SCHEDULED,
            scheduled_for=(
                timezone.now() - timedelta(minutes=1)
            ),
            author=self.admin,
            created_by=self.admin,
            updated_by=self.admin,
        )

        count = (
            InsightService
            .process_scheduled_articles()
        )

        article.refresh_from_db()

        self.assertEqual(count, 1)
        self.assertEqual(
            article.status,
            ArticleStatus.PUBLISHED,
        )

    def test_soft_delete_article(self):
        created = self.create_article().json()

        response = self.client.delete(
            f"/insights/{created['id']}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            InsightArticle.objects.filter(
                pk=created["id"],
            ).exists()
        )
        self.assertTrue(
            InsightArticle.all_objects.filter(
                pk=created["id"],
            ).exists()
        )

    def test_unauthenticated_request_is_rejected(self):
        response = self.client.get("/insights")

        self.assertEqual(response.status_code, 401)


class InsightMetricTests(TestCase):
    def test_content_metrics_are_calculated(self):
        metrics = InsightService.calculate_content_metrics(
            {
                "heading": "Example heading",
                "body": "One two three four five.",
            }
        )

        self.assertGreater(
            metrics["word_count"],
            0,
        )
        self.assertGreaterEqual(
            metrics["reading_time_minutes"],
            1,
        )
