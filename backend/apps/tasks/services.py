from decimal import Decimal
from typing import Any

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    Task,
    TaskAssignee,
    TaskChecklistItem,
    TaskComment,
    TaskDependency,
    TaskEvent,
    TaskStatus,
    TaskTimeLog,
    TaskWatcher,
)


class TaskService:
    @staticmethod
    def create_event(
        *,
        task: Task,
        event_type: str,
        description: str,
        actor=None,
        metadata: dict[str, Any] | None = None,
    ) -> TaskEvent:
        return TaskEvent.objects.create(
            task=task,
            event_type=event_type,
            description=description,
            metadata=metadata or {},
            created_by=actor,
            updated_by=actor,
        )

    @staticmethod
    @transaction.atomic
    def create_task(
        *,
        request,
        values: dict[str, Any],
    ) -> Task:
        task = Task.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        TaskService.create_event(
            task=task,
            event_type="created",
            description="Task created.",
            actor=request.auth,
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="task_created",
            module="tasks",
            description="Task created.",
            entity_type="tasks.Task",
            entity_id=str(task.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="tasks",
            message="Task created.",
            target_type="tasks.Task",
            target_id=str(task.pk),
            after={
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
                "project_id": (
                    str(task.project_id)
                    if task.project_id
                    else None
                ),
                "assignee_id": task.assignee_id,
            },
        )

        return task

    @staticmethod
    @transaction.atomic
    def update_task(
        *,
        request,
        task: Task,
        values: dict[str, Any],
    ) -> Task:
        before = {
            "title": task.title,
            "status": task.status,
            "priority": task.priority,
            "progress": task.progress,
            "assignee_id": task.assignee_id,
            "due_date": (
                task.due_date.isoformat()
                if task.due_date
                else None
            ),
        }

        previous_status = task.status
        previous_assignee = task.assignee_id

        for field, value in values.items():
            setattr(task, field, value)

        task.progress = min(
            max(task.progress, 0),
            100,
        )

        if task.status == TaskStatus.COMPLETED:
            task.progress = 100

            if task.completed_at is None:
                task.completed_at = timezone.now()
        elif previous_status == TaskStatus.COMPLETED:
            task.completed_at = None

        task.updated_by = request.auth
        task.save()

        if previous_status != task.status:
            TaskService.create_event(
                task=task,
                event_type="status_changed",
                description=(
                    f"Task status changed from "
                    f"{previous_status} to {task.status}."
                ),
                actor=request.auth,
                metadata={
                    "before": previous_status,
                    "after": task.status,
                },
            )

        if previous_assignee != task.assignee_id:
            TaskService.create_event(
                task=task,
                event_type="assignee_changed",
                description="Task assignee changed.",
                actor=request.auth,
                metadata={
                    "before": previous_assignee,
                    "after": task.assignee_id,
                },
            )

        log_activity(
            request=request,
            actor=request.auth,
            action="task_updated",
            module="tasks",
            description="Task updated.",
            entity_type="tasks.Task",
            entity_id=str(task.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="tasks",
            message="Task updated.",
            target_type="tasks.Task",
            target_id=str(task.pk),
            before=before,
            after={
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
                "progress": task.progress,
                "assignee_id": task.assignee_id,
                "due_date": (
                    task.due_date.isoformat()
                    if task.due_date
                    else None
                ),
            },
        )

        return task

    @staticmethod
    @transaction.atomic
    def assign_additional_user(
        *,
        request,
        task: Task,
        user,
    ) -> TaskAssignee:
        assignment = TaskAssignee.all_objects.filter(
            task=task,
            user=user,
        ).first()

        if assignment is None:
            assignment = TaskAssignee.objects.create(
                task=task,
                user=user,
                created_by=request.auth,
                updated_by=request.auth,
            )
        else:
            assignment.is_deleted = False
            assignment.deleted_at = None
            assignment.updated_by = request.auth
            assignment.save()

        TaskService.create_event(
            task=task,
            event_type="additional_assignee_added",
            description="Additional assignee added.",
            actor=request.auth,
            metadata={"user_id": user.pk},
        )

        return assignment

    @staticmethod
    @transaction.atomic
    def add_watcher(
        *,
        request,
        task: Task,
        user,
    ) -> TaskWatcher:
        watcher = TaskWatcher.all_objects.filter(
            task=task,
            user=user,
        ).first()

        if watcher is None:
            watcher = TaskWatcher.objects.create(
                task=task,
                user=user,
                created_by=request.auth,
                updated_by=request.auth,
            )
        else:
            watcher.is_deleted = False
            watcher.deleted_at = None
            watcher.updated_by = request.auth
            watcher.save()

        return watcher

    @staticmethod
    @transaction.atomic
    def add_checklist_item(
        *,
        request,
        task: Task,
        title: str,
        sort_order: int = 0,
    ) -> TaskChecklistItem:
        item = TaskChecklistItem.objects.create(
            task=task,
            title=title,
            sort_order=sort_order,
            created_by=request.auth,
            updated_by=request.auth,
        )

        TaskService.create_event(
            task=task,
            event_type="checklist_item_added",
            description="Checklist item added.",
            actor=request.auth,
            metadata={"checklist_item_id": str(item.pk)},
        )

        return item

    @staticmethod
    @transaction.atomic
    def toggle_checklist_item(
        *,
        request,
        item: TaskChecklistItem,
        is_completed: bool,
    ) -> TaskChecklistItem:
        item.is_completed = is_completed
        item.completed_at = (
            timezone.now()
            if is_completed
            else None
        )
        item.completed_by = (
            request.auth
            if is_completed
            else None
        )
        item.updated_by = request.auth
        item.save()

        return item

    @staticmethod
    @transaction.atomic
    def add_comment(
        *,
        request,
        task: Task,
        content: str,
        is_internal: bool = True,
    ) -> TaskComment:
        comment = TaskComment.objects.create(
            task=task,
            content=content,
            is_internal=is_internal,
            created_by=request.auth,
            updated_by=request.auth,
        )

        TaskService.create_event(
            task=task,
            event_type="comment_added",
            description="Task comment added.",
            actor=request.auth,
            metadata={"comment_id": str(comment.pk)},
        )

        return comment

    @staticmethod
    @transaction.atomic
    def add_dependency(
        *,
        request,
        task: Task,
        related_task: Task,
        dependency_type: str,
    ) -> TaskDependency:
        if task.pk == related_task.pk:
            raise ValueError(
                "A task cannot depend on itself."
            )

        dependency, _ = TaskDependency.objects.get_or_create(
            task=task,
            related_task=related_task,
            dependency_type=dependency_type,
            defaults={
                "created_by": request.auth,
                "updated_by": request.auth,
            },
        )

        return dependency

    @staticmethod
    @transaction.atomic
    def log_time(
        *,
        request,
        task: Task,
        user,
        work_date,
        hours: Decimal,
        description: str = "",
        is_billable: bool = True,
    ) -> TaskTimeLog:
        if hours <= Decimal("0.00"):
            raise ValueError(
                "Time logged must be greater than zero."
            )

        time_log = TaskTimeLog.objects.create(
            task=task,
            user=user,
            work_date=work_date,
            hours=hours,
            description=description,
            is_billable=is_billable,
            created_by=request.auth,
            updated_by=request.auth,
        )

        total = (
            task.time_logs.aggregate(
                total=Sum("hours"),
            )["total"]
            or Decimal("0.00")
        )

        task.actual_hours = total
        task.updated_by = request.auth
        task.save(
            update_fields=[
                "actual_hours",
                "updated_by",
                "updated_at",
            ],
        )

        TaskService.create_event(
            task=task,
            event_type="time_logged",
            description="Time logged against task.",
            actor=request.auth,
            metadata={
                "hours": str(hours),
                "user_id": user.pk,
            },
        )

        return time_log

    @staticmethod
    @transaction.atomic
    def soft_delete(
        *,
        request,
        task: Task,
    ) -> None:
        task_id = str(task.pk)
        task.delete()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="tasks",
            message="Task soft deleted.",
            target_type="tasks.Task",
            target_id=task_id,
            after={"is_deleted": True},
        )
