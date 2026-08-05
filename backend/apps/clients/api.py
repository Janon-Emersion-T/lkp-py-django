from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema, MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.api.pagination_schemas import PaginatedResponseSchema
from apps.api.responses import paginated_response
from apps.common.pagination import paginate_queryset
from apps.crm.repositories import LeadRepository
from apps.rbac.services import require_permissions

from .repositories import ClientRepository
from .schemas import (
    ClientContactCreateSchema,
    ClientContactSchema,
    ClientCreateSchema,
    ClientSchema,
    ClientUpdateSchema,
    ClientWebsiteCreateSchema,
    ClientWebsiteSchema,
)
from .services import ClientService


router = Router(
    tags=["Clients"],
    auth=jwt_auth,
)


def serialize_contact(contact):
    return {
        "id": contact.id,
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "position": contact.position,
        "department": contact.department,
        "email": contact.email,
        "phone": contact.phone,
        "whatsapp": contact.whatsapp,
        "is_primary": contact.is_primary,
        "receives_quotations": contact.receives_quotations,
        "receives_invoices": contact.receives_invoices,
        "receives_project_updates": contact.receives_project_updates,
        "notes": contact.notes,
        "created_at": contact.created_at,
    }


def serialize_website(website):
    return {
        "id": website.id,
        "name": website.name,
        "url": website.url,
        "platform": website.platform,
        "admin_url": website.admin_url,
        "is_primary": website.is_primary,
        "is_active": website.is_active,
        "notes": website.notes,
        "created_at": website.created_at,
    }


def serialize_client(client):
    return {
        "id": client.id,
        "client_code": client.client_code,
        "company_name": client.company_name,
        "legal_name": client.legal_name,
        "client_type": client.client_type,
        "status": client.status,
        "industry": client.industry,
        "country": client.country,
        "timezone": client.timezone,
        "email": client.email,
        "phone": client.phone,
        "whatsapp": client.whatsapp,
        "website": client.website,
        "tax_number": client.tax_number,
        "registration_number": client.registration_number,
        "billing_address": client.billing_address,
        "shipping_address": client.shipping_address,
        "default_currency": client.default_currency,
        "payment_terms_days": client.payment_terms_days,
        "notes": client.notes,
        "tags": client.tags,
        "source_lead_id": client.source_lead_id,
        "contacts": [
            serialize_contact(contact)
            for contact in client.contacts.all()
        ],
        "websites": [
            serialize_website(website)
            for website in client.websites.all()
        ],
        "created_at": client.created_at,
        "updated_at": client.updated_at,
    }


def normalize_client_values(payload):
    values = payload.dict()
    email = values.get("email")
    values["email"] = str(email) if email else ""
    return values


def normalize_contact_values(payload):
    values = payload.dict()
    email = values.get("email")
    values["email"] = str(email) if email else ""
    return values


@router.get(
    "",
    response={
        200: PaginatedResponseSchema[ClientSchema],
        403: ErrorSchema,
    },
)
@require_permissions("clients.view_client")
def list_clients(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    status: str | None = None,
    client_type: str | None = None,
    country: str | None = None,
    industry: str | None = None,
    ordering: str | None = None,
):
    queryset = ClientRepository.search(
        search=search,
        status=status,
        client_type=client_type,
        country=country,
        industry=industry,
        ordering=ordering,
    )

    result = paginate_queryset(
        queryset,
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_client,
    )


@router.post(
    "",
    response={
        201: ClientSchema,
        403: ErrorSchema,
    },
)
@require_permissions("clients.add_client")
def create_client(request, payload: ClientCreateSchema):
    client = ClientService.create_client(
        request=request,
        values=normalize_client_values(payload),
    )

    return 201, serialize_client(client)


@router.get(
    "/{client_id}",
    response={
        200: ClientSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("clients.view_client")
def get_client(request, client_id: str):
    client = ClientRepository.find_by_id(client_id)

    if client is None:
        raise ApiHttpError(
            404,
            "Client not found.",
            code="client_not_found",
        )

    return serialize_client(client)


@router.put(
    "/{client_id}",
    response={
        200: ClientSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("clients.change_client")
def update_client(
    request,
    client_id: str,
    payload: ClientUpdateSchema,
):
    client = ClientRepository.find_by_id(client_id)

    if client is None:
        raise ApiHttpError(
            404,
            "Client not found.",
            code="client_not_found",
        )

    client = ClientService.update_client(
        request=request,
        client=client,
        values=normalize_client_values(payload),
    )

    return serialize_client(client)


@router.delete(
    "/{client_id}",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("clients.delete_client")
def delete_client(request, client_id: str):
    client = ClientRepository.find_by_id(client_id)

    if client is None:
        raise ApiHttpError(
            404,
            "Client not found.",
            code="client_not_found",
        )

    ClientService.soft_delete_client(
        request=request,
        client=client,
    )

    return {
        "status": "ok",
        "message": "Client deleted successfully.",
    }


@router.post(
    "/{client_id}/contacts",
    response={
        201: ClientContactSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("clients.add_clientcontact")
def add_contact(
    request,
    client_id: str,
    payload: ClientContactCreateSchema,
):
    client = ClientRepository.find_by_id(client_id)

    if client is None:
        raise ApiHttpError(
            404,
            "Client not found.",
            code="client_not_found",
        )

    contact = ClientService.add_contact(
        request=request,
        client=client,
        values=normalize_contact_values(payload),
    )

    return 201, serialize_contact(contact)


@router.post(
    "/{client_id}/websites",
    response={
        201: ClientWebsiteSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("clients.add_clientwebsite")
def add_website(
    request,
    client_id: str,
    payload: ClientWebsiteCreateSchema,
):
    client = ClientRepository.find_by_id(client_id)

    if client is None:
        raise ApiHttpError(
            404,
            "Client not found.",
            code="client_not_found",
        )

    website = ClientService.add_website(
        request=request,
        client=client,
        values=payload.dict(),
    )

    return 201, serialize_website(website)


@router.post(
    "/convert-lead/{lead_id}",
    response={
        201: ClientSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("clients.add_client")
def convert_lead(request, lead_id: str):
    lead = LeadRepository.find_by_id(lead_id)

    if lead is None:
        raise ApiHttpError(
            404,
            "Lead not found.",
            code="lead_not_found",
        )

    client = ClientService.convert_lead(
        request=request,
        lead=lead,
    )

    return 201, serialize_client(client)
