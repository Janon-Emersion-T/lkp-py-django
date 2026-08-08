from django.test import TestCase
from django.utils import timezone

from apps.case_studies.models import (
    CaseStudy,
    CaseStudyService,
    CaseStudyStatus,
)
from apps.services_catalog.models import Service


class PublicCaseStudiesApiTests(TestCase):
    url = "/api/v1/case-studies/public"

    def create_service(
        self,
        *,
        slug="mobile-app-development",
        title="Mobile App Development",
    ):
        return Service.objects.create(
            title=title,
            slug=slug,
            status="published",
            is_active=True,
            published_at=timezone.now(),
        )

    def create_case_study(
        self,
        *,
        title="Mobile Banking Application",
        slug="mobile-banking-application",
        status=CaseStudyStatus.PUBLISHED,
        published=True,
        is_active=True,
        service=None,
    ):
        case_study = CaseStudy.objects.create(
            title=title,
            slug=slug,
            client_name="Example Client",
            short_description=(
                "A mobile application case study."
            ),
            status=status,
            published_at=(
                timezone.now()
                if published
                else None
            ),
            is_active=is_active,
        )

        if service:
            CaseStudyService.objects.create(
                case_study=case_study,
                service=service,
            )

        return case_study

    def test_public_list_is_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            response.json()["count"],
            0,
        )

    def test_published_case_study_is_visible(self):
        self.create_case_study()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

        payload = response.json()

        self.assertEqual(
            payload["count"],
            1,
        )
        self.assertEqual(
            payload["items"][0]["slug"],
            "mobile-banking-application",
        )

    def test_draft_case_study_is_hidden(self):
        self.create_case_study(
            status=CaseStudyStatus.DRAFT,
            published=False,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.json()["count"],
            0,
        )

    def test_inactive_case_study_is_hidden(self):
        self.create_case_study(
            is_active=False,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.json()["count"],
            0,
        )

    def test_service_slug_filter(self):
        mobile = self.create_service()

        web = self.create_service(
            slug="web-development",
            title="Web Development",
        )

        mobile_case = self.create_case_study(
            service=mobile,
        )

        web_case = self.create_case_study(
            title="Corporate Website",
            slug="corporate-website",
            service=web,
        )

        response = self.client.get(
            self.url,
            {
                "service_slug": (
                    "mobile-app-development"
                ),
            },
        )

        payload = response.json()

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            payload["count"],
            1,
        )
        self.assertEqual(
            payload["items"][0]["id"],
            str(mobile_case.id),
        )
        self.assertNotEqual(
            payload["items"][0]["id"],
            str(web_case.id),
        )

    def test_public_detail_by_slug(self):
        self.create_case_study()

        response = self.client.get(
            f"{self.url}/mobile-banking-application"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.json()["title"],
            "Mobile Banking Application",
        )

    def test_unpublished_detail_returns_404(self):
        self.create_case_study(
            status=CaseStudyStatus.DRAFT,
            published=False,
        )

        response = self.client.get(
            f"{self.url}/mobile-banking-application"
        )

        self.assertEqual(
            response.status_code,
            404,
        )
