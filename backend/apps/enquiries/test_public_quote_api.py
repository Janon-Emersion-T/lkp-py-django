from django.test import (
    TestCase,
    override_settings,
)

from .models import (
    EnquirySource,
    QuoteEnquiry,
)


@override_settings(
    EMAIL_BACKEND=(
        "django.core.mail.backends.locmem.EmailBackend"
    ),
    DEFAULT_FROM_EMAIL=(
        "LKProfessionals <dev@example.com>"
    ),
    LKP_CONTACT_EMAIL=(
        "info@lkprofessionals.com"
    ),
    LKP_QUOTE_NOTIFICATION_EMAIL=(
        "info@lkprofessionals.com"
    ),
)
class PublicQuoteRequestApiTests(TestCase):
    url = "/api/v1/enquiries/quotes/public"

    def valid_payload(self):
        return {
            "full_name": "Website Customer",
            "company_name": "Example Company",
            "service_required": "Website Development",
            "email": "customer@example.com",
            "whatsapp_number": "",
            "preferred_contact_method": "email",
            "country": "Sri Lanka",
            "project_description": (
                "We need a business website with CMS "
                "and enquiry functionality."
            ),
            "best_time_to_contact": "morning",
            "source_surface": "page",
            "source_url": (
                "https://lkprofessionals.com/get-a-quote/"
            ),
        }

    def test_public_quote_requires_no_authentication(self):
        response = self.client.post(
            self.url,
            data=self.valid_payload(),
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

    def test_public_quote_enters_existing_quote_enquiries(self):
        response = self.client.post(
            self.url,
            data=self.valid_payload(),
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        enquiry = QuoteEnquiry.objects.get(
            email="customer@example.com",
        )

        self.assertTrue(
            enquiry.reference_code.startswith(
                "WEBQ-"
            )
        )

        self.assertEqual(
            enquiry.source,
            EnquirySource.WEBSITE,
        )

        self.assertEqual(
            enquiry.project_title,
            "Website Development",
        )

        self.assertEqual(
            enquiry.metadata[
                "preferred_contact_method"
            ],
            "email",
        )

        self.assertEqual(
            enquiry.metadata[
                "source_surface"
            ],
            "page",
        )

    def test_whatsapp_remains_optional_for_email(self):
        payload = self.valid_payload()

        payload["whatsapp_number"] = ""
        payload[
            "preferred_contact_method"
        ] = "email"

        response = self.client.post(
            self.url,
            data=payload,
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

    def test_whatsapp_is_required_when_preferred(self):
        payload = self.valid_payload()

        payload["whatsapp_number"] = ""
        payload[
            "preferred_contact_method"
        ] = "whatsapp"

        response = self.client.post(
            self.url,
            data=payload,
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            QuoteEnquiry.objects.filter(
                email="customer@example.com",
            ).exists()
        )

    def test_whatsapp_submission_with_number_succeeds(self):
        payload = self.valid_payload()

        payload["whatsapp_number"] = (
            "+94761234321"
        )

        payload[
            "preferred_contact_method"
        ] = "whatsapp"

        response = self.client.post(
            self.url,
            data=payload,
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        enquiry = QuoteEnquiry.objects.get(
            email="customer@example.com",
        )

        self.assertEqual(
            enquiry.phone,
            "+94761234321",
        )

    def test_invalid_email_is_rejected(self):
        payload = self.valid_payload()
        payload["email"] = "invalid-email"

        response = self.client.post(
            self.url,
            data=payload,
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_invalid_service_is_rejected(self):
        payload = self.valid_payload()

        payload["service_required"] = (
            "Imaginary Service"
        )

        response = self.client.post(
            self.url,
            data=payload,
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_modal_submission_source_is_recorded(self):
        payload = self.valid_payload()

        payload["source_surface"] = "modal"

        response = self.client.post(
            self.url,
            data=payload,
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        enquiry = QuoteEnquiry.objects.get(
            email="customer@example.com",
        )

        self.assertEqual(
            enquiry.metadata["source_surface"],
            "modal",
        )
