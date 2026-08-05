from django.contrib.auth import get_user_model
from django.test import TestCase
from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.activity.models import ActivityLog
from apps.api.api import api
from apps.audit.models import AuditLog
from apps.crm.models import (
    Lead,
    LeadStatus,
    LeadTimelineEvent,
)

from .models import (
    Client,
    ClientContact,
    ClientWebsite,
)


User = get_user_model()


class ClientsApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="clients-admin",
            email="clients-admin@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(
            self.admin
        ).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

    def create_client_record(self):
        return Client.objects.create(
            company_name="Existing Client",
            client_code="LKP-CL-99999",
            created_by=self.admin,
            updated_by=self.admin,
        )

    def test_superuser_can_create_client(self):
        response = self.client.post(
            "/clients",
            json={
                "company_name": "Example Corporation",
                "legal_name": "Example Corporation Ltd",
                "client_type": "company",
                "status": "active",
                "industry": "Technology",
                "country": "United Kingdom",
                "timezone": "Europe/London",
                "email": "info@example.com",
                "phone": "+44123456789",
                "whatsapp": "+44123456789",
                "website": "https://example.com",
                "default_currency": "GBP",
                "payment_terms_days": 30,
                "tags": ["international", "priority"],
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)

        client = Client.objects.get(
            company_name="Example Corporation"
        )

        self.assertTrue(
            client.client_code.startswith("LKP-CL-")
        )

        self.assertTrue(
            ActivityLog.objects.filter(
                action="client_created",
                entity_id=str(client.pk),
            ).exists()
        )

        self.assertTrue(
            AuditLog.objects.filter(
                target_id=str(client.pk),
            ).exists()
        )

    def test_superuser_can_list_and_search_clients(self):
        self.create_client_record()

        response = self.client.get(
            "/clients",
            data={
                "search": "Existing Client",
                "page": 1,
                "page_size": 10,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["pagination"]["total_items"],
            1,
        )

    def test_superuser_can_update_client(self):
        client = self.create_client_record()

        response = self.client.put(
            f"/clients/{client.pk}",
            json={
                "company_name": "Updated Client",
                "legal_name": "",
                "client_type": "company",
                "status": "active",
                "industry": "Software",
                "country": "Sri Lanka",
                "timezone": "Asia/Colombo",
                "phone": "+94770000000",
                "whatsapp": "+94770000000",
                "default_currency": "LKR",
                "payment_terms_days": 14,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        client.refresh_from_db()

        self.assertEqual(
            client.company_name,
            "Updated Client",
        )
        self.assertEqual(client.industry, "Software")

    def test_superuser_can_add_primary_contact(self):
        client = self.create_client_record()

        response = self.client.post(
            f"/clients/{client.pk}/contacts",
            json={
                "first_name": "John",
                "last_name": "Smith",
                "email": "john@example.com",
                "phone": "+44123456789",
                "is_primary": True,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            ClientContact.objects.filter(
                client=client,
                is_primary=True,
            ).exists()
        )

    def test_only_one_primary_contact_is_retained(self):
        client = self.create_client_record()

        ClientContact.objects.create(
            client=client,
            first_name="First",
            is_primary=True,
        )

        self.client.post(
            f"/clients/{client.pk}/contacts",
            json={
                "first_name": "Second",
                "is_primary": True,
            },
            headers=self.headers,
        )

        self.assertEqual(
            ClientContact.objects.filter(
                client=client,
                is_primary=True,
            ).count(),
            1,
        )

    def test_superuser_can_add_primary_website(self):
        client = self.create_client_record()

        response = self.client.post(
            f"/clients/{client.pk}/websites",
            json={
                "name": "Corporate Website",
                "url": "https://example.com",
                "platform": "Django",
                "is_primary": True,
                "is_active": True,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            ClientWebsite.objects.filter(
                client=client,
                is_primary=True,
            ).exists()
        )

    def test_lead_can_be_converted_to_client(self):
        lead = Lead.objects.create(
            name="Lead Contact",
            company="Lead Company",
            email="lead@example.com",
            phone="+94771111111",
            whatsapp="+94771111111",
            country="Sri Lanka",
            currency="LKR",
            created_by=self.admin,
            updated_by=self.admin,
        )

        response = self.client.post(
            f"/clients/convert-lead/{lead.pk}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)

        lead.refresh_from_db()

        self.assertEqual(lead.status, LeadStatus.WON)

        client = Client.objects.get(source_lead=lead)

        self.assertEqual(
            client.company_name,
            "Lead Company",
        )

        self.assertTrue(
            client.contacts.filter(
                is_primary=True,
                email=lead.email,
            ).exists()
        )

        self.assertTrue(
            lead.timeline_entries.filter(
                event_type=LeadTimelineEvent.CONVERTED,
            ).exists()
        )

    def test_duplicate_lead_conversion_returns_existing_client(self):
        lead = Lead.objects.create(
            name="Duplicate Lead",
            company="Duplicate Company",
            created_by=self.admin,
            updated_by=self.admin,
        )

        first_response = self.client.post(
            f"/clients/convert-lead/{lead.pk}",
            headers=self.headers,
        )

        second_response = self.client.post(
            f"/clients/convert-lead/{lead.pk}",
            headers=self.headers,
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 201)

        self.assertEqual(
            Client.objects.filter(
                source_lead=lead,
            ).count(),
            1,
        )

    def test_superuser_can_soft_delete_client(self):
        client = self.create_client_record()

        response = self.client.delete(
            f"/clients/{client.pk}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Client.objects.filter(pk=client.pk).exists()
        )
        self.assertTrue(
            Client.all_objects.filter(
                pk=client.pk
            ).exists()
        )

    def test_unauthenticated_request_is_rejected(self):
        response = self.client.get("/clients")

        self.assertEqual(response.status_code, 401)
