from typing import Any

from django.db import transaction

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event
from apps.crm.models import (
    Lead,
    LeadStatus,
    LeadTimelineEvent,
)
from apps.crm.services import LeadService

from .models import (
    Client,
    ClientContact,
    ClientWebsite,
)


class ClientService:
    @staticmethod
    def generate_client_code() -> str:
        latest = (
            Client.all_objects.order_by("-created_at")
            .values_list("client_code", flat=True)
            .first()
        )

        if latest and latest.startswith("LKP-CL-"):
            try:
                sequence = int(latest.rsplit("-", 1)[1]) + 1
            except ValueError:
                sequence = Client.all_objects.count() + 1
        else:
            sequence = Client.all_objects.count() + 1

        return f"LKP-CL-{sequence:05d}"

    @staticmethod
    @transaction.atomic
    def create_client(
        *,
        request,
        values: dict[str, Any],
    ) -> Client:
        values.setdefault(
            "client_code",
            ClientService.generate_client_code(),
        )

        client = Client.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="client_created",
            module="clients",
            description="Client created.",
            entity_type="clients.Client",
            entity_id=str(client.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="clients",
            message="Client created.",
            target_type="clients.Client",
            target_id=str(client.pk),
            after={
                "client_code": client.client_code,
                "company_name": client.company_name,
                "status": client.status,
                "country": client.country,
                "source_lead_id": (
                    str(client.source_lead_id)
                    if client.source_lead_id
                    else None
                ),
            },
        )

        return client

    @staticmethod
    @transaction.atomic
    def update_client(
        *,
        request,
        client: Client,
        values: dict[str, Any],
    ) -> Client:
        before = {
            "company_name": client.company_name,
            "legal_name": client.legal_name,
            "status": client.status,
            "industry": client.industry,
            "country": client.country,
            "email": client.email,
            "phone": client.phone,
            "whatsapp": client.whatsapp,
            "default_currency": client.default_currency,
        }

        for field, value in values.items():
            setattr(client, field, value)

        client.updated_by = request.auth
        client.save()

        log_activity(
            request=request,
            actor=request.auth,
            action="client_updated",
            module="clients",
            description="Client updated.",
            entity_type="clients.Client",
            entity_id=str(client.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="clients",
            message="Client updated.",
            target_type="clients.Client",
            target_id=str(client.pk),
            before=before,
            after={
                "company_name": client.company_name,
                "legal_name": client.legal_name,
                "status": client.status,
                "industry": client.industry,
                "country": client.country,
                "email": client.email,
                "phone": client.phone,
                "whatsapp": client.whatsapp,
                "default_currency": client.default_currency,
            },
        )

        return client

    @staticmethod
    @transaction.atomic
    def add_contact(
        *,
        request,
        client: Client,
        values: dict[str, Any],
    ) -> ClientContact:
        if values.get("is_primary"):
            ClientContact.objects.filter(
                client=client,
                is_primary=True,
            ).update(is_primary=False)

        contact = ClientContact.objects.create(
            client=client,
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="client_contact_added",
            module="clients",
            description="Client contact added.",
            entity_type="clients.Client",
            entity_id=str(client.pk),
            metadata={
                "contact_id": str(contact.pk),
            },
        )

        return contact

    @staticmethod
    @transaction.atomic
    def add_website(
        *,
        request,
        client: Client,
        values: dict[str, Any],
    ) -> ClientWebsite:
        if values.get("is_primary"):
            ClientWebsite.objects.filter(
                client=client,
                is_primary=True,
            ).update(is_primary=False)

        website = ClientWebsite.objects.create(
            client=client,
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        return website

    @staticmethod
    @transaction.atomic
    def convert_lead(
        *,
        request,
        lead: Lead,
    ) -> Client:
        if hasattr(lead, "converted_client"):
            return lead.converted_client

        company_name = (
            lead.company.strip()
            or lead.name.strip()
        )

        client = ClientService.create_client(
            request=request,
            values={
                "company_name": company_name,
                "email": lead.email,
                "phone": lead.phone,
                "whatsapp": lead.whatsapp,
                "country": lead.country,
                "website": lead.website,
                "notes": lead.notes,
                "tags": lead.tags,
                "source_lead": lead,
                "default_currency": lead.currency,
            },
        )

        ClientService.add_contact(
            request=request,
            client=client,
            values={
                "first_name": lead.name,
                "email": lead.email,
                "phone": lead.phone,
                "whatsapp": lead.whatsapp,
                "is_primary": True,
            },
        )

        lead.status = LeadStatus.WON
        lead.updated_by = request.auth
        lead.save(
            update_fields=[
                "status",
                "updated_by",
                "updated_at",
            ],
        )

        LeadService.create_timeline(
            lead=lead,
            event_type=LeadTimelineEvent.CONVERTED,
            description="Lead converted to client.",
            actor=request.auth,
            metadata={
                "client_id": str(client.pk),
                "client_code": client.client_code,
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="lead_converted",
            module="clients",
            description="Lead converted to client.",
            entity_type="clients.Client",
            entity_id=str(client.pk),
            metadata={
                "lead_id": str(lead.pk),
            },
        )

        return client

    @staticmethod
    @transaction.atomic
    def soft_delete_client(
        *,
        request,
        client: Client,
    ) -> None:
        client_id = str(client.pk)
        client.delete()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="clients",
            message="Client soft deleted.",
            target_type="clients.Client",
            target_id=client_id,
            after={
                "is_deleted": True,
            },
        )
