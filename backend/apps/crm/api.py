from django.core.exceptions import ObjectDoesNotExist
from ninja import Router

from apps.accounts.models import User
from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema, MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.api.pagination_schemas import (
    PaginatedResponseSchema,
)
from apps.api.responses import paginated_response
from apps.common.pagination import paginate_queryset
from apps.rbac.services import require_permissions

from .models import Lead
from .repositories import LeadRepository
from .schemas import (
    LeadCreateSchema,
    LeadNoteCreateSchema,
    LeadNoteSchema,
    LeadSchema,
    LeadTimelineSchema,
    LeadUpdateSchema,
)
from .services import LeadService


router = Router(
    tags=["CRM Leads"],
    auth=jwt_auth,
)


def serialize_user(user):
    if user is None:
        return None

    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


def serialize_lead(lead):
    return {
        "id": lead.id,
        "name": lead.name,
        "company": lead.company,
        "email": lead.email,
        "phone": lead.phone,
        "whatsapp": lead.whatsapp,
        "country": lead.country,
        "website": lead.website,
        "source": lead.source,
        "status": lead.status,
        "priority": lead.priority,
        "assigned_to": serialize_user(
            lead.assigned_to
        ),
        "lead_score": lead.lead_score,
        "estimated_value": lead.estimated_value,
        "currency": lead.currency,
        "notes": lead.notes,
        "tags": lead.tags,
        "next_follow_up_at": lead.next_follow_up_at,
        "last_contacted_at": lead.last_contacted_at,
        "created_at": lead.created_at,
        "updated_at": lead.updated_at,
    }


def payload_values(payload):
    values = payload.dict()

    email = values.get("email")
    values["email"] = str(email) if email else ""

    assigned_to_id = values.pop(
        "assigned_to_id",
        None,
    )

    if assigned_to_id:
        try:
            values["assigned_to"] = User.objects.get(
                pk=assigned_to_id,
                is_deleted=False,
                is_active=True,
            )
        except ObjectDoesNotExist as exc:
            raise ApiHttpError(
                400,
                "Assigned user was not found.",
                code="invalid_assigned_user",
            ) from exc
    else:
        values["assigned_to"] = None

    return values


@router.get(
    "",
    response={
        200: PaginatedResponseSchema[LeadSchema],
        403: ErrorSchema,
    },
)
@require_permissions("crm.view_lead")
def list_leads(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    status: str | None = None,
    source: str | None = None,
    assigned_to_id: int | None = None,
    country: str | None = None,
    ordering: str | None = None,
):
    queryset = LeadRepository.search(
        search=search,
        status=status,
        source=source,
        assigned_to_id=assigned_to_id,
        country=country,
        ordering=ordering,
    )

    result = paginate_queryset(
        queryset,
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_lead,
    )


@router.post(
    "",
    response={
        201: LeadSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("crm.add_lead")
def create_lead(request, payload: LeadCreateSchema):
    lead = LeadService.create_lead(
        request=request,
        values=payload_values(payload),
    )

    return 201, serialize_lead(lead)


@router.get(
    "/{lead_id}",
    response={
        200: LeadSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("crm.view_lead")
def get_lead(request, lead_id: str):
    lead = LeadRepository.find_by_id(lead_id)

    if lead is None:
        raise ApiHttpError(
            404,
            "Lead not found.",
            code="lead_not_found",
        )

    return serialize_lead(lead)


@router.put(
    "/{lead_id}",
    response={
        200: LeadSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("crm.change_lead")
def update_lead(
    request,
    lead_id: str,
    payload: LeadUpdateSchema,
):
    lead = LeadRepository.find_by_id(lead_id)

    if lead is None:
        raise ApiHttpError(
            404,
            "Lead not found.",
            code="lead_not_found",
        )

    lead = LeadService.update_lead(
        request=request,
        lead=lead,
        values=payload_values(payload),
    )

    return serialize_lead(lead)


@router.delete(
    "/{lead_id}",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("crm.delete_lead")
def delete_lead(request, lead_id: str):
    lead = LeadRepository.find_by_id(lead_id)

    if lead is None:
        raise ApiHttpError(
            404,
            "Lead not found.",
            code="lead_not_found",
        )

    LeadService.soft_delete_lead(
        request=request,
        lead=lead,
    )

    return {
        "status": "ok",
        "message": "Lead deleted successfully.",
    }


@router.post(
    "/{lead_id}/notes",
    response={
        201: LeadNoteSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("crm.add_leadnote")
def add_lead_note(
    request,
    lead_id: str,
    payload: LeadNoteCreateSchema,
):
    lead = LeadRepository.find_by_id(lead_id)

    if lead is None:
        raise ApiHttpError(
            404,
            "Lead not found.",
            code="lead_not_found",
        )

    note = LeadService.add_note(
        request=request,
        lead=lead,
        content=payload.content,
        is_pinned=payload.is_pinned,
    )

    return 201, note


@router.get(
    "/{lead_id}/timeline",
    response={
        200: list[LeadTimelineSchema],
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("crm.view_leadtimeline")
def lead_timeline(request, lead_id: str):
    lead = LeadRepository.find_by_id(lead_id)

    if lead is None:
        raise ApiHttpError(
            404,
            "Lead not found.",
            code="lead_not_found",
        )

    return lead.timeline_entries.all()
