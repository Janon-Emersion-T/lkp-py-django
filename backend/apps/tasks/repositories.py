from django.db.models import QuerySet
from django.utils import timezone

from apps.common.query import (
    apply_ordering,
    apply_search,
)
from apps.common.repositories import BaseRepository

from .models import Task, TaskStatus


class TaskRepository(BaseRepository[Task]):
    model = Task

    @classmethod
    def queryset(cls) -> QuerySet[Task]:
        return (
            Task.objects.select_related(
                "project",
                "milestone",
                "parent",
                "assignee",
                "created_by",
                "updated_by",
            )
            .prefetch_related(
                "additional_assignees__user",
                "watchers__user",
                "checklist_items",
                "comments",
                "attachments",
                "dependencies__related_task",
                "time_logs",
                "events",
            )
        )

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        status: str | None = None,
        priority: str | None = None,
        project_id: str | None = None,
        milestone_id: str | None = None,
        assignee_id: int | None = None,
        ordering: str | None = None,
    ) -> QuerySet[Task]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "title",
                "description",
                "project__title",
                "project__project_code",
            ),
        )

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        if project_id:
            queryset = queryset.filter(project_id=project_id)

        if milestone_id:
            queryset = queryset.filter(
                milestone_id=milestone_id,
            )

        if assignee_id:
            queryset = queryset.filter(
                assignee_id=assignee_id,
            )

        return apply_ordering(
            queryset,
            ordering=ordering,
            allowed_fields=(
                "title",
                "status",
                "priority",
                "start_date",
                "due_date",
                "progress",
                "sort_order",
                "created_at",
                "updated_at",
            ),
            default="sort_order",
        )

    @classmethod
    def overdue(cls) -> QuerySet[Task]:
        return cls.queryset().filter(
            due_date__lt=timezone.localdate(),
        ).exclude(
            status__in=(
                TaskStatus.COMPLETED,
                TaskStatus.CANCELLED,
            ),
        )
