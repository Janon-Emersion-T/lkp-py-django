from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from ninja import Schema
from pydantic import Field


class UserSummarySchema(Schema):
    id: int
    email: str
    first_name: str
    last_name: str


class TaskCreateSchema(Schema):
    project_id: UUID | None = None
    milestone_id: UUID | None = None
    parent_id: UUID | None = None
    assignee_id: int | None = None

    title: str = Field(min_length=1, max_length=250)
    description: str = ""

    status: str = "todo"
    priority: str = "normal"

    start_date: date | None = None
    due_date: date | None = None

    estimated_hours: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
    )
    actual_hours: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
    )

    progress: int = Field(default=0, ge=0, le=100)
    sort_order: int = Field(default=0, ge=0)

    labels: list[str] = Field(default_factory=list)

    is_recurring: bool = False
    recurrence_rule: str = Field(
        default="",
        max_length=255,
    )


class TaskUpdateSchema(TaskCreateSchema):
    pass


class TaskAssigneeCreateSchema(Schema):
    user_id: int


class TaskAssigneeSchema(Schema):
    id: UUID
    user: UserSummarySchema
    created_at: datetime


class TaskWatcherCreateSchema(Schema):
    user_id: int


class TaskWatcherSchema(Schema):
    id: UUID
    user: UserSummarySchema
    created_at: datetime


class TaskChecklistCreateSchema(Schema):
    title: str = Field(min_length=1, max_length=250)
    sort_order: int = Field(default=0, ge=0)


class TaskChecklistToggleSchema(Schema):
    is_completed: bool


class TaskChecklistSchema(Schema):
    id: UUID
    title: str
    is_completed: bool
    completed_at: datetime | None
    completed_by: UserSummarySchema | None
    sort_order: int
    created_at: datetime


class TaskCommentCreateSchema(Schema):
    content: str = Field(min_length=1)
    is_internal: bool = True


class TaskCommentSchema(Schema):
    id: UUID
    content: str
    is_internal: bool
    author: UserSummarySchema | None
    created_at: datetime


class TaskDependencyCreateSchema(Schema):
    related_task_id: UUID
    dependency_type: str = "related"


class TaskDependencySchema(Schema):
    id: UUID
    related_task_id: UUID
    related_task_title: str
    dependency_type: str
    created_at: datetime


class TaskTimeLogCreateSchema(Schema):
    user_id: int | None = None
    work_date: date
    hours: Decimal = Field(gt=0)
    description: str = ""
    is_billable: bool = True


class TaskTimeLogSchema(Schema):
    id: UUID
    user: UserSummarySchema
    work_date: date
    hours: Decimal
    description: str
    is_billable: bool
    created_at: datetime


class TaskEventSchema(Schema):
    id: UUID
    event_type: str
    description: str
    metadata: dict[str, Any]
    created_at: datetime


class TaskSchema(Schema):
    id: UUID

    project_id: UUID | None
    project_title: str | None

    milestone_id: UUID | None
    milestone_title: str | None

    parent_id: UUID | None

    title: str
    description: str
    status: str
    priority: str

    assignee: UserSummarySchema | None

    start_date: date | None
    due_date: date | None
    completed_at: datetime | None

    estimated_hours: Decimal
    actual_hours: Decimal

    progress: int
    sort_order: int
    labels: list[str]

    is_recurring: bool
    recurrence_rule: str

    additional_assignees: list[TaskAssigneeSchema]
    watchers: list[TaskWatcherSchema]
    checklist_items: list[TaskChecklistSchema]
    comments: list[TaskCommentSchema]
    dependencies: list[TaskDependencySchema]
    time_logs: list[TaskTimeLogSchema]
    events: list[TaskEventSchema]

    created_at: datetime
    updated_at: datetime
