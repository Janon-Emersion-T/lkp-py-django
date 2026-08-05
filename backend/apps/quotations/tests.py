from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.clients.models import Client

from .calculations import calculate_item
from .models import (
    Quotation,
    QuotationItem,
    QuotationStatus,
)
from .services import QuotationService


User = get_user_model()


class QuotationServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="quotation-admin",
            email="quotation-admin@example.com",
            password="StrongPassword123!",
        )

        self.client = Client.objects.create(
            company_name="Quotation Client",
            client_code="LKP-CL-00001",
            created_by=self.user,
            updated_by=self.user,
        )

        self.request = type(
            "Request",
            (),
            {
                "auth": self.user,
                "META": {},
            },
        )()

    def test_item_calculation(self):
        item = QuotationItem(
            title="Website Development",
            quantity=Decimal("2.00"),
            unit_price=Decimal("1000.00"),
            discount_amount=Decimal("200.00"),
            tax_rate=Decimal("10.00"),
        )

        calculate_item(item)

        self.assertEqual(
            item.subtotal,
            Decimal("1800.00"),
        )
        self.assertEqual(
            item.tax_amount,
            Decimal("180.00"),
        )
        self.assertEqual(
            item.total_amount,
            Decimal("1980.00"),
        )

    def test_create_quotation_calculates_totals(self):
        quotation = QuotationService.create_quotation(
            request=self.request,
            values={
                "client": self.client,
                "title": "Website Quotation",
                "currency": "GBP",
                "discount_amount": Decimal("100.00"),
            },
            items=[
                {
                    "title": "Website",
                    "quantity": Decimal("1.00"),
                    "unit_price": Decimal("1000.00"),
                    "discount_amount": Decimal("0.00"),
                    "tax_rate": Decimal("10.00"),
                },
                {
                    "title": "SEO",
                    "quantity": Decimal("2.00"),
                    "unit_price": Decimal("200.00"),
                    "discount_amount": Decimal("0.00"),
                    "tax_rate": Decimal("0.00"),
                },
            ],
        )

        self.assertEqual(
            quotation.subtotal,
            Decimal("1400.00"),
        )
        self.assertEqual(
            quotation.discount_amount,
            Decimal("100.00"),
        )
        self.assertEqual(
            quotation.tax_amount,
            Decimal("100.00"),
        )
        self.assertEqual(
            quotation.total_amount,
            Decimal("1400.00"),
        )

    def test_quotation_number_is_generated(self):
        first = QuotationService.create_quotation(
            request=self.request,
            values={
                "client": self.client,
                "title": "First",
            },
            items=[],
        )

        second = QuotationService.create_quotation(
            request=self.request,
            values={
                "client": self.client,
                "title": "Second",
            },
            items=[],
        )

        self.assertNotEqual(
            first.quotation_number,
            second.quotation_number,
        )
        self.assertTrue(
            first.quotation_number.startswith(
                f"LKP-QT-{timezone.localdate().year}-"
            )
        )

    def test_duplicate_creates_new_draft(self):
        quotation = QuotationService.create_quotation(
            request=self.request,
            values={
                "client": self.client,
                "title": "Original",
            },
            items=[
                {
                    "title": "Development",
                    "quantity": Decimal("1.00"),
                    "unit_price": Decimal("500.00"),
                    "discount_amount": Decimal("0.00"),
                    "tax_rate": Decimal("0.00"),
                },
            ],
        )

        duplicate = QuotationService.duplicate(
            request=self.request,
            quotation=quotation,
        )

        self.assertNotEqual(
            quotation.pk,
            duplicate.pk,
        )
        self.assertEqual(
            duplicate.status,
            QuotationStatus.DRAFT,
        )
        self.assertEqual(
            duplicate.duplicated_from,
            quotation,
        )
        self.assertEqual(
            duplicate.items.count(),
            1,
        )

    def test_accept_quotation(self):
        quotation = QuotationService.create_quotation(
            request=self.request,
            values={
                "client": self.client,
                "title": "Acceptable",
            },
            items=[],
        )

        QuotationService.accept(
            request=self.request,
            quotation=quotation,
            accepted_by_name="John Smith",
            accepted_by_email="john@example.com",
        )

        quotation.refresh_from_db()

        self.assertEqual(
            quotation.status,
            QuotationStatus.ACCEPTED,
        )
        self.assertIsNotNone(
            quotation.accepted_at,
        )

    def test_expired_quotation_cannot_be_accepted(self):
        quotation = Quotation.objects.create(
            quotation_number="LKP-QT-2026-99999",
            client=self.client,
            title="Expired",
            expiry_date=(
                timezone.localdate()
                - timedelta(days=1)
            ),
            created_by=self.user,
            updated_by=self.user,
        )

        with self.assertRaises(ValueError):
            QuotationService.accept(
                request=self.request,
                quotation=quotation,
                accepted_by_name="John Smith",
                accepted_by_email="john@example.com",
            )

        quotation.refresh_from_db()

        self.assertEqual(
            quotation.status,
            QuotationStatus.EXPIRED,
        )

    def test_expired_quotations_are_marked(self):
        Quotation.objects.create(
            quotation_number="LKP-QT-2026-99998",
            client=self.client,
            title="Old quotation",
            status=QuotationStatus.SENT,
            expiry_date=(
                timezone.localdate()
                - timedelta(days=2)
            ),
            created_by=self.user,
            updated_by=self.user,
        )

        count = (
            QuotationService.mark_expired_quotations()
        )

        self.assertEqual(count, 1)

        self.assertTrue(
            Quotation.objects.filter(
                status=QuotationStatus.EXPIRED,
            ).exists()
        )


from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api


class QuotationApiTests(TestCase):
    def setUp(self):
        self.api_client = TestClient(api)

        self.user = User.objects.create_superuser(
            username="quotation-api-admin",
            email="quotation-api@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(
            self.user
        ).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

        self.client_record = Client.objects.create(
            company_name="API Client",
            client_code="LKP-CL-00999",
            email="client@example.com",
            country="Sri Lanka",
            created_by=self.user,
            updated_by=self.user,
        )

    def create_via_api(self):
        return self.api_client.post(
            "/quotations",
            json={
                "client_id": str(
                    self.client_record.pk
                ),
                "title": "Website Development",
                "subject": "Business website",
                "currency": "LKR",
                "discount_amount": "1000.00",
                "items": [
                    {
                        "title": "Website",
                        "quantity": "1.00",
                        "unit_price": "100000.00",
                        "discount_amount": "0.00",
                        "tax_rate": "0.00",
                    },
                ],
                "recipients": [
                    {
                        "name": "Client Contact",
                        "email": "client@example.com",
                        "is_primary": True,
                    },
                ],
            },
            headers=self.headers,
        )

    def test_superuser_can_create_quotation(self):
        response = self.create_via_api()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["total_amount"],
            "99000.00",
        )

    def test_superuser_can_list_quotations(self):
        self.create_via_api()

        response = self.api_client.get(
            "/quotations",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["pagination"]["total_items"],
            1,
        )

    def test_superuser_can_update_quotation(self):
        created = self.create_via_api().json()

        response = self.api_client.put(
            f"/quotations/{created['id']}",
            json={
                "title": "Updated Quotation",
                "subject": "Updated subject",
                "description": "",
                "issue_date": created["issue_date"],
                "expiry_date": created["expiry_date"],
                "currency": "LKR",
                "discount_amount": "0.00",
                "tax_amount": "0.00",
                "terms": "",
                "notes": "",
                "items": [
                    {
                        "title": "Updated Website",
                        "quantity": "1.00",
                        "unit_price": "120000.00",
                        "discount_amount": "0.00",
                        "tax_rate": "0.00",
                    },
                ],
                "recipients": [],
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["title"],
            "Updated Quotation",
        )
        self.assertEqual(
            response.json()["total_amount"],
            "120000.00",
        )

    def test_superuser_can_duplicate_quotation(self):
        created = self.create_via_api().json()

        response = self.api_client.post(
            f"/quotations/{created['id']}/duplicate",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(
            response.json()["id"],
            created["id"],
        )
        self.assertEqual(
            response.json()["status"],
            QuotationStatus.DRAFT,
        )

    def test_superuser_can_send_and_accept_quotation(self):
        created = self.create_via_api().json()

        sent = self.api_client.post(
            f"/quotations/{created['id']}/send",
            headers=self.headers,
        )

        self.assertEqual(sent.status_code, 200)
        self.assertEqual(
            sent.json()["status"],
            QuotationStatus.SENT,
        )

        accepted = self.api_client.post(
            f"/quotations/{created['id']}/accept",
            json={
                "accepted_by_name": "Client Contact",
                "accepted_by_email": "client@example.com",
            },
            headers=self.headers,
        )

        self.assertEqual(accepted.status_code, 200)
        self.assertEqual(
            accepted.json()["status"],
            QuotationStatus.ACCEPTED,
        )

    def test_superuser_can_reject_quotation(self):
        created = self.create_via_api().json()

        response = self.api_client.post(
            f"/quotations/{created['id']}/reject",
            json={
                "reason": "Budget rejected",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            QuotationStatus.REJECTED,
        )

    def test_pdf_payload_is_available(self):
        created = self.create_via_api().json()

        response = self.api_client.get(
            f"/quotations/{created['id']}/pdf-data",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["client"]["company_name"],
            "API Client",
        )
        self.assertEqual(
            response.json()["quotation"][
                "quotation_number"
            ],
            created["quotation_number"],
        )

    def test_superuser_can_soft_delete_quotation(self):
        created = self.create_via_api().json()

        response = self.api_client.delete(
            f"/quotations/{created['id']}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Quotation.objects.filter(
                pk=created["id"]
            ).exists()
        )
        self.assertTrue(
            Quotation.all_objects.filter(
                pk=created["id"]
            ).exists()
        )

    def test_unauthenticated_request_is_rejected(self):
        response = self.api_client.get("/quotations")

        self.assertEqual(response.status_code, 401)
