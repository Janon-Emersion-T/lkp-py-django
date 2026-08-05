from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema, MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.api.pagination_schemas import PaginatedResponseSchema
from apps.api.responses import paginated_response
from apps.clients.models import Client
from apps.common.pagination import paginate_queryset
from apps.quotations.models import Quotation
from apps.rbac.services import require_permissions

from .models import ProjectMilestone
from .repositories import ProjectRepository
from .schemas import (
    ProjectCreateSchema,
    ProjectMilestoneCreateSchema,
    ProjectMilestoneSchema,
    ProjectMilestoneUpdateSchema,
    ProjectNoteCreateSchema,
    ProjectNoteSchema,
    ProjectSchema,
    ProjectTeamMemberCreateSchema,
    ProjectTeamMemberSchema,
    ProjectUpdateSchema,
)
from .services import ProjectService


User = get_user_model()

router = Router(
    tags=["Projects"],
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


def serialize_team_member(assignment):
    return {
        "id": assignment.id,
        "user": serialize_user(assignment.user),
        "role": assignment.role,
        "allocation_percentage": assignment.allocation_percentage,
        "is_active": assignment.is_active,
        "created_at": assignment.created_at,
    }


def serialize_milestone(milestone):
    return {
        "id": milestone.id,
        "title": milestone.title,
        "description": milestone.description,
        "status": milestone.status,
        "start_date": milestone.start_date,
        "due_date": milestone.due_date,
        "completed_at": milestone.completed_at,
        "progress": milestone.progress,
        "sort_order": milestone.sort_order,
        "amount": milestone.amount,
        "created_at": milestone.created_at,
        "updated_at": milestone.updated_at,
    }


def serialize_note(note):
    return {
        "id": note.id,
        "content": note.content,
        "is_pinned": note.is_pinned,
        "is_client_visible": note.is_client_visible,
        "created_at": note.created_at,
    }


def serialize_event(event):
    return {
        "id": event.id,
        "event_type": event.event_type,
        "description": event.description,
        "metadata": event.metadata,
        "created_at": event.created_at,
    }


def serialize_project(project):
    return {
        "id": project.id,
        "project_code": project.project_code,
        "client_id": project.client_id,
        "client_name": project.client.company_name,
        "quotation_id": project.quotation_id,
        "title": project.title,
        "description": project.description,
        "status": project.status,
        "priority": project.priority,
        "budget": project.budget,
        "currency": project.currency,
        "start_date": project.start_date,
        "deadline": project.deadline,
        "completed_at": project.completed_at,
        "progress": project.progress,
        "project_manager": serialize_user(project.project_manager),
        "repository_url": project.repository_url,
        "staging_url": project.staging_url,
        "production_url": project.production_url,
        "notes": project.notes,
        "tags": project.tags,
        "team_members": [
            serialize_team_member(member)
            for member in project.team_members.all()
        ],
        "milestones": [
            serialize_milestone(milestone)
            for milestone in project.milestones.all()
        ],
        "project_notes": [
            serialize_note(note)
            for note in project.project_notes.all()
        ],
        "events": [
            serialize_event(event)
            for event in project.events.all()
        ],
        "created_at": project.created_at,
        "updated_at": project.updated_at,
    }


def resolve_client(client_id):
    try:
        return Client.objects.get(pk=client_id)
    except ObjectDoesNotExist as exc:
        raise ApiHttpError(
            400,
            "Client not found.",
            code="invalid_client",
        ) from exc


def resolve_user(user_id):
    if user_id is None:
        return None

    try:
        return User.objects.get(
            pk=user_id,
            is_deleted=False,
            is_active=True,
        )
    except ObjectDoesNotExist as exc:
        raise ApiHttpError(
            400,
            "User not found.",
            code="invalid_user",
        ) from exc


def project_values(payload, *, require_client=True):
    values = payload.dict()

    client_id = values.pop("client_id", None)
    manager_id = values.pop("project_manager_id", None)

    if require_client:
        if client_id is None:
            raise ApiHttpError(
                400,
                "Client is required.",
                code="invalid_client",
            )

        values["client"] = resolve_client(client_id)
    elif client_id is not None:
        values["client"] = resolve_client(client_id)

    values["project_manager"] = resolve_user(manager_id)
    values["currency"] = values["currency"].upper()

    return values


@router.get(
    "",
    response={
        200: PaginatedResponseSchema[ProjectSchema],
        403: ErrorSchema,
    },
)
@require_permissions("projects.view_project")
def list_projects(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    client_id: str | None = None,
    project_manager_id: int | None = None,
    ordering: str | None = None,
):
    queryset = ProjectRepository.search(
        search=search,
        status=status,
        priority=priority,
        client_id=client_id,
        project_manager_id=project_manager_id,
        ordering=ordering,
    )

    result = paginate_queryset(
        queryset,
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_project,
    )


@router.post(
    "",
    response={
        201: ProjectSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("projects.add_project")
def create_project(request, payload: ProjectCreateSchema):
    project = ProjectService.create_project(
        request=request,
        values=project_values(payload),
    )

    return 201, serialize_project(project)


@router.get(
    "/{project_id}",
    response={
        200: ProjectSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("projects.view_project")
def get_project(request, project_id: str):
    project = ProjectRepository.find_by_id(project_id)

    if project is None:
        raise ApiHttpError(
            404,
            "Project not found.",
            code="project_not_found",
        )

    return serialize_project(project)


@router.put(
    "/{project_id}",
    response={
        200: ProjectSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("projects.change_project")
def update_project(
    request,
    project_id: str,
    payload: ProjectUpdateSchema,
):
    project = ProjectRepository.find_by_id(project_id)

    if project is None:
        raise ApiHttpError(
            404,
            "Project not found.",
            code="project_not_found",
        )

    project = ProjectService.update_project(
        request=request,
        project=project,
        values=project_values(
            payload,
            require_client=False,
        ),
    )

    return serialize_project(project)


@router.delete(
    "/{project_id}",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("projects.delete_project")
def delete_project(request, project_id: str):
    project = ProjectRepository.find_by_id(project_id)

    if project is None:
        raise ApiHttpError(
            404,
            "Project not found.",
            code="project_not_found",
        )

    ProjectService.soft_delete(
        request=request,
        project=project,
    )

    return {
        "status": "ok",
        "message": "Project deleted successfully.",
    }


@router.post(
    "/{project_id}/team",
    response={
        201: ProjectTeamMemberSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("projects.add_projectteammember")
def assign_team_member(
    request,
    project_id: str,
    payload: ProjectTeamMemberCreateSchema,
):
    project = ProjectRepository.find_by_id(project_id)

    if project is None:
        raise ApiHttpError(
            404,
            "Project not found.",
            code="project_not_found",
        )

    assignment = ProjectService.assign_team_member(
        request=request,
        project=project,
        user=resolve_user(payload.user_id),
        role=payload.role,
        allocation_percentage=payload.allocation_percentage,
    )

    return 201, serialize_team_member(assignment)


@router.post(
    "/{project_id}/milestones",
    response={
        201: ProjectMilestoneSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("projects.add_projectmilestone")
def create_milestone(
    request,
    project_id: str,
    payload: ProjectMilestoneCreateSchema,
):
    project = ProjectRepository.find_by_id(project_id)

    if project is None:
        raise ApiHttpError(
            404,
            "Project not found.",
            code="project_not_found",
        )

    milestone = ProjectService.create_milestone(
        request=request,
        project=project,
        values=payload.dict(),
    )

    return 201, serialize_milestone(milestone)


@router.put(
    "/milestones/{milestone_id}",
    response={
        200: ProjectMilestoneSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("projects.change_projectmilestone")
def update_milestone(
    request,
    milestone_id: str,
    payload: ProjectMilestoneUpdateSchema,
):
    milestone = ProjectMilestone.objects.filter(
        pk=milestone_id,
    ).first()

    if milestone is None:
        raise ApiHttpError(
            404,
            "Milestone not found.",
            code="milestone_not_found",
        )

    milestone = ProjectService.update_milestone(
        request=request,
        milestone=milestone,
        values=payload.dict(),
    )

    return serialize_milestone(milestone)


@router.post(
    "/{project_id}/notes",
    response={
        201: ProjectNoteSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("projects.add_projectnote")
def add_note(
    request,
    project_id: str,
    payload: ProjectNoteCreateSchema,
):
    project = ProjectRepository.find_by_id(project_id)

    if project is None:
        raise ApiHttpError(
            404,
            "Project not found.",
            code="project_not_found",
        )

    note = ProjectService.add_note(
        request=request,
        project=project,
        content=payload.content,
        is_pinned=payload.is_pinned,
        is_client_visible=payload.is_client_visible,
    )

    return 201, serialize_note(note)


@router.post(
    "/convert-quotation/{quotation_id}",
    response={
        201: ProjectSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("projects.add_project")
def convert_quotation(request, quotation_id: str):
    quotation = Quotation.objects.filter(
        pk=quotation_id,
    ).first()

    if quotation is None:
        raise ApiHttpError(
            404,
            "Quotation not found.",
            code="quotation_not_found",
        )

    try:
        project = ProjectService.convert_quotation(
            request=request,
            quotation=quotation,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_project_conversion",
        ) from exc

    return 201, serialize_project(project)
