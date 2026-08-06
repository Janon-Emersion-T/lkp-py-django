from datetime import date
from decimal import Decimal
from typing import Literal
from uuid import UUID

from ninja import Schema
from pydantic import Field


TeamTypeValue = Literal[
    "executive",
    "management",
    "engineering",
    "design",
    "marketing",
    "sales",
    "finance",
    "operations",
    "support",
    "hr",
    "legal",
    "project",
    "custom",
]

EmploymentStatusValue = Literal[
    "active",
    "on_leave",
    "suspended",
    "resigned",
    "terminated",
    "contract_ended",
    "inactive",
]

EngagementTypeValue = Literal[
    "full_time",
    "part_time",
    "contract",
    "intern",
    "consultant",
    "volunteer",
]

WorkLocationTypeValue = Literal[
    "onsite",
    "remote",
    "hybrid",
]

ExpertiseLevelValue = Literal[
    "awareness",
    "working",
    "proficient",
    "expert",
    "lead",
]


class TeamCreateSchema(Schema):
    name: str
    slug: str
    team_type: TeamTypeValue = "custom"
    description: str = ""
    parent_id: UUID | None = None
    manager_id: UUID | None = None
    is_active: bool = True
    is_public: bool = False
    sort_order: int = 0
    metadata: dict = Field(default_factory=dict)


class TeamUpdateSchema(TeamCreateSchema):
    pass


class TeamMembershipInputSchema(Schema):
    team_id: UUID
    role_title: str = ""
    is_primary: bool = False
    is_active: bool = True
    joined_at: date | None = None
    left_at: date | None = None
    sort_order: int = 0


class TeamMemberServiceInputSchema(Schema):
    service_id: UUID
    expertise_level: ExpertiseLevelValue = "proficient"
    years_of_experience: Decimal | None = None
    is_primary: bool = False
    is_public: bool = True
    sort_order: int = 0


class TeamMemberCreateSchema(Schema):
    user_id: UUID | None = None
    employee_code: str
    first_name: str
    last_name: str = ""
    preferred_name: str = ""
    job_title: str
    professional_title: str = ""
    email: str = ""
    phone: str = ""
    public_email: str = ""
    public_phone: str = ""
    profile_image_id: UUID | None = None
    bio: str = ""
    short_bio: str = ""
    qualifications: str = ""
    years_of_experience: int | None = None
    engagement_type: EngagementTypeValue = "full_time"
    employment_status: EmploymentStatusValue = "active"
    work_location_type: WorkLocationTypeValue = "onsite"
    office_location: str = ""
    country: str = ""
    timezone_name: str = "Asia/Colombo"
    joined_at: date | None = None
    employment_ended_at: date | None = None
    reports_to_id: UUID | None = None
    linkedin_url: str = ""
    github_url: str = ""
    portfolio_url: str = ""
    website_url: str = ""
    is_leadership: bool = False
    is_public: bool = False
    is_featured: bool = False
    sort_order: int = 0
    metadata: dict = Field(default_factory=dict)
    memberships: list[
        TeamMembershipInputSchema
    ] = Field(default_factory=list)
    services: list[
        TeamMemberServiceInputSchema
    ] = Field(default_factory=list)


class TeamMemberUpdateSchema(TeamMemberCreateSchema):
    pass


class TeamMembershipSchema(Schema):
    id: UUID
    team_id: UUID
    team_name: str
    role_title: str
    is_primary: bool
    is_active: bool
    joined_at: date
    left_at: date | None
    sort_order: int


class TeamMemberServiceSchema(Schema):
    id: UUID
    service_id: UUID
    service_title: str
    expertise_level: str
    years_of_experience: Decimal | None
    is_primary: bool
    is_public: bool
    sort_order: int


class TeamMemberSchema(Schema):
    id: UUID
    user_id: UUID | None
    employee_code: str
    first_name: str
    last_name: str
    full_name: str
    preferred_name: str
    display_name: str
    job_title: str
    professional_title: str
    email: str
    phone: str
    public_email: str
    public_phone: str
    profile_image_id: UUID | None
    bio: str
    short_bio: str
    qualifications: str
    years_of_experience: int | None
    engagement_type: str
    employment_status: str
    work_location_type: str
    office_location: str
    country: str
    timezone_name: str
    joined_at: date | None
    employment_ended_at: date | None
    reports_to_id: UUID | None
    reports_to_name: str | None
    linkedin_url: str
    github_url: str
    portfolio_url: str
    website_url: str
    is_leadership: bool
    is_public: bool
    is_featured: bool
    is_current: bool
    sort_order: int
    metadata: dict
    memberships: list[TeamMembershipSchema]
    services: list[TeamMemberServiceSchema]


class TeamSchema(Schema):
    id: UUID
    name: str
    slug: str
    team_type: str
    description: str
    parent_id: UUID | None
    parent_name: str | None
    manager_id: UUID | None
    manager_name: str | None
    is_active: bool
    is_public: bool
    sort_order: int
    metadata: dict
    member_count: int


class PublicTeamMemberSchema(Schema):
    id: UUID
    display_name: str
    job_title: str
    professional_title: str
    public_email: str
    public_phone: str
    profile_image_id: UUID | None
    short_bio: str
    bio: str
    qualifications: str
    years_of_experience: int | None
    country: str
    linkedin_url: str
    github_url: str
    portfolio_url: str
    website_url: str
    is_leadership: bool
    is_featured: bool
    services: list[TeamMemberServiceSchema]


class PublicTeamSchema(Schema):
    id: UUID
    name: str
    slug: str
    team_type: str
    description: str
    members: list[PublicTeamMemberSchema]



class TeamMemberStatusUpdateSchema(Schema):
    employment_status: EmploymentStatusValue
    employment_ended_at: date | None = None


class TeamMemberReportingLineSchema(Schema):
    reports_to_id: UUID | None = None


class TeamManagerUpdateSchema(Schema):
    manager_id: UUID | None = None


class TeamManagementDashboardSchema(Schema):
    total_teams: int
    active_teams: int
    public_teams: int
    total_members: int
    active_members: int
    members_on_leave: int
    inactive_members: int
    public_members: int
    featured_members: int
    leadership_members: int
    members_without_primary_team: int
    members_without_manager: int
    members_by_status: dict
    members_by_engagement: dict
    members_by_location: dict
    members_by_country: dict
    team_sizes: dict
