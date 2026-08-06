from django.core.exceptions import ValidationError
from ninja import Router

from apps.accounts.models import User
from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.api.exceptions import ApiHttpError
from apps.clients.models import Client
from apps.crm.models import Lead
from apps.packages_catalog.models import Package
from apps.rbac.services import require_permissions
from apps.services_catalog.models import Service

from .models import ContactEnquiry, QuoteEnquiry
from .repositories import (
    ContactEnquiryRepository,
    QuoteEnquiryRepository,
)
from .schemas import (
    ContactEnquiryCreateSchema,
    ContactEnquirySchema,
    EnquiryAssignmentSchema,
    EnquiryNoteCreateSchema,
    EnquiryNoteSchema,
    EnquiryStatusUpdateSchema,
    QuoteEnquiryCreateSchema,
    QuoteEnquirySchema,
)
from .services import EnquiryService


router = Router(
    tags=["Contact and Quote Enquiries"],
    auth=jwt_auth,
)


def get_contact_enquiry(enquiry_id):
    enquiry = ContactEnquiryRepository.find_by_id(
        enquiry_id
    )

    if enquiry is None:
        raise ApiHttpError(
            404,
            "Contact enquiry not found.",
            code="contact_enquiry_not_found",
        )

    return enquiry


def get_quote_enquiry(enquiry_id):
    enquiry = QuoteEnquiryRepository.find_by_id(
        enquiry_id
    )

    if enquiry is None:
        raise ApiHttpError(
            404,
            "Quote enquiry not found.",
            code="quote_enquiry_not_found",
        )

    return enquiry


def resolve_user(user_id):
    if user_id is None:
        return None

    user = User.objects.filter(pk=user_id).first()

    if user is None:
        raise ApiHttpError(
            400,
            "Assigned user not found.",
            code="invalid_assigned_user",
        )

    return user


def resolve_client(client_id):
    if client_id is None:
        return None

    client = Client.objects.filter(pk=client_id).first()

    if client is None:
        raise ApiHttpError(
            400,
            "Client not found.",
            code="invalid_client",
        )

    return client


def resolve_lead(lead_id):
    if lead_id is None:
        return None

    lead = Lead.objects.filter(pk=lead_id).first()

    if lead is None:
        raise ApiHttpError(
            400,
            "Lead not found.",
            code="invalid_lead",
        )

    return lead


def resolve_package(package_id):
    if package_id is None:
        return None

    package = Package.objects.filter(
        pk=package_id,
    ).first()

    if package is None:
        raise ApiHttpError(
            400,
            "Package not found.",
            code="invalid_package",
        )

    return package


def resolve_services(items):
    service_ids = [
        item.service_id
        for item in items
    ]

    services = {
        service.id: service
        for service in Service.objects.filter(
            id__in=service_ids,
        )
    }

    if len(services) != len(set(service_ids)):
        raise ApiHttpError(
            400,
            "One or more services are invalid.",
            code="invalid_services",
        )

    return [
        {
            "service": services[item.service_id],
            "notes": item.notes,
            "sort_order": item.sort_order,
        }
        for item in items
    ]


def serialize_note(note):
    return {
        "id": note.id,
        "author_id": note.author_id,
        "author_name": (
            str(note.author)
            if note.author
            else None
        ),
        "note": note.note,
        "is_private": note.is_private,
        "created_at": note.created_at,
    }


def serialize_contact(enquiry):
    return {
        "id": enquiry.id,
        "reference_code": enquiry.reference_code,
        "name": enquiry.name,
        "email": enquiry.email,
        "phone": enquiry.phone,
        "company_name": enquiry.company_name,
        "subject": enquiry.subject,
        "message": enquiry.message,
        "source": enquiry.source,
        "source_url": enquiry.source_url,
        "status": enquiry.status,
        "priority": enquiry.priority,
        "assigned_to_id": enquiry.assigned_to_id,
        "assigned_to_name": (
            str(enquiry.assigned_to)
            if enquiry.assigned_to
            else None
        ),
        "client_id": enquiry.client_id,
        "lead_id": enquiry.lead_id,
        "submitted_at": enquiry.submitted_at,
        "first_contacted_at": (
            enquiry.first_contacted_at
        ),
        "resolved_at": enquiry.resolved_at,
        "last_follow_up_at": (
            enquiry.last_follow_up_at
        ),
        "next_follow_up_at": (
            enquiry.next_follow_up_at
        ),
        "internal_summary": (
            enquiry.internal_summary
        ),
        "loss_reason": enquiry.loss_reason,
        "metadata": enquiry.metadata,
        "notes": [
            serialize_note(note)
            for note in enquiry.notes.all()
        ],
        "created_at": enquiry.created_at,
        "updated_at": enquiry.updated_at,
    }


def serialize_quote(enquiry):
    return {
        "id": enquiry.id,
        "reference_code": enquiry.reference_code,
        "name": enquiry.name,
        "email": enquiry.email,
        "phone": enquiry.phone,
        "company_name": enquiry.company_name,
        "country": enquiry.country,
        "website_url": enquiry.website_url,
        "project_title": enquiry.project_title,
        "project_description": (
            enquiry.project_description
        ),
        "preferred_package_id": (
            enquiry.preferred_package_id
        ),
        "budget_min": enquiry.budget_min,
        "budget_max": enquiry.budget_max,
        "budget_currency": enquiry.budget_currency,
        "desired_start_date": (
            enquiry.desired_start_date
        ),
        "desired_completion_date": (
            enquiry.desired_completion_date
        ),
        "source": enquiry.source,
        "source_url": enquiry.source_url,
        "status": enquiry.status,
        "priority": enquiry.priority,
        "assigned_to_id": enquiry.assigned_to_id,
        "assigned_to_name": (
            str(enquiry.assigned_to)
            if enquiry.assigned_to
            else None
        ),
        "client_id": enquiry.client_id,
        "lead_id": enquiry.lead_id,
        "quotation_id": enquiry.quotation_id,
        "submitted_at": enquiry.submitted_at,
        "first_contacted_at": (
            enquiry.first_contacted_at
        ),
        "resolved_at": enquiry.resolved_at,
        "last_follow_up_at": (
            enquiry.last_follow_up_at
        ),
        "next_follow_up_at": (
            enquiry.next_follow_up_at
        ),
        "internal_summary": (
            enquiry.internal_summary
        ),
        "loss_reason": enquiry.loss_reason,
        "metadata": enquiry.metadata,
        "services": [
            {
                "id": item.id,
                "service_id": item.service_id,
                "service_title": item.service.title,
                "notes": item.notes,
                "sort_order": item.sort_order,
            }
            for item in enquiry.service_links.all()
        ],
        "notes": [
            serialize_note(note)
            for note in enquiry.notes.all()
        ],
        "created_at": enquiry.created_at,
        "updated_at": enquiry.updated_at,
    }


@router.get(
    "/contacts",
    response={
        200: list[ContactEnquirySchema],
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.view_contactenquiry")
def list_contact_enquiries(
    request,
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    source: str | None = None,
    assigned_to_id: str | None = None,
    ordering: str | None = None,
):
    return [
        serialize_contact(enquiry)
        for enquiry in ContactEnquiryRepository.search(
            search=search,
            status=status,
            priority=priority,
            source=source,
            assigned_to_id=assigned_to_id,
            ordering=ordering,
        )
    ]


@router.post(
    "/contacts",
    response={
        201: ContactEnquirySchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.add_contactenquiry")
def create_contact_enquiry(
    request,
    payload: ContactEnquiryCreateSchema,
):
    if ContactEnquiry.all_objects.filter(
        reference_code=payload.reference_code,
    ).exists():
        raise ApiHttpError(
            400,
            "Contact enquiry reference already exists.",
            code="duplicate_contact_reference",
        )

    values = payload.dict()

    assigned_to_id = values.pop("assigned_to_id")
    client_id = values.pop("client_id")
    lead_id = values.pop("lead_id")

    values["assigned_to"] = resolve_user(
        assigned_to_id
    )
    values["client"] = resolve_client(client_id)
    values["lead"] = resolve_lead(lead_id)

    enquiry = EnquiryService.create_contact_enquiry(
        request=request,
        values=values,
    )

    return 201, serialize_contact(
        get_contact_enquiry(enquiry.id)
    )


@router.get(
    "/contacts/{enquiry_id}",
    response={
        200: ContactEnquirySchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.view_contactenquiry")
def contact_enquiry_detail(
    request,
    enquiry_id: str,
):
    return serialize_contact(
        get_contact_enquiry(enquiry_id)
    )


@router.get(
    "/quotes",
    response={
        200: list[QuoteEnquirySchema],
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.view_quoteenquiry")
def list_quote_enquiries(
    request,
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    source: str | None = None,
    country: str | None = None,
    assigned_to_id: str | None = None,
    service_id: str | None = None,
    ordering: str | None = None,
):
    return [
        serialize_quote(enquiry)
        for enquiry in QuoteEnquiryRepository.search(
            search=search,
            status=status,
            priority=priority,
            source=source,
            country=country,
            assigned_to_id=assigned_to_id,
            service_id=service_id,
            ordering=ordering,
        )
    ]


@router.post(
    "/quotes",
    response={
        201: QuoteEnquirySchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.add_quoteenquiry")
def create_quote_enquiry(
    request,
    payload: QuoteEnquiryCreateSchema,
):
    if QuoteEnquiry.all_objects.filter(
        reference_code=payload.reference_code,
    ).exists():
        raise ApiHttpError(
            400,
            "Quote enquiry reference already exists.",
            code="duplicate_quote_reference",
        )

    values = payload.dict()

    services = resolve_services(
        payload.services
    )

    values.pop("services")
    assigned_to_id = values.pop("assigned_to_id")
    client_id = values.pop("client_id")
    lead_id = values.pop("lead_id")
    package_id = values.pop(
        "preferred_package_id"
    )

    values["assigned_to"] = resolve_user(
        assigned_to_id
    )
    values["client"] = resolve_client(client_id)
    values["lead"] = resolve_lead(lead_id)
    values["preferred_package"] = (
        resolve_package(package_id)
    )

    enquiry = QuoteEnquiry(**values)

    try:
        enquiry.full_clean()
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Quote enquiry validation failed.",
            code="invalid_quote_enquiry",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    enquiry = EnquiryService.create_quote_enquiry(
        request=request,
        values=values,
        services=services,
    )

    return 201, serialize_quote(
        get_quote_enquiry(enquiry.id)
    )


@router.get(
    "/quotes/{enquiry_id}",
    response={
        200: QuoteEnquirySchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.view_quoteenquiry")
def quote_enquiry_detail(
    request,
    enquiry_id: str,
):
    return serialize_quote(
        get_quote_enquiry(enquiry_id)
    )


def update_status_response(
    *,
    request,
    enquiry,
    payload,
    serializer,
    getter,
):
    enquiry = EnquiryService.update_status(
        request=request,
        enquiry=enquiry,
        status=payload.status,
        loss_reason=payload.loss_reason,
    )

    return serializer(getter(enquiry.id))


@router.post(
    "/contacts/{enquiry_id}/status",
    response={
        200: ContactEnquirySchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.change_contactenquiry")
def update_contact_status(
    request,
    enquiry_id: str,
    payload: EnquiryStatusUpdateSchema,
):
    return update_status_response(
        request=request,
        enquiry=get_contact_enquiry(enquiry_id),
        payload=payload,
        serializer=serialize_contact,
        getter=get_contact_enquiry,
    )


@router.post(
    "/quotes/{enquiry_id}/status",
    response={
        200: QuoteEnquirySchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.change_quoteenquiry")
def update_quote_status(
    request,
    enquiry_id: str,
    payload: EnquiryStatusUpdateSchema,
):
    return update_status_response(
        request=request,
        enquiry=get_quote_enquiry(enquiry_id),
        payload=payload,
        serializer=serialize_quote,
        getter=get_quote_enquiry,
    )


def assignment_response(
    *,
    request,
    enquiry,
    payload,
    serializer,
    getter,
):
    enquiry = EnquiryService.assign_enquiry(
        request=request,
        enquiry=enquiry,
        assigned_to=resolve_user(
            payload.assigned_to_id
        ),
        priority=payload.priority,
        internal_summary=(
            payload.internal_summary
        ),
        next_follow_up_at=(
            payload.next_follow_up_at
        ),
    )

    return serializer(getter(enquiry.id))


@router.put(
    "/contacts/{enquiry_id}/assignment",
    response={
        200: ContactEnquirySchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.change_contactenquiry")
def assign_contact_enquiry(
    request,
    enquiry_id: str,
    payload: EnquiryAssignmentSchema,
):
    return assignment_response(
        request=request,
        enquiry=get_contact_enquiry(enquiry_id),
        payload=payload,
        serializer=serialize_contact,
        getter=get_contact_enquiry,
    )


@router.put(
    "/quotes/{enquiry_id}/assignment",
    response={
        200: QuoteEnquirySchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.change_quoteenquiry")
def assign_quote_enquiry(
    request,
    enquiry_id: str,
    payload: EnquiryAssignmentSchema,
):
    return assignment_response(
        request=request,
        enquiry=get_quote_enquiry(enquiry_id),
        payload=payload,
        serializer=serialize_quote,
        getter=get_quote_enquiry,
    )


@router.post(
    "/contacts/{enquiry_id}/notes",
    response={
        201: EnquiryNoteSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.add_enquirynote")
def add_contact_note(
    request,
    enquiry_id: str,
    payload: EnquiryNoteCreateSchema,
):
    note = EnquiryService.add_note(
        request=request,
        contact_enquiry=get_contact_enquiry(
            enquiry_id
        ),
        note=payload.note,
        is_private=payload.is_private,
    )

    return 201, serialize_note(note)


@router.post(
    "/quotes/{enquiry_id}/notes",
    response={
        201: EnquiryNoteSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.add_enquirynote")
def add_quote_note(
    request,
    enquiry_id: str,
    payload: EnquiryNoteCreateSchema,
):
    note = EnquiryService.add_note(
        request=request,
        quote_enquiry=get_quote_enquiry(
            enquiry_id
        ),
        note=payload.note,
        is_private=payload.is_private,
    )

    return 201, serialize_note(note)



from .repositories import EnquiryDashboardRepository
from .schemas import (
    ContactEnquiryUpdateSchema,
    EnquiryDashboardSchema,
    EnquiryFollowUpSchema,
    QuoteEnquiryUpdateSchema,
)


def contact_update_values(payload):
    values = payload.dict()

    values.pop("reference_code", None)

    assigned_to_id = values.pop("assigned_to_id")
    client_id = values.pop("client_id")
    lead_id = values.pop("lead_id")

    values["assigned_to"] = resolve_user(
        assigned_to_id
    )
    values["client"] = resolve_client(client_id)
    values["lead"] = resolve_lead(lead_id)

    return values


def quote_update_values(payload):
    values = payload.dict()

    values.pop("reference_code", None)
    values.pop("services")

    assigned_to_id = values.pop("assigned_to_id")
    client_id = values.pop("client_id")
    lead_id = values.pop("lead_id")
    package_id = values.pop(
        "preferred_package_id"
    )

    values["assigned_to"] = resolve_user(
        assigned_to_id
    )
    values["client"] = resolve_client(client_id)
    values["lead"] = resolve_lead(lead_id)
    values["preferred_package"] = (
        resolve_package(package_id)
    )

    return values


@router.put(
    "/contacts/{enquiry_id}",
    response={
        200: ContactEnquirySchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.change_contactenquiry")
def update_contact_enquiry(
    request,
    enquiry_id: str,
    payload: ContactEnquiryUpdateSchema,
):
    enquiry = EnquiryService.update_contact_enquiry(
        request=request,
        enquiry=get_contact_enquiry(enquiry_id),
        values=contact_update_values(payload),
    )

    return serialize_contact(
        get_contact_enquiry(enquiry.id)
    )


@router.put(
    "/quotes/{enquiry_id}",
    response={
        200: QuoteEnquirySchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.change_quoteenquiry")
def update_quote_enquiry(
    request,
    enquiry_id: str,
    payload: QuoteEnquiryUpdateSchema,
):
    services = resolve_services(
        payload.services
    )

    try:
        enquiry = (
            EnquiryService.update_quote_enquiry(
                request=request,
                enquiry=get_quote_enquiry(
                    enquiry_id
                ),
                values=quote_update_values(payload),
                services=services,
            )
        )
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Quote enquiry validation failed.",
            code="invalid_quote_enquiry",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    return serialize_quote(
        get_quote_enquiry(enquiry.id)
    )


def complete_follow_up_response(
    *,
    request,
    enquiry,
    payload,
    serializer,
    getter,
):
    enquiry = EnquiryService.complete_follow_up(
        request=request,
        enquiry=enquiry,
        next_follow_up_at=(
            payload.next_follow_up_at
        ),
    )

    return serializer(getter(enquiry.id))


@router.post(
    "/contacts/{enquiry_id}/follow-up",
    response={
        200: ContactEnquirySchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.change_contactenquiry")
def complete_contact_follow_up(
    request,
    enquiry_id: str,
    payload: EnquiryFollowUpSchema,
):
    return complete_follow_up_response(
        request=request,
        enquiry=get_contact_enquiry(enquiry_id),
        payload=payload,
        serializer=serialize_contact,
        getter=get_contact_enquiry,
    )


@router.post(
    "/quotes/{enquiry_id}/follow-up",
    response={
        200: QuoteEnquirySchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.change_quoteenquiry")
def complete_quote_follow_up(
    request,
    enquiry_id: str,
    payload: EnquiryFollowUpSchema,
):
    return complete_follow_up_response(
        request=request,
        enquiry=get_quote_enquiry(enquiry_id),
        payload=payload,
        serializer=serialize_quote,
        getter=get_quote_enquiry,
    )


@router.get(
    "/dashboard",
    response={
        200: EnquiryDashboardSchema,
        403: ErrorSchema,
    },
)
@require_permissions("enquiries.view_contactenquiry")
def enquiry_dashboard(request):
    return EnquiryDashboardRepository.statistics()
