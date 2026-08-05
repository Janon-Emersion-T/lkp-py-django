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


class ProjectTeamMemberCreateSchema(Schema):
    user_id: int
    role: str = Field(default="", max_length=150)
    allocation_percentage: int = Field(default=100, ge=1, le=100)


class ProjectTeamMemberSchema(Schema):
    id: UUID
    user: UserSummarySchema
    role: str
    allocation_percentage: int
    is_active: bool
    created_at: datetime


class ProjectMilestoneCreateSchema(Schema):
    title: str = Field(min_length=1, max_length=250)
    description: str = ""
    status: str = "pending"
    start_date: date | None = None
    due_date: date | None = None
    progress: int = Field(default=0, ge=0, le=100)
    sort_order: int = Field(default=0, ge=0)
    amount: Decimal = Field(default=Decimal("0.00"), ge=0)


class ProjectMilestoneUpdateSchema(ProjectMilestoneCreateSchema):
    pass


class ProjectMilestoneSchema(Schema):
    id: UUID
    title: str
    description: str
    status: str
    start_date: date | None
    due_date: date | None
    completed_at: datetime | None
    progress: int
    sort_order: int
    amount: Decimal
    created_at: datetime
    updated_at: datetime


class ProjectNoteCreateSchema(Schema):
    content: str = Field(min_length=1)
    is_pinned: bool = False
    is_client_visible: bool = False


class ProjectNoteSchema(Schema):
    id: UUID
    content: str
    is_pinned: bool
    is_client_visible: bool
    created_at: datetime


class ProjectEventSchema(Schema):
    id: UUID
    event_type: str
    description: str
    metadata: dict[str, Any]
    created_at: datetime


class ProjectCreateSchema(Schema):
    client_id: UUID
    project_manager_id: int | None = None
    title: str = Field(min_length=1, max_length=250)
    description: str = ""
    status: str = "planning"
    priority: str = "normal"
    budget: Decimal = Field(default=Decimal("0.00"), ge=0)
    currency: str = Field(default="LKR", min_length=3, max_length=3)
    start_date: date | None = None
    deadline: date | None = None
    progress: int = Field(default=0, ge=0, le=100)
    repository_url: str = ""
    staging_url: str = ""
    production_url: str = ""
    notes: str = ""
    tags: list[str] = Field(default_factory=list)


class ProjectUpdateSchema(ProjectCreateSchema):
    client_id: UUID | None = None


class ProjectSchema(Schema):
    id: UUID
    project_code: str
    client_id: UUID
    client_name: str
    quotation_id: UUID | None
    title: str
    description: str
    status: str
    priority: str
    budget: Decimal
    currency: str
    start_date: date | None
    deadline: date | None
    completed_at: datetime | None
    progress: int
    project_manager: UserSummarySchema | None
    repository_url: str
    staging_url: str
    production_url: str
    notes: str
    tags: list[str]
    team_members: list[ProjectTeamMemberSchema]
    milestones: list[ProjectMilestoneSchema]
    project_notes: list[ProjectNoteSchema]
    events: list[ProjectEventSchema]
    created_at: datetime
    updated_at: datetime
