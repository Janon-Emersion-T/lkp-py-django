from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import User

from .models import (
    ContactEnquiry,
    EnquiryNote,
    EnquiryPriority,
    EnquirySource,
    EnquiryStatus,
    QuoteEnquiry,
)
from .repositories import (
    ContactEnquiryRepository,
    QuoteEnquiryRepository,
)
from .services import EnquiryService


class RequestStub:
    def __init__(self, user):
        self.auth = user
        self.user = user
        self.META = {}
        self.headers = {}


class EnquiryModelTests(TestCase):
    def test_contact_enquiry_string(self):
        enquiry = ContactEnquiry.objects.create(
            reference_code="CNT-001",
            name="Example Person",
            message="I need more information.",
        )

        self.assertEqual(
            str(enquiry),
            "CNT-001 — Example Person",
        )

    def test_quote_enquiry_string(self):
        enquiry = QuoteEnquiry.objects.create(
            reference_code="QTE-001",
            name="Example Client",
            project_title="Business Website",
            project_description="Build a new website.",
        )

        self.assertEqual(
            str(enquiry),
            "QTE-001 — Business Website",
        )

    def test_quote_rejects_invalid_budget_range(self):
        enquiry = QuoteEnquiry(
            reference_code="QTE-002",
            name="Example Client",
            project_description="Build software.",
            budget_min=Decimal("200000.00"),
            budget_max=Decimal("100000.00"),
        )

        with self.assertRaises(ValidationError):
            enquiry.full_clean()

    def test_quote_rejects_invalid_date_range(self):
        start = timezone.now().date()
        completion = start - timedelta(days=1)

        enquiry = QuoteEnquiry(
            reference_code="QTE-003",
            name="Example Client",
            project_description="Build software.",
            desired_start_date=start,
            desired_completion_date=completion,
        )

        with self.assertRaises(ValidationError):
            enquiry.full_clean()

    def test_note_requires_exactly_one_enquiry(self):
        note = EnquiryNote(
            note="Invalid unlinked note.",
        )

        with self.assertRaises(ValidationError):
            note.full_clean()


class EnquiryRepositoryTests(TestCase):
    def setUp(self):
        self.contact = ContactEnquiry.objects.create(
            reference_code="CNT-100",
            name="Contact Person",
            email="contact@example.com",
            company_name="Contact Company",
            message="Need consultation.",
            source=EnquirySource.GOOGLE,
            priority=EnquiryPriority.HIGH,
        )

        self.quote = QuoteEnquiry.objects.create(
            reference_code="QTE-100",
            name="Quote Person",
            email="quote@example.com",
            company_name="Quote Company",
            country="United Kingdom",
            project_title="ERP System",
            project_description="Need an ERP system.",
            source=EnquirySource.LINKEDIN,
            priority=EnquiryPriority.URGENT,
        )

    def test_search_contact_enquiry(self):
        queryset = ContactEnquiryRepository.search(
            search="Contact Company",
            source=EnquirySource.GOOGLE,
            priority=EnquiryPriority.HIGH,
        )

        self.assertEqual(queryset.count(), 1)

    def test_search_quote_enquiry(self):
        queryset = QuoteEnquiryRepository.search(
            search="ERP",
            country="United Kingdom",
            source=EnquirySource.LINKEDIN,
        )

        self.assertEqual(queryset.count(), 1)


class EnquiryServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="enquiry_admin",
            email="enquiry-admin@example.com",
            password="StrongPassword123!",
        )

        self.assignee = User.objects.create_user(
            username="enquiry_assignee",
            email="enquiry-assignee@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.user)

    def test_create_contact_enquiry(self):
        enquiry = EnquiryService.create_contact_enquiry(
            request=self.request,
            values={
                "reference_code": "CNT-200",
                "name": "Contact Applicant",
                "message": "I need web development.",
            },
        )

        self.assertEqual(
            enquiry.status,
            EnquiryStatus.NEW,
        )

    def test_create_quote_enquiry(self):
        enquiry = EnquiryService.create_quote_enquiry(
            request=self.request,
            values={
                "reference_code": "QTE-200",
                "name": "Quote Applicant",
                "project_description": (
                    "I need custom software."
                ),
            },
            services=[],
        )

        self.assertEqual(
            enquiry.status,
            EnquiryStatus.NEW,
        )

    def test_assign_enquiry(self):
        enquiry = ContactEnquiry.objects.create(
            reference_code="CNT-201",
            name="Assigned Person",
            message="Need a website.",
        )

        follow_up = (
            timezone.now() + timedelta(days=1)
        )

        enquiry = EnquiryService.assign_enquiry(
            request=self.request,
            enquiry=enquiry,
            assigned_to=self.assignee,
            priority=EnquiryPriority.URGENT,
            internal_summary="Qualified inbound lead.",
            next_follow_up_at=follow_up,
        )

        self.assertEqual(
            enquiry.assigned_to,
            self.assignee,
        )
        self.assertEqual(
            enquiry.status,
            EnquiryStatus.ASSIGNED,
        )
        self.assertEqual(
            enquiry.priority,
            EnquiryPriority.URGENT,
        )

    def test_contacted_status_sets_contact_time(self):
        enquiry = ContactEnquiry.objects.create(
            reference_code="CNT-202",
            name="Contacted Person",
            message="Need consultation.",
        )

        enquiry = EnquiryService.update_status(
            request=self.request,
            enquiry=enquiry,
            status=EnquiryStatus.CONTACTED,
        )

        self.assertIsNotNone(
            enquiry.first_contacted_at,
        )

    def test_lost_status_records_reason(self):
        enquiry = QuoteEnquiry.objects.create(
            reference_code="QTE-202",
            name="Lost Person",
            project_description="Need a system.",
        )

        enquiry = EnquiryService.update_status(
            request=self.request,
            enquiry=enquiry,
            status=EnquiryStatus.LOST,
            loss_reason="Budget was not approved.",
        )

        self.assertEqual(
            enquiry.loss_reason,
            "Budget was not approved.",
        )
        self.assertIsNotNone(enquiry.resolved_at)

    def test_add_contact_note(self):
        enquiry = ContactEnquiry.objects.create(
            reference_code="CNT-203",
            name="Note Person",
            message="Need support.",
        )

        note = EnquiryService.add_note(
            request=self.request,
            contact_enquiry=enquiry,
            note="Called the prospect.",
        )

        self.assertEqual(note.author, self.user)
        self.assertEqual(
            note.contact_enquiry,
            enquiry,
        )

    def test_add_quote_note(self):
        enquiry = QuoteEnquiry.objects.create(
            reference_code="QTE-203",
            name="Quote Note Person",
            project_description="Need an application.",
        )

        note = EnquiryService.add_note(
            request=self.request,
            quote_enquiry=enquiry,
            note="Requested detailed requirements.",
        )

        self.assertEqual(
            note.quote_enquiry,
            enquiry,
        )



from .repositories import EnquiryDashboardRepository


class EnquiryFinalizationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="enquiry_final_admin",
            email="enquiry-final@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.user)

        self.contact = ContactEnquiry.objects.create(
            reference_code="CNT-300",
            name="Final Contact",
            email="final-contact@example.com",
            message="Need a consultation.",
            priority=EnquiryPriority.URGENT,
            next_follow_up_at=(
                timezone.now() - timedelta(hours=1)
            ),
        )

        self.quote = QuoteEnquiry.objects.create(
            reference_code="QTE-300",
            name="Final Quote",
            email="final-quote@example.com",
            project_title="Custom ERP",
            project_description="Need an ERP platform.",
            priority=EnquiryPriority.HIGH,
        )

    def test_update_contact_enquiry(self):
        enquiry = (
            EnquiryService.update_contact_enquiry(
                request=self.request,
                enquiry=self.contact,
                values={
                    "subject": "Updated subject",
                    "company_name": (
                        "Updated Company"
                    ),
                },
            )
        )

        self.assertEqual(
            enquiry.subject,
            "Updated subject",
        )
        self.assertEqual(
            enquiry.company_name,
            "Updated Company",
        )

    def test_update_quote_enquiry(self):
        enquiry = (
            EnquiryService.update_quote_enquiry(
                request=self.request,
                enquiry=self.quote,
                values={
                    "project_title": (
                        "Updated ERP Platform"
                    ),
                    "budget_min": Decimal(
                        "100000.00"
                    ),
                    "budget_max": Decimal(
                        "200000.00"
                    ),
                },
                services=[],
            )
        )

        self.assertEqual(
            enquiry.project_title,
            "Updated ERP Platform",
        )

    def test_complete_follow_up(self):
        next_follow_up = (
            timezone.now() + timedelta(days=2)
        )

        enquiry = EnquiryService.complete_follow_up(
            request=self.request,
            enquiry=self.contact,
            next_follow_up_at=next_follow_up,
        )

        self.assertIsNotNone(
            enquiry.last_follow_up_at,
        )
        self.assertEqual(
            enquiry.next_follow_up_at,
            next_follow_up,
        )

    def test_dashboard_statistics(self):
        stats = EnquiryDashboardRepository.statistics()

        self.assertEqual(
            stats["total_contact_enquiries"],
            1,
        )
        self.assertEqual(
            stats["total_quote_enquiries"],
            1,
        )
        self.assertEqual(
            stats["new_contact_enquiries"],
            1,
        )
        self.assertEqual(
            stats["urgent_contact_enquiries"],
            1,
        )
        self.assertEqual(
            stats["overdue_contact_follow_ups"],
            1,
        )

    def test_won_and_lost_dashboard_counts(self):
        self.contact.status = EnquiryStatus.WON
        self.contact.save()

        self.quote.status = EnquiryStatus.LOST
        self.quote.loss_reason = "Budget unavailable."
        self.quote.save()

        stats = EnquiryDashboardRepository.statistics()

        self.assertEqual(
            stats["won_contact_enquiries"],
            1,
        )
        self.assertEqual(
            stats["lost_quote_enquiries"],
            1,
        )
