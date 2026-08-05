from django.contrib.auth import get_user_model
from django.test import TestCase
from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.activity.models import ActivityLog
from apps.api.api import api
from apps.audit.models import AuditLog

from .models import (
    Lead,
    LeadNote,
    LeadStatus,
    LeadTimelineEvent,
)


User = get_user_model()


class CrmApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="crm-admin",
            email="crm-admin@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(
            self.admin
        ).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

    def create_lead(self):
        return Lead.objects.create(
            name="Test Contact",
            company="Test Company",
            email="lead@example.com",
            created_by=self.admin,
            updated_by=self.admin,
        )

    def test_superuser_can_create_lead(self):
        response = self.client.post(
            "/crm",
            json={
                "name": "John Smith",
                "company": "Example Ltd",
                "email": "john@example.com",
                "phone": "+44123456789",
                "whatsapp": "+44123456789",
                "country": "United Kingdom",
                "website": "https://example.com",
                "source": "google",
                "status": "new",
                "priority": "high",
                "lead_score": 75,
                "estimated_value": "2500.00",
                "currency": "GBP",
                "tags": ["website", "seo"],
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)

        lead = Lead.objects.get(
            email="john@example.com"
        )

        self.assertEqual(
            lead.company,
            "Example Ltd",
        )

        self.assertTrue(
            lead.timeline_entries.filter(
                event_type=LeadTimelineEvent.CREATED,
            ).exists()
        )

        self.assertTrue(
            ActivityLog.objects.filter(
                entity_id=str(lead.pk),
                action="lead_created",
            ).exists()
        )

        self.assertTrue(
            AuditLog.objects.filter(
                target_id=str(lead.pk),
            ).exists()
        )

    def test_superuser_can_list_and_search_leads(self):
        self.create_lead()

        response = self.client.get(
            "/crm",
            data={
                "search": "Test Company",
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
        self.assertEqual(
            response.json()["items"][0]["company"],
            "Test Company",
        )

    def test_superuser_can_update_lead_status(self):
        lead = self.create_lead()

        response = self.client.put(
            f"/crm/{lead.pk}",
            json={
                "name": lead.name,
                "company": lead.company,
                "email": lead.email,
                "status": "contacted",
                "source": "manual",
                "priority": "normal",
                "lead_score": 20,
                "currency": "LKR",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        lead.refresh_from_db()

        self.assertEqual(
            lead.status,
            LeadStatus.CONTACTED,
        )

        self.assertTrue(
            lead.timeline_entries.filter(
                event_type=(
                    LeadTimelineEvent.STATUS_CHANGED
                ),
            ).exists()
        )

    def test_superuser_can_add_note(self):
        lead = self.create_lead()

        response = self.client.post(
            f"/crm/{lead.pk}/notes",
            json={
                "content": "Call the client tomorrow.",
                "is_pinned": True,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            LeadNote.objects.filter(
                lead=lead,
                is_pinned=True,
            ).exists()
        )

    def test_superuser_can_view_timeline(self):
        lead = self.create_lead()

        response = self.client.get(
            f"/crm/{lead.pk}/timeline",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

    def test_superuser_can_soft_delete_lead(self):
        lead = self.create_lead()

        response = self.client.delete(
            f"/crm/{lead.pk}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Lead.objects.filter(pk=lead.pk).exists()
        )
        self.assertTrue(
            Lead.all_objects.filter(pk=lead.pk).exists()
        )

    def test_unauthenticated_request_is_rejected(self):
        response = self.client.get("/crm")

        self.assertEqual(response.status_code, 401)
