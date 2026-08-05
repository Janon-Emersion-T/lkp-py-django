from django.db.models import QuerySet
from django.utils import timezone

from apps.common.query import (
    apply_ordering,
    apply_search,
)
from apps.common.repositories import BaseRepository

from .models import Project, ProjectStatus


class ProjectRepository(BaseRepository[Project]):
    model = Project

    @classmethod
    def queryset(cls) -> QuerySet[Project]:
        return (
            Project.objects.select_related(
                "client",
                "quotation",
                "project_manager",
                "created_by",
                "updated_by",
            )
            .prefetch_related(
                "team_members__user",
                "milestones",
                "project_notes",
                "files",
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
        client_id: str | None = None,
        project_manager_id: int | None = None,
        ordering: str | None = None,
    ) -> QuerySet[Project]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "project_code",
                "title",
                "description",
                "client__company_name",
                "client__client_code",
            ),
        )

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        if client_id:
            queryset = queryset.filter(client_id=client_id)

        if project_manager_id:
            queryset = queryset.filter(
                project_manager_id=project_manager_id,
            )

        return apply_ordering(
            queryset,
            ordering=ordering,
            allowed_fields=(
                "project_code",
                "title",
                "status",
                "priority",
                "budget",
                "progress",
                "start_date",
                "deadline",
                "created_at",
                "updated_at",
            ),
            default="-created_at",
        )

    @classmethod
    def active(cls) -> QuerySet[Project]:
        return cls.queryset().exclude(
            status__in=(
                ProjectStatus.COMPLETED,
                ProjectStatus.CANCELLED,
            ),
        )

    @classmethod
    def overdue(cls) -> QuerySet[Project]:
        return cls.active().filter(
            deadline__lt=timezone.localdate(),
        )
