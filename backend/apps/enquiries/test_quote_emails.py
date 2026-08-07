from django.core import mail
from django.test import (
    TestCase,
    override_settings,
)

from .emails import QuoteEnquiryEmailService
from .models import QuoteEnquiry


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
class QuoteEnquiryEmailServiceTests(TestCase):
    def setUp(self):
        self.enquiry = QuoteEnquiry.objects.create(
            reference_code="WEBQ-EMAIL001",
            name="Test Customer",
            email="customer@example.com",
            phone="+94761234321",
            company_name="Example Company",
            country="Sri Lanka",
            project_title="Website Development",
            project_description=(
                "We need a corporate website."
            ),
            source="website",
            source_url=(
                "https://lkprofessionals.com/"
                "get-a-quote/"
            ),
            metadata={
                "preferred_contact_method": (
                    "email"
                ),
                "best_time_to_contact": (
                    "morning"
                ),
                "source_surface": "page",
            },
        )

    def test_sends_customer_and_internal_email(self):
        result = (
            QuoteEnquiryEmailService
            .send_quote_emails(
                self.enquiry
            )
        )

        self.assertTrue(
            result["customer"]
        )

        self.assertTrue(
            result["internal"]
        )

        self.assertEqual(
            len(mail.outbox),
            2,
        )

    def test_customer_email_recipient(self):
        QuoteEnquiryEmailService.send_quote_emails(
            self.enquiry
        )

        customer_email = mail.outbox[0]

        self.assertEqual(
            customer_email.to,
            [
                "customer@example.com",
            ],
        )

        self.assertIn(
            self.enquiry.reference_code,
            customer_email.subject,
        )

        self.assertEqual(
            customer_email.reply_to,
            [
                "info@lkprofessionals.com",
            ],
        )

    def test_internal_email_recipient(self):
        QuoteEnquiryEmailService.send_quote_emails(
            self.enquiry
        )

        internal_email = mail.outbox[1]

        self.assertEqual(
            internal_email.to,
            [
                "info@lkprofessionals.com",
            ],
        )

        self.assertEqual(
            internal_email.reply_to,
            [
                "customer@example.com",
            ],
        )

        self.assertIn(
            "Website Development",
            internal_email.subject,
        )

    def test_emails_include_html_alternative(self):
        QuoteEnquiryEmailService.send_quote_emails(
            self.enquiry
        )

        for message in mail.outbox:
            self.assertEqual(
                len(message.alternatives),
                1,
            )

            html_content, mimetype = (
                message.alternatives[0]
            )

            self.assertEqual(
                mimetype,
                "text/html",
            )

            self.assertTrue(
                html_content.strip(),
            )
