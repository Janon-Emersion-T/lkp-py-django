from django.test import TestCase

from .models import (
    ContactEnquiry,
    EnquirySource,
)


class PublicContactEnquiryApiTests(TestCase):
    url = "/api/v1/enquiries/contacts/public"

    def valid_payload(self):
        return {
            "full_name": "Website Visitor",
            "company_name": "Example Company",
            "email": "visitor@example.com",
            "phone": "+94761234321",
            "subject": "Website enquiry",
            "message": (
                "We would like to discuss a new website."
            ),
            "source_url": (
                "https://lkprofessionals.com/contact/"
            ),
        }

    def test_public_contact_submission(self):
        response = self.client.post(
            self.url,
            data=self.valid_payload(),
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        enquiry = ContactEnquiry.objects.get(
            email="visitor@example.com",
        )

        self.assertEqual(
            enquiry.source,
            EnquirySource.WEBSITE,
        )

        self.assertEqual(
            enquiry.metadata["website_form"],
            "contact",
        )

    def test_invalid_email_rejected(self):
        payload = self.valid_payload()
        payload["email"] = "invalid"

        response = self.client.post(
            self.url,
            data=payload,
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )
