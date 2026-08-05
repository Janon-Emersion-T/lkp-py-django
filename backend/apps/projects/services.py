from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event
from apps.quotations.models import (
    Quotation,
    QuotationStatus,
)

from .models import (
    MilestoneStatus,
    Project,
    ProjectEvent,
    ProjectMilestone,
    ProjectNote,
    ProjectStatus,
    ProjectTeamMember,
)


class ProjectService:
    @staticmethod
    def generate_project_code() -> str:
        year = timezone.localdate().year
        prefix = f"LKP-PR-{year}-"

        latest = (
            Project.all_objects.filter(
                project_code__startswith=prefix,
            )
            .order_by("-project_code")
            .values_list("project_code", flat=True)
            .first()
        )

        if latest:
            try:
                sequence = int(
                    latest.rsplit("-", 1)[1]
                ) + 1
            except ValueError:
                sequence = (
                    Project.all_objects.filter(
                        project_code__startswith=prefix,
                    ).count()
                    + 1
                )
        else:
            sequence = 1

        return f"{prefix}{sequence:05d}"

    @staticmethod
    def create_event(
        *,
        project: Project,
        event_type: str,
        description: str,
        actor=None,
        metadata: dict[str, Any] | None = None,
    ) -> ProjectEvent:
        return ProjectEvent.objects.create(
            project=project,
            event_type=event_type,
            description=description,
            metadata=metadata or {},
            created_by=actor,
            updated_by=actor,
        )

    @staticmethod
    @transaction.atomic
    def create_project(
        *,
        request,
        values: dict[str, Any],
    ) -> Project:
        values.setdefault(
            "project_code",
            ProjectService.generate_project_code(),
        )

        project = Project.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        ProjectService.create_event(
            project=project,
            event_type="created",
            description="Project created.",
            actor=request.auth,
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="project_created",
            module="projects",
            description="Project created.",
            entity_type="projects.Project",
            entity_id=str(project.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="projects",
            message="Project created.",
            target_type="projects.Project",
            target_id=str(project.pk),
            after={
                "project_code": project.project_code,
                "client_id": str(project.client_id),
                "quotation_id": (
                    str(project.quotation_id)
                    if project.quotation_id
                    else None
                ),
                "title": project.title,
                "status": project.status,
                "budget": str(project.budget),
                "currency": project.currency,
            },
        )

        return project

    @staticmethod
    @transaction.atomic
    def update_project(
        *,
        request,
        project: Project,
        values: dict[str, Any],
    ) -> Project:
        before = {
            "title": project.title,
            "status": project.status,
            "priority": project.priority,
            "budget": str(project.budget),
            "progress": project.progress,
            "deadline": (
                project.deadline.isoformat()
                if project.deadline
                else None
            ),
            "project_manager_id": (
                project.project_manager_id
            ),
        }

        previous_status = project.status
        previous_progress = project.progress
        previous_manager = project.project_manager_id

        for field, value in values.items():
            setattr(project, field, value)

        project.progress = min(
            max(project.progress, 0),
            100,
        )

        if project.status == ProjectStatus.COMPLETED:
            project.progress = 100

            if project.completed_at is None:
                project.completed_at = timezone.now()
        elif previous_status == ProjectStatus.COMPLETED:
            project.completed_at = None

        project.updated_by = request.auth
        project.save()

        if previous_status != project.status:
            ProjectService.create_event(
                project=project,
                event_type="status_changed",
                description=(
                    f"Project status changed from "
                    f"{previous_status} to {project.status}."
                ),
                actor=request.auth,
                metadata={
                    "before": previous_status,
                    "after": project.status,
                },
            )

        if previous_progress != project.progress:
            ProjectService.create_event(
                project=project,
                event_type="progress_changed",
                description=(
                    f"Project progress changed from "
                    f"{previous_progress}% to "
                    f"{project.progress}%."
                ),
                actor=request.auth,
                metadata={
                    "before": previous_progress,
                    "after": project.progress,
                },
            )

        if previous_manager != project.project_manager_id:
            ProjectService.create_event(
                project=project,
                event_type="manager_changed",
                description="Project manager changed.",
                actor=request.auth,
                metadata={
                    "before": previous_manager,
                    "after": project.project_manager_id,
                },
            )

        log_activity(
            request=request,
            actor=request.auth,
            action="project_updated",
            module="projects",
            description="Project updated.",
            entity_type="projects.Project",
            entity_id=str(project.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="projects",
            message="Project updated.",
            target_type="projects.Project",
            target_id=str(project.pk),
            before=before,
            after={
                "title": project.title,
                "status": project.status,
                "priority": project.priority,
                "budget": str(project.budget),
                "progress": project.progress,
                "deadline": (
                    project.deadline.isoformat()
                    if project.deadline
                    else None
                ),
                "project_manager_id": (
                    project.project_manager_id
                ),
            },
        )

        return project

    @staticmethod
    @transaction.atomic
    def assign_team_member(
        *,
        request,
        project: Project,
        user,
        role: str = "",
        allocation_percentage: int = 100,
    ) -> ProjectTeamMember:
        assignment = ProjectTeamMember.all_objects.filter(
            project=project,
            user=user,
        ).first()

        if assignment is None:
            assignment = ProjectTeamMember.objects.create(
                project=project,
                user=user,
                role=role,
                allocation_percentage=allocation_percentage,
                is_active=True,
                created_by=request.auth,
                updated_by=request.auth,
            )
        else:
            assignment.role = role
            assignment.allocation_percentage = min(
                max(allocation_percentage, 1),
                100,
            )
            assignment.is_active = True
            assignment.is_deleted = False
            assignment.deleted_at = None
            assignment.updated_by = request.auth
            assignment.save()

        ProjectService.create_event(
            project=project,
            event_type="team_member_assigned",
            description="Team member assigned.",
            actor=request.auth,
            metadata={
                "user_id": user.pk,
                "role": assignment.role,
                "allocation_percentage": (
                    assignment.allocation_percentage
                ),
            },
        )

        return assignment

    @staticmethod
    @transaction.atomic
    def create_milestone(
        *,
        request,
        project: Project,
        values: dict[str, Any],
    ) -> ProjectMilestone:
        milestone = ProjectMilestone.objects.create(
            project=project,
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        ProjectService.create_event(
            project=project,
            event_type="milestone_created",
            description="Project milestone created.",
            actor=request.auth,
            metadata={
                "milestone_id": str(milestone.pk),
                "title": milestone.title,
            },
        )

        return milestone

    @staticmethod
    @transaction.atomic
    def update_milestone(
        *,
        request,
        milestone: ProjectMilestone,
        values: dict[str, Any],
    ) -> ProjectMilestone:
        previous_status = milestone.status

        for field, value in values.items():
            setattr(milestone, field, value)

        milestone.progress = min(
            max(milestone.progress, 0),
            100,
        )

        if milestone.status == MilestoneStatus.COMPLETED:
            milestone.progress = 100

            if milestone.completed_at is None:
                milestone.completed_at = timezone.now()
        elif previous_status == MilestoneStatus.COMPLETED:
            milestone.completed_at = None

        milestone.updated_by = request.auth
        milestone.save()

        ProjectService.create_event(
            project=milestone.project,
            event_type="milestone_updated",
            description="Project milestone updated.",
            actor=request.auth,
            metadata={
                "milestone_id": str(milestone.pk),
                "status": milestone.status,
                "progress": milestone.progress,
            },
        )

        return milestone

    @staticmethod
    @transaction.atomic
    def add_note(
        *,
        request,
        project: Project,
        content: str,
        is_pinned: bool = False,
        is_client_visible: bool = False,
    ) -> ProjectNote:
        note = ProjectNote.objects.create(
            project=project,
            content=content,
            is_pinned=is_pinned,
            is_client_visible=is_client_visible,
            created_by=request.auth,
            updated_by=request.auth,
        )

        ProjectService.create_event(
            project=project,
            event_type="note_added",
            description="Project note added.",
            actor=request.auth,
            metadata={
                "note_id": str(note.pk),
            },
        )

        return note

    @staticmethod
    @transaction.atomic
    def convert_quotation(
        *,
        request,
        quotation: Quotation,
    ) -> Project:
        if quotation.status != QuotationStatus.ACCEPTED:
            raise ValueError(
                "Only accepted quotations can be converted."
            )

        if hasattr(quotation, "project"):
            return quotation.project

        project = ProjectService.create_project(
            request=request,
            values={
                "client": quotation.client,
                "quotation": quotation,
                "title": quotation.title,
                "description": quotation.description,
                "budget": quotation.total_amount,
                "currency": quotation.currency,
                "status": ProjectStatus.PLANNING,
                "notes": quotation.notes,
            },
        )

        for index, item in enumerate(
            quotation.items.all()
        ):
            ProjectService.create_milestone(
                request=request,
                project=project,
                values={
                    "title": item.title,
                    "description": item.description,
                    "status": MilestoneStatus.PENDING,
                    "progress": 0,
                    "sort_order": index,
                    "amount": item.total_amount,
                },
            )

        ProjectService.create_event(
            project=project,
            event_type="quotation_converted",
            description=(
                "Accepted quotation converted to project."
            ),
            actor=request.auth,
            metadata={
                "quotation_id": str(quotation.pk),
                "quotation_number": (
                    quotation.quotation_number
                ),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="quotation_converted_to_project",
            module="projects",
            description=(
                "Accepted quotation converted to project."
            ),
            entity_type="projects.Project",
            entity_id=str(project.pk),
            metadata={
                "quotation_id": str(quotation.pk),
            },
        )

        return project

    @staticmethod
    @transaction.atomic
    def soft_delete(
        *,
        request,
        project: Project,
    ) -> None:
        project_id = str(project.pk)
        project.delete()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="projects",
            message="Project soft deleted.",
            target_type="projects.Project",
            target_id=project_id,
            after={
                "is_deleted": True,
            },
        )
