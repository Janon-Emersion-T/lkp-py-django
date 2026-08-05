from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema, MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.api.pagination_schemas import PaginatedResponseSchema
from apps.api.responses import paginated_response
from apps.clients.models import Client
from apps.common.pagination import paginate_queryset
from apps.crm.models import Lead
from apps.rbac.services import require_permissions

from .models import QuotationStatus
from .repositories import QuotationRepository
from .schemas import (
    QuotationAcceptSchema,
    QuotationCreateSchema,
    QuotationPdfPayloadSchema,
    QuotationRejectSchema,
    QuotationSchema,
    QuotationUpdateSchema,
)
from .services import QuotationService


router = Router(
    tags=["Quotations"],
    auth=jwt_auth,
)


def serialize_item(item):
    return {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "quantity": item.quantity,
        "unit_price": item.unit_price,
        "discount_amount": item.discount_amount,
        "tax_rate": item.tax_rate,
        "subtotal": item.subtotal,
        "tax_amount": item.tax_amount,
        "total_amount": item.total_amount,
        "sort_order": item.sort_order,
    }


def serialize_recipient(recipient):
    return {
        "id": recipient.id,
        "name": recipient.name,
        "email": recipient.email,
        "is_primary": recipient.is_primary,
        "received_at": recipient.received_at,
        "viewed_at": recipient.viewed_at,
    }


def serialize_event(event):
    return {
        "id": event.id,
        "event_type": event.event_type,
        "description": event.description,
        "metadata": event.metadata,
        "created_at": event.created_at,
    }


def serialize_quotation(quotation):
    return {
        "id": quotation.id,
        "quotation_number": quotation.quotation_number,
        "client_id": quotation.client_id,
        "client_name": quotation.client.company_name,
        "lead_id": quotation.lead_id,
        "title": quotation.title,
        "subject": quotation.subject,
        "description": quotation.description,
        "status": quotation.status,
        "issue_date": quotation.issue_date,
        "expiry_date": quotation.expiry_date,
        "currency": quotation.currency,
        "subtotal": quotation.subtotal,
        "discount_amount": quotation.discount_amount,
        "tax_amount": quotation.tax_amount,
        "total_amount": quotation.total_amount,
        "terms": quotation.terms,
        "notes": quotation.notes,
        "accepted_at": quotation.accepted_at,
        "accepted_by_name": quotation.accepted_by_name,
        "accepted_by_email": quotation.accepted_by_email,
        "sent_at": quotation.sent_at,
        "duplicated_from_id": quotation.duplicated_from_id,
        "is_expired": quotation.is_expired,
        "items": [
            serialize_item(item)
            for item in quotation.items.all()
        ],
        "recipients": [
            serialize_recipient(recipient)
            for recipient in quotation.recipients.all()
        ],
        "events": [
            serialize_event(event)
            for event in quotation.events.all()
        ],
        "created_at": quotation.created_at,
        "updated_at": quotation.updated_at,
    }


def resolve_relations(payload):
    try:
        client = Client.objects.get(pk=payload.client_id)
    except ObjectDoesNotExist as exc:
        raise ApiHttpError(
            400,
            "Client not found.",
            code="invalid_client",
        ) from exc

    lead = None

    if payload.lead_id:
        try:
            lead = Lead.objects.get(pk=payload.lead_id)
        except ObjectDoesNotExist as exc:
            raise ApiHttpError(
                400,
                "Lead not found.",
                code="invalid_lead",
            ) from exc

    return client, lead


def item_values(items):
    return [
        item.dict()
        for item in items
    ]


def recipient_values(recipients):
    return [
        {
            **recipient.dict(),
            "email": str(recipient.email),
        }
        for recipient in recipients
    ]


@router.get(
    "",
    response={
        200: PaginatedResponseSchema[QuotationSchema],
        403: ErrorSchema,
    },
)
@require_permissions("quotations.view_quotation")
def list_quotations(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    status: str | None = None,
    client_id: str | None = None,
    currency: str | None = None,
    ordering: str | None = None,
):
    queryset = QuotationRepository.search(
        search=search,
        status=status,
        client_id=client_id,
        currency=currency,
        ordering=ordering,
    )

    result = paginate_queryset(
        queryset,
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_quotation,
    )


@router.post(
    "",
    response={
        201: QuotationSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("quotations.add_quotation")
def create_quotation(
    request,
    payload: QuotationCreateSchema,
):
    client, lead = resolve_relations(payload)

    values = {
        "client": client,
        "lead": lead,
        "title": payload.title,
        "subject": payload.subject,
        "description": payload.description,
        "currency": payload.currency.upper(),
        "discount_amount": payload.discount_amount,
        "tax_amount": payload.tax_amount,
        "terms": payload.terms,
        "notes": payload.notes,
    }

    if payload.issue_date:
        values["issue_date"] = payload.issue_date

    if payload.expiry_date:
        values["expiry_date"] = payload.expiry_date

    quotation = QuotationService.create_quotation(
        request=request,
        values=values,
        items=item_values(payload.items),
        recipients=recipient_values(payload.recipients),
    )

    return 201, serialize_quotation(quotation)


@router.get(
    "/{quotation_id}",
    response={
        200: QuotationSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("quotations.view_quotation")
def get_quotation(request, quotation_id: str):
    quotation = QuotationRepository.find_by_id(
        quotation_id
    )

    if quotation is None:
        raise ApiHttpError(
            404,
            "Quotation not found.",
            code="quotation_not_found",
        )

    return serialize_quotation(quotation)


@router.put(
    "/{quotation_id}",
    response={
        200: QuotationSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("quotations.change_quotation")
def update_quotation(
    request,
    quotation_id: str,
    payload: QuotationUpdateSchema,
):
    quotation = QuotationRepository.find_by_id(
        quotation_id
    )

    if quotation is None:
        raise ApiHttpError(
            404,
            "Quotation not found.",
            code="quotation_not_found",
        )

    try:
        quotation = QuotationService.update_quotation(
            request=request,
            quotation=quotation,
            values={
                "title": payload.title,
                "subject": payload.subject,
                "description": payload.description,
                "issue_date": payload.issue_date,
                "expiry_date": payload.expiry_date,
                "currency": payload.currency.upper(),
                "discount_amount": payload.discount_amount,
                "tax_amount": payload.tax_amount,
                "terms": payload.terms,
                "notes": payload.notes,
            },
            items=item_values(payload.items),
            recipients=recipient_values(
                payload.recipients
            ),
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_quotation_operation",
        ) from exc

    return serialize_quotation(quotation)


@router.delete(
    "/{quotation_id}",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("quotations.delete_quotation")
def delete_quotation(request, quotation_id: str):
    quotation = QuotationRepository.find_by_id(
        quotation_id
    )

    if quotation is None:
        raise ApiHttpError(
            404,
            "Quotation not found.",
            code="quotation_not_found",
        )

    QuotationService.soft_delete(
        request=request,
        quotation=quotation,
    )

    return {
        "status": "ok",
        "message": "Quotation deleted successfully.",
    }


@router.post(
    "/{quotation_id}/duplicate",
    response={
        201: QuotationSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("quotations.add_quotation")
def duplicate_quotation(request, quotation_id: str):
    quotation = QuotationRepository.find_by_id(
        quotation_id
    )

    if quotation is None:
        raise ApiHttpError(
            404,
            "Quotation not found.",
            code="quotation_not_found",
        )

    duplicate = QuotationService.duplicate(
        request=request,
        quotation=quotation,
    )

    return 201, serialize_quotation(duplicate)


@router.post(
    "/{quotation_id}/send",
    response={
        200: QuotationSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("quotations.change_quotation")
def send_quotation(request, quotation_id: str):
    quotation = QuotationRepository.find_by_id(
        quotation_id
    )

    if quotation is None:
        raise ApiHttpError(
            404,
            "Quotation not found.",
            code="quotation_not_found",
        )

    try:
        quotation = QuotationService.mark_sent(
            request=request,
            quotation=quotation,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_quotation_operation",
        ) from exc

    return serialize_quotation(quotation)


@router.post(
    "/{quotation_id}/accept",
    response={
        200: QuotationSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("quotations.change_quotation")
def accept_quotation(
    request,
    quotation_id: str,
    payload: QuotationAcceptSchema,
):
    quotation = QuotationRepository.find_by_id(
        quotation_id
    )

    if quotation is None:
        raise ApiHttpError(
            404,
            "Quotation not found.",
            code="quotation_not_found",
        )

    try:
        quotation = QuotationService.accept(
            request=request,
            quotation=quotation,
            accepted_by_name=payload.accepted_by_name,
            accepted_by_email=str(
                payload.accepted_by_email
            ),
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_quotation_operation",
        ) from exc

    return serialize_quotation(quotation)


@router.post(
    "/{quotation_id}/reject",
    response={
        200: QuotationSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("quotations.change_quotation")
def reject_quotation(
    request,
    quotation_id: str,
    payload: QuotationRejectSchema,
):
    quotation = QuotationRepository.find_by_id(
        quotation_id
    )

    if quotation is None:
        raise ApiHttpError(
            404,
            "Quotation not found.",
            code="quotation_not_found",
        )

    try:
        quotation = QuotationService.reject(
            request=request,
            quotation=quotation,
            reason=payload.reason,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_quotation_operation",
        ) from exc

    return serialize_quotation(quotation)


@router.get(
    "/{quotation_id}/pdf-data",
    response={
        200: QuotationPdfPayloadSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("quotations.view_quotation")
def quotation_pdf_data(request, quotation_id: str):
    quotation = QuotationRepository.find_by_id(
        quotation_id
    )

    if quotation is None:
        raise ApiHttpError(
            404,
            "Quotation not found.",
            code="quotation_not_found",
        )

    client = quotation.client

    return {
        "company": {
            "name": "LKProfessionals (Pvt) Ltd",
            "timezone": "Asia/Colombo",
        },
        "client": {
            "client_code": client.client_code,
            "company_name": client.company_name,
            "legal_name": client.legal_name,
            "email": client.email,
            "phone": client.phone,
            "billing_address": client.billing_address,
            "country": client.country,
        },
        "quotation": {
            "quotation_number": (
                quotation.quotation_number
            ),
            "title": quotation.title,
            "subject": quotation.subject,
            "description": quotation.description,
            "status": quotation.status,
            "issue_date": quotation.issue_date,
            "expiry_date": quotation.expiry_date,
            "currency": quotation.currency,
            "terms": quotation.terms,
            "notes": quotation.notes,
            "generated_at": timezone.now(),
        },
        "items": [
            serialize_item(item)
            for item in quotation.items.all()
        ],
        "totals": {
            "subtotal": quotation.subtotal,
            "discount_amount": (
                quotation.discount_amount
            ),
            "tax_amount": quotation.tax_amount,
            "total_amount": quotation.total_amount,
        },
    }
