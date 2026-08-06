from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from ninja import Schema
from pydantic import Field


class JobDepartmentSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str
    is_active: bool
    sort_order: int


class EmploymentTypeSchema(Schema):
    id: UUID
    name: str
    code: str
    description: str
    is_active: bool
    sort_order: int


class JobPositionSchema(Schema):
    id: UUID
    department_id: UUID
    department_name: str
    employment_type_id: UUID
    employment_type_name: str
    title: str
    slug: str
    summary: str
    description: dict
    responsibilities: list
    requirements: list
    preferred_qualifications: list
    benefits: list
    location: str
    remote_policy: str
    experience_level: str
    salary_min: Decimal | None
    salary_max: Decimal | None
    salary_currency: str
    salary_visible: bool
    is_active: bool
    sort_order: int


class JobListingSchema(Schema):
    id: UUID
    position_id: UUID
    position_title: str
    department_name: str
    employment_type_name: str
    reference_code: str
    status: str
    number_of_openings: int
    application_deadline: datetime | None
    published_at: datetime | None
    scheduled_for: datetime | None
    is_featured: bool
    is_active: bool
    is_publicly_available: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime



ApplicationStatusValue = Literal[
    "new",
    "screening",
    "shortlisted",
    "interview",
    "assessment",
    "offered",
    "hired",
    "rejected",
    "withdrawn",
    "archived",
]

ApplicationSourceValue = Literal[
    "careers_page",
    "linkedin",
    "facebook",
    "referral",
    "email",
    "manual",
    "other",
]

QuestionTypeValue = Literal[
    "short_text",
    "long_text",
    "number",
    "boolean",
    "single_choice",
    "multiple_choice",
    "date",
]


class ApplicationQuestionCreateSchema(Schema):
    question: str
    question_type: QuestionTypeValue = "short_text"
    help_text: str = ""
    options: list = Field(default_factory=list)
    is_required: bool = False
    is_active: bool = True
    sort_order: int = 0


class ApplicationQuestionSchema(Schema):
    id: UUID
    listing_id: UUID
    question: str
    question_type: str
    help_text: str
    options: list
    is_required: bool
    is_active: bool
    sort_order: int


class ApplicationAnswerInputSchema(Schema):
    question_id: UUID
    answer: object


class JobApplicationCreateSchema(Schema):
    listing_id: UUID
    applicant_name: str
    email: str
    phone: str = ""
    country: str = ""
    city: str = ""
    linkedin_url: str = ""
    portfolio_url: str = ""
    current_company: str = ""
    current_position: str = ""
    years_of_experience: Decimal | None = None
    expected_salary: Decimal | None = None
    expected_salary_currency: str = "LKR"
    availability_date: str | None = None
    cover_letter: str = ""
    resume_asset_id: UUID | None = None
    source: ApplicationSourceValue = "manual"
    assigned_to_id: UUID | None = None
    consent_to_process: bool = False
    consent_to_retain: bool = False
    answers: list[ApplicationAnswerInputSchema] = Field(default_factory=list)


class JobApplicationStatusSchema(Schema):
    status: ApplicationStatusValue
    rejection_reason: str = ""


class ApplicationNoteCreateSchema(Schema):
    note: str
    is_private: bool = True


class ApplicationAnswerSchema(Schema):
    id: UUID
    question_id: UUID
    question: str
    answer: object


class ApplicationNoteSchema(Schema):
    id: UUID
    author_id: UUID | None
    author_name: str | None
    note: str
    is_private: bool
    created_at: datetime


class JobApplicationSchema(Schema):
    id: UUID
    listing_id: UUID
    listing_reference_code: str
    position_title: str
    applicant_name: str
    email: str
    phone: str
    country: str
    city: str
    linkedin_url: str
    portfolio_url: str
    current_company: str
    current_position: str
    years_of_experience: Decimal | None
    expected_salary: Decimal | None
    expected_salary_currency: str
    availability_date: str | None
    cover_letter: str
    resume_asset_id: UUID | None
    status: str
    source: str
    assigned_to_id: UUID | None
    assigned_to_name: str | None
    submitted_at: datetime
    reviewed_at: datetime | None
    rating: int | None
    internal_summary: str
    rejection_reason: str
    consent_to_process: bool
    consent_to_retain: bool
    answers: list[ApplicationAnswerSchema]
    notes: list[ApplicationNoteSchema]
    created_at: datetime
    updated_at: datetime



InterviewStatusValue = Literal[
    "scheduled",
    "confirmed",
    "completed",
    "cancelled",
    "no_show",
    "rescheduled",
]

InterviewTypeValue = Literal[
    "phone",
    "video",
    "onsite",
    "technical",
    "hr",
    "final",
]

EvaluationRecommendationValue = Literal[
    "strong_hire",
    "hire",
    "hold",
    "no_hire",
    "strong_no_hire",
]


class InterviewParticipantInputSchema(Schema):
    user_id: UUID
    is_lead: bool = False


class InterviewCreateSchema(Schema):
    application_id: UUID
    title: str = "Job Interview"
    interview_type: InterviewTypeValue = "video"
    scheduled_start: datetime
    scheduled_end: datetime
    timezone_name: str = "Asia/Colombo"
    location: str = ""
    meeting_url: str = ""
    instructions: str = ""
    organizer_id: UUID | None = None
    participants: list[
        InterviewParticipantInputSchema
    ] = Field(default_factory=list)


class InterviewStatusSchema(Schema):
    status: InterviewStatusValue
    cancellation_reason: str = ""


class InterviewParticipantSchema(Schema):
    id: UUID
    user_id: UUID
    user_name: str
    is_lead: bool
    attendance_confirmed: bool


class InterviewSchema(Schema):
    id: UUID
    application_id: UUID
    applicant_name: str
    position_title: str
    title: str
    interview_type: str
    status: str
    scheduled_start: datetime
    scheduled_end: datetime
    timezone_name: str
    location: str
    meeting_url: str
    instructions: str
    organizer_id: UUID | None
    organizer_name: str | None
    completed_at: datetime | None
    cancellation_reason: str
    participants: list[
        InterviewParticipantSchema
    ]
    created_at: datetime
    updated_at: datetime


class ApplicationEvaluationCreateSchema(Schema):
    application_id: UUID
    interview_id: UUID | None = None
    evaluator_id: UUID | None = None
    technical_score: int | None = None
    communication_score: int | None = None
    culture_score: int | None = None
    overall_score: int
    recommendation: EvaluationRecommendationValue
    strengths: str = ""
    concerns: str = ""
    comments: str = ""


class ApplicationEvaluationSchema(Schema):
    id: UUID
    application_id: UUID
    applicant_name: str
    interview_id: UUID | None
    evaluator_id: UUID
    evaluator_name: str
    technical_score: int | None
    communication_score: int | None
    culture_score: int | None
    overall_score: int
    recommendation: str
    strengths: str
    concerns: str
    comments: str
    submitted_at: datetime
    created_at: datetime
    updated_at: datetime



class JobListingScheduleSchema(Schema):
    scheduled_for: datetime


class JobApplicationReviewSchema(Schema):
    assigned_to_id: UUID | None = None
    rating: int | None = None
    internal_summary: str = ""


class CareersDashboardSchema(Schema):
    open_listings: int
    featured_listings: int
    total_applications: int
    new_applications: int
    screening_applications: int
    shortlisted_applications: int
    interview_applications: int
    offered_applications: int
    hired_applications: int
    rejected_applications: int
    upcoming_interviews: int
    completed_interviews: int
    applications_by_status: dict
    applications_by_source: dict
