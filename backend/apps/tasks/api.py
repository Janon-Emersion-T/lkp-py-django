from django.contrib.auth import get_user_model
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema, MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.api.pagination_schemas import PaginatedResponseSchema
from apps.api.responses import paginated_response
from apps.common.pagination import paginate_queryset
from apps.projects.models import Project, ProjectMilestone
from apps.rbac.services import require_permissions

from .models import (
    Task,
    TaskChecklistItem,
)
from .repositories import TaskRepository
from .schemas import (
    TaskAssigneeCreateSchema,
    TaskAssigneeSchema,
    TaskChecklistCreateSchema,
    TaskChecklistSchema,
    TaskChecklistToggleSchema,
    TaskCommentCreateSchema,
    TaskCommentSchema,
    TaskCreateSchema,
    TaskDependencyCreateSchema,
    TaskDependencySchema,
    TaskSchema,
    TaskTimeLogCreateSchema,
    TaskTimeLogSchema,
    TaskUpdateSchema,
    TaskWatcherCreateSchema,
    TaskWatcherSchema,
)
from .services import TaskService


User = get_user_model()

router = Router(
    tags=["Tasks"],
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


def serialize_assignee(assignment):
    return {
        "id": assignment.id,
        "user": serialize_user(assignment.user),
        "created_at": assignment.created_at,
    }


def serialize_watcher(watcher):
    return {
        "id": watcher.id,
        "user": serialize_user(watcher.user),
        "created_at": watcher.created_at,
    }


def serialize_checklist_item(item):
    return {
        "id": item.id,
        "title": item.title,
        "is_completed": item.is_completed,
        "completed_at": item.completed_at,
        "completed_by": serialize_user(
            item.completed_by
        ),
        "sort_order": item.sort_order,
        "created_at": item.created_at,
    }


def serialize_comment(comment):
    return {
        "id": comment.id,
        "content": comment.content,
        "is_internal": comment.is_internal,
        "author": serialize_user(comment.created_by),
        "created_at": comment.created_at,
    }


def serialize_dependency(dependency):
    return {
        "id": dependency.id,
        "related_task_id": dependency.related_task_id,
        "related_task_title": dependency.related_task.title,
        "dependency_type": dependency.dependency_type,
        "created_at": dependency.created_at,
    }


def serialize_time_log(time_log):
    return {
        "id": time_log.id,
        "user": serialize_user(time_log.user),
        "work_date": time_log.work_date,
        "hours": time_log.hours,
        "description": time_log.description,
        "is_billable": time_log.is_billable,
        "created_at": time_log.created_at,
    }


def serialize_event(event):
    return {
        "id": event.id,
        "event_type": event.event_type,
        "description": event.description,
        "metadata": event.metadata,
        "created_at": event.created_at,
    }


def serialize_task(task):
    return {
        "id": task.id,
        "project_id": task.project_id,
        "project_title": (
            task.project.title
            if task.project
            else None
        ),
        "milestone_id": task.milestone_id,
        "milestone_title": (
            task.milestone.title
            if task.milestone
            else None
        ),
        "parent_id": task.parent_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "assignee": serialize_user(task.assignee),
        "start_date": task.start_date,
        "due_date": task.due_date,
        "completed_at": task.completed_at,
        "estimated_hours": task.estimated_hours,
        "actual_hours": task.actual_hours,
        "progress": task.progress,
        "sort_order": task.sort_order,
        "labels": task.labels,
        "is_recurring": task.is_recurring,
        "recurrence_rule": task.recurrence_rule,
        "additional_assignees": [
            serialize_assignee(assignment)
            for assignment
            in task.additional_assignees.all()
        ],
        "watchers": [
            serialize_watcher(watcher)
            for watcher in task.watchers.all()
        ],
        "checklist_items": [
            serialize_checklist_item(item)
            for item in task.checklist_items.all()
        ],
        "comments": [
            serialize_comment(comment)
            for comment in task.comments.all()
        ],
        "dependencies": [
            serialize_dependency(dependency)
            for dependency in task.dependencies.all()
        ],
        "time_logs": [
            serialize_time_log(time_log)
            for time_log in task.time_logs.all()
        ],
        "events": [
            serialize_event(event)
            for event in task.events.all()
        ],
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }


def resolve_user(user_id):
    if user_id is None:
        return None

    user = User.objects.filter(
        pk=user_id,
        is_deleted=False,
        is_active=True,
    ).first()

    if user is None:
        raise ApiHttpError(
            400,
            "User not found.",
            code="invalid_user",
        )

    return user


def resolve_project(project_id):
    if project_id is None:
        return None

    project = Project.objects.filter(
        pk=project_id,
    ).first()

    if project is None:
        raise ApiHttpError(
            400,
            "Project not found.",
            code="invalid_project",
        )

    return project


def resolve_milestone(milestone_id, project):
    if milestone_id is None:
        return None

    milestone = ProjectMilestone.objects.filter(
        pk=milestone_id,
    ).first()

    if milestone is None:
        raise ApiHttpError(
            400,
            "Milestone not found.",
            code="invalid_milestone",
        )

    if project and milestone.project_id != project.pk:
        raise ApiHttpError(
            400,
            "Milestone does not belong to the project.",
            code="invalid_milestone_project",
        )

    return milestone


def resolve_parent(parent_id):
    if parent_id is None:
        return None

    parent = Task.objects.filter(pk=parent_id).first()

    if parent is None:
        raise ApiHttpError(
            400,
            "Parent task not found.",
            code="invalid_parent_task",
        )

    return parent


def task_values(payload):
    values = payload.dict()

    project_id = values.pop("project_id", None)
    milestone_id = values.pop("milestone_id", None)
    parent_id = values.pop("parent_id", None)
    assignee_id = values.pop("assignee_id", None)

    project = resolve_project(project_id)

    values["project"] = project
    values["milestone"] = resolve_milestone(
        milestone_id,
        project,
    )
    values["parent"] = resolve_parent(parent_id)
    values["assignee"] = resolve_user(assignee_id)

    return values


def get_task_or_404(task_id):
    task = TaskRepository.find_by_id(task_id)

    if task is None:
        raise ApiHttpError(
            404,
            "Task not found.",
            code="task_not_found",
        )

    return task


@router.get(
    "",
    response={
        200: PaginatedResponseSchema[TaskSchema],
        403: ErrorSchema,
    },
)
@require_permissions("tasks.view_task")
def list_tasks(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    project_id: str | None = None,
    milestone_id: str | None = None,
    assignee_id: int | None = None,
    ordering: str | None = None,
):
    queryset = TaskRepository.search(
        search=search,
        status=status,
        priority=priority,
        project_id=project_id,
        milestone_id=milestone_id,
        assignee_id=assignee_id,
        ordering=ordering,
    )

    result = paginate_queryset(
        queryset,
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_task,
    )


@router.post(
    "",
    response={
        201: TaskSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("tasks.add_task")
def create_task(request, payload: TaskCreateSchema):
    task = TaskService.create_task(
        request=request,
        values=task_values(payload),
    )

    return 201, serialize_task(task)


@router.get(
    "/{task_id}",
    response={
        200: TaskSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("tasks.view_task")
def get_task(request, task_id: str):
    return serialize_task(get_task_or_404(task_id))


@router.put(
    "/{task_id}",
    response={
        200: TaskSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("tasks.change_task")
def update_task(
    request,
    task_id: str,
    payload: TaskUpdateSchema,
):
    task = get_task_or_404(task_id)

    task = TaskService.update_task(
        request=request,
        task=task,
        values=task_values(payload),
    )

    return serialize_task(task)


@router.delete(
    "/{task_id}",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("tasks.delete_task")
def delete_task(request, task_id: str):
    task = get_task_or_404(task_id)

    TaskService.soft_delete(
        request=request,
        task=task,
    )

    return {
        "status": "ok",
        "message": "Task deleted successfully.",
    }


@router.post(
    "/{task_id}/assignees",
    response={
        201: TaskAssigneeSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("tasks.add_taskassignee")
def add_assignee(
    request,
    task_id: str,
    payload: TaskAssigneeCreateSchema,
):
    assignment = TaskService.assign_additional_user(
        request=request,
        task=get_task_or_404(task_id),
        user=resolve_user(payload.user_id),
    )

    return 201, serialize_assignee(assignment)


@router.post(
    "/{task_id}/watchers",
    response={
        201: TaskWatcherSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("tasks.add_taskwatcher")
def add_watcher(
    request,
    task_id: str,
    payload: TaskWatcherCreateSchema,
):
    watcher = TaskService.add_watcher(
        request=request,
        task=get_task_or_404(task_id),
        user=resolve_user(payload.user_id),
    )

    return 201, serialize_watcher(watcher)


@router.post(
    "/{task_id}/checklist",
    response={
        201: TaskChecklistSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("tasks.add_taskchecklistitem")
def add_checklist_item(
    request,
    task_id: str,
    payload: TaskChecklistCreateSchema,
):
    item = TaskService.add_checklist_item(
        request=request,
        task=get_task_or_404(task_id),
        title=payload.title,
        sort_order=payload.sort_order,
    )

    return 201, serialize_checklist_item(item)


@router.put(
    "/checklist/{item_id}",
    response={
        200: TaskChecklistSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("tasks.change_taskchecklistitem")
def toggle_checklist_item(
    request,
    item_id: str,
    payload: TaskChecklistToggleSchema,
):
    item = TaskChecklistItem.objects.filter(
        pk=item_id,
    ).first()

    if item is None:
        raise ApiHttpError(
            404,
            "Checklist item not found.",
            code="checklist_item_not_found",
        )

    item = TaskService.toggle_checklist_item(
        request=request,
        item=item,
        is_completed=payload.is_completed,
    )

    return serialize_checklist_item(item)


@router.post(
    "/{task_id}/comments",
    response={
        201: TaskCommentSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("tasks.add_taskcomment")
def add_comment(
    request,
    task_id: str,
    payload: TaskCommentCreateSchema,
):
    comment = TaskService.add_comment(
        request=request,
        task=get_task_or_404(task_id),
        content=payload.content,
        is_internal=payload.is_internal,
    )

    return 201, serialize_comment(comment)


@router.post(
    "/{task_id}/dependencies",
    response={
        201: TaskDependencySchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("tasks.add_taskdependency")
def add_dependency(
    request,
    task_id: str,
    payload: TaskDependencyCreateSchema,
):
    task = get_task_or_404(task_id)
    related_task = get_task_or_404(
        str(payload.related_task_id)
    )

    try:
        dependency = TaskService.add_dependency(
            request=request,
            task=task,
            related_task=related_task,
            dependency_type=payload.dependency_type,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_task_dependency",
        ) from exc

    return 201, serialize_dependency(dependency)


@router.post(
    "/{task_id}/time-logs",
    response={
        201: TaskTimeLogSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("tasks.add_tasktimelog")
def add_time_log(
    request,
    task_id: str,
    payload: TaskTimeLogCreateSchema,
):
    user = (
        resolve_user(payload.user_id)
        if payload.user_id
        else request.auth
    )

    try:
        time_log = TaskService.log_time(
            request=request,
            task=get_task_or_404(task_id),
            user=user,
            work_date=payload.work_date,
            hours=payload.hours,
            description=payload.description,
            is_billable=payload.is_billable,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_time_log",
        ) from exc

    return 201, serialize_time_log(time_log)
