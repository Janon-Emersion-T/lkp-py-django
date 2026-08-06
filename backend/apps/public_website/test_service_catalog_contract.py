from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from ninja.testing import TestClient

from apps.public_website.api import router
from apps.public_website.services import (
    PublicWebsiteService,
)
from apps.services_catalog.models import (
    Service,
    ServiceFaq,
    ServiceFeature,
    ServiceProcessStep,
    ServiceSeo,
    ServiceStatus,
    ServiceTechnology,
)


class PublicServiceCatalogContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = Service.objects.create(
            title="Web Development",
            slug="web-development",
            short_description="Business websites.",
            description={
                "overview": "Reliable web platforms.",
                "outcomes": ["Qualified enquiries"],
            },
            hero_title="Useful websites.",
            hero_description="Built for business.",
            status=ServiceStatus.PUBLISHED,
            published_at=timezone.now(),
            icon="browser",
            sort_order=1,
            is_featured=True,
            is_active=True,
            cta_title="Start a website project",
            cta_text="Discuss the requirement.",
            cta_label="Request a quote",
            cta_url="/request-quote",
        )

        ServiceFeature.objects.create(
            service=cls.service,
            title="Information architecture",
            description="Clear page structure.",
            icon="structure",
            sort_order=1,
        )

        ServiceProcessStep.objects.create(
            service=cls.service,
            step_number=1,
            title="Understand",
            description="Clarify the business.",
            sort_order=1,
        )

        ServiceTechnology.objects.create(
            service=cls.service,
            name="Astro",
            description="Performance-led publishing.",
            sort_order=1,
        )

        ServiceFaq.objects.create(
            service=cls.service,
            question="How long does it take?",
            answer="The timeline depends on scope.",
            sort_order=1,
        )

        ServiceSeo.objects.create(
            service=cls.service,
            meta_title="Web Development",
            meta_description="Professional websites.",
            canonical_url=(
                "https://lkprofessionals.com/"
                "services/web-development"
            ),
            structured_data={
                "@type": "Service",
            },
        )

    def test_catalog_contains_full_service_contract(self):
        payload = PublicWebsiteService.build_catalog(
            "production"
        )

        self.assertEqual(
            len(payload["services"]),
            1,
        )

        service = payload["services"][0]

        self.assertEqual(
            service["slug"],
            "web-development",
        )
        self.assertTrue(
            service["is_publicly_available"]
        )
        self.assertEqual(
            service["description"]["overview"],
            "Reliable web platforms.",
        )
        self.assertEqual(
            service["features"][0]["title"],
            "Information architecture",
        )
        self.assertEqual(
            service["process_steps"][0]["step_number"],
            1,
        )
        self.assertEqual(
            service["technologies"][0]["name"],
            "Astro",
        )
        self.assertEqual(
            service["faqs"][0]["question"],
            "How long does it take?",
        )
        self.assertEqual(
            service["seo"]["meta_title"],
            "Web Development",
        )

    def test_homepage_uses_full_featured_contract(self):
        payload = PublicWebsiteService.build_homepage(
            "production"
        )

        self.assertEqual(
            len(payload["featured_services"]),
            1,
        )

        service = payload["featured_services"][0]

        self.assertIn("features", service)
        self.assertIn("process_steps", service)
        self.assertIn("faqs", service)
        self.assertIn("seo", service)

    def test_unpublished_service_is_excluded(self):
        Service.objects.create(
            title="Draft Service",
            slug="draft-service",
            status=ServiceStatus.DRAFT,
            is_active=True,
            sort_order=2,
        )

        payload = PublicWebsiteService.build_catalog(
            "production"
        )

        self.assertEqual(
            [
                item["slug"]
                for item in payload["services"]
            ],
            ["web-development"],
        )

    def test_catalog_endpoint_is_anonymous(self):
        client = TestClient(router)

        response = client.get(
            "/catalog",
            {
                "environment": "production",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["services"][0]["slug"],
            "web-development",
        )


class PublicServiceSeedCommandTests(TestCase):
    def test_seed_command_is_idempotent(self):
        call_command("seed_public_services")

        first_count = Service.objects.count()
        first_feature_count = ServiceFeature.objects.count()

        call_command("seed_public_services")

        second_count = Service.objects.count()
        second_feature_count = ServiceFeature.objects.count()

        self.assertEqual(first_count, 8)
        self.assertEqual(second_count, 8)
        self.assertEqual(
            first_feature_count,
            second_feature_count,
        )

        web_service = Service.objects.get(
            slug="web-development"
        )

        self.assertEqual(
            web_service.status,
            ServiceStatus.PUBLISHED,
        )
        self.assertTrue(web_service.is_featured)
        self.assertEqual(web_service.features.count(), 4)
        self.assertEqual(
            web_service.process_steps.count(),
            4,
        )
        self.assertEqual(
            web_service.technologies.count(),
            4,
        )
        self.assertEqual(web_service.faqs.count(), 3)
        self.assertTrue(
            hasattr(web_service, "seo")
        )
