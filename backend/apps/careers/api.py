from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.rbac.services import require_permissions

from .repositories import (
    EmploymentTypeRepository,
    JobDepartmentRepository,
    JobListingRepository,
    JobPositionRepository,
)
from .schemas import (
    EmploymentTypeSchema,
    JobDepartmentSchema,
    JobListingSchema,
    JobPositionSchema,
)


router = Router(
    tags=["Careers"],
    auth=jwt_auth,
)


def serialize_department(department):
    return {
        "id": department.id,
        "name": department.name,
        "slug": department.slug,
        "description": department.description,
        "is_active": department.is_active,
        "sort_order": department.sort_order,
    }


def serialize_employment_type(employment_type):
    return {
        "id": employment_type.id,
        "name": employment_type.name,
        "code": employment_type.code,
        "description": employment_type.description,
        "is_active": employment_type.is_active,
        "sort_order": employment_type.sort_order,
    }


def serialize_position(position):
    return {
        "id": position.id,
        "department_id": position.department_id,
        "department_name": position.department.name,
        "employment_type_id": (
            position.employment_type_id
        ),
        "employment_type_name": (
            position.employment_type.name
        ),
        "title": position.title,
        "slug": position.slug,
        "summary": position.summary,
        "description": position.description,
        "responsibilities": position.responsibilities,
        "requirements": position.requirements,
        "preferred_qualifications": (
            position.preferred_qualifications
        ),
        "benefits": position.benefits,
        "location": position.location,
        "remote_policy": position.remote_policy,
        "experience_level": position.experience_level,
        "salary_min": position.salary_min,
        "salary_max": position.salary_max,
        "salary_currency": position.salary_currency,
        "salary_visible": position.salary_visible,
        "is_active": position.is_active,
        "sort_order": position.sort_order,
    }


def serialize_listing(listing):
    return {
        "id": listing.id,
        "position_id": listing.position_id,
        "position_title": listing.position.title,
        "department_name": (
            listing.position.department.name
        ),
        "employment_type_name": (
            listing.position.employment_type.name
        ),
        "reference_code": listing.reference_code,
        "status": listing.status,
        "number_of_openings": (
            listing.number_of_openings
        ),
        "application_deadline": (
            listing.application_deadline
        ),
        "published_at": listing.published_at,
        "scheduled_for": listing.scheduled_for,
        "is_featured": listing.is_featured,
        "is_active": listing.is_active,
        "is_publicly_available": (
            listing.is_publicly_available
        ),
        "sort_order": listing.sort_order,
        "created_at": listing.created_at,
        "updated_at": listing.updated_at,
    }


@router.get(
    "/departments",
    response={
        200: list[JobDepartmentSchema],
        403: ErrorSchema,
    },
)
@require_permissions("careers.view_jobdepartment")
def list_departments(
    request,
    search: str | None = None,
    is_active: bool | None = None,
):
    return [
        serialize_department(item)
        for item in JobDepartmentRepository.search(
            search=search,
            is_active=is_active,
        )
    ]


@router.get(
    "/employment-types",
    response={
        200: list[EmploymentTypeSchema],
        403: ErrorSchema,
    },
)
@require_permissions("careers.view_employmenttype")
def list_employment_types(
    request,
    search: str | None = None,
    is_active: bool | None = None,
):
    return [
        serialize_employment_type(item)
        for item in EmploymentTypeRepository.search(
            search=search,
            is_active=is_active,
        )
    ]


@router.get(
    "/positions",
    response={
        200: list[JobPositionSchema],
        403: ErrorSchema,
    },
)
@require_permissions("careers.view_jobposition")
def list_positions(
    request,
    search: str | None = None,
    department_id: str | None = None,
    employment_type_id: str | None = None,
    experience_level: str | None = None,
    remote_policy: str | None = None,
    is_active: bool | None = None,
    ordering: str | None = None,
):
    return [
        serialize_position(item)
        for item in JobPositionRepository.search(
            search=search,
            department_id=department_id,
            employment_type_id=employment_type_id,
            experience_level=experience_level,
            remote_policy=remote_policy,
            is_active=is_active,
            ordering=ordering,
        )
    ]


@router.get(
    "/listings",
    response={
        200: list[JobListingSchema],
        403: ErrorSchema,
    },
)
@require_permissions("careers.view_joblisting")
def list_job_listings(
    request,
    search: str | None = None,
    status: str | None = None,
    department_id: str | None = None,
    employment_type_id: str | None = None,
    is_featured: bool | None = None,
    is_active: bool | None = None,
    ordering: str | None = None,
):
    return [
        serialize_listing(item)
        for item in JobListingRepository.search(
            search=search,
            status=status,
            department_id=department_id,
            employment_type_id=employment_type_id,
            is_featured=is_featured,
            is_active=is_active,
            ordering=ordering,
        )
    ]



from datetime import date

from apps.accounts.models import User
from apps.api.common_schemas import MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.media_library.models import MediaAsset

from .models import (
    ApplicationQuestion,
    JobApplication,
    JobListing,
)
from .repositories import (
    ApplicationQuestionRepository,
    JobApplicationRepository,
)
from .schemas import (
    ApplicationNoteCreateSchema,
    ApplicationNoteSchema,
    ApplicationQuestionCreateSchema,
    ApplicationQuestionSchema,
    JobApplicationCreateSchema,
    JobApplicationSchema,
    JobApplicationStatusSchema,
)
from .services import JobApplicationService


def get_listing(listing_id):
    listing = JobListingRepository.find_by_id(listing_id)

    if listing is None:
        raise ApiHttpError(
            404,
            "Job listing not found.",
            code="job_listing_not_found",
        )

    return listing


def get_application(application_id):
    application = JobApplicationRepository.find_by_id(
        application_id
    )

    if application is None:
        raise ApiHttpError(
            404,
            "Job application not found.",
            code="job_application_not_found",
        )

    return application


def resolve_resume_asset(asset_id):
    if asset_id is None:
        return None

    asset = MediaAsset.objects.filter(
        pk=asset_id,
    ).first()

    if asset is None:
        raise ApiHttpError(
            400,
            "Resume media asset not found.",
            code="invalid_resume_asset",
        )

    return asset


def resolve_assigned_user(user_id):
    if user_id is None:
        return None

    user = User.objects.filter(pk=user_id).first()

    if user is None:
        raise ApiHttpError(
            400,
            "Assigned user not found.",
            code="invalid_assigned_user",
        )

    return user


def resolve_application_answers(listing, answer_inputs):
    questions = {
        str(question.id): question
        for question in (
            ApplicationQuestionRepository.for_listing(
                listing.id,
                is_active=True,
            )
        )
    }

    answers = []
    answered_ids = set()

    for answer_input in answer_inputs:
        question_id = str(answer_input.question_id)
        question = questions.get(question_id)

        if question is None:
            raise ApiHttpError(
                400,
                "Application question is invalid.",
                code="invalid_application_question",
            )

        if question_id in answered_ids:
            raise ApiHttpError(
                400,
                "Application question was answered twice.",
                code="duplicate_application_answer",
            )

        answered_ids.add(question_id)

        answers.append(
            {
                "question": question,
                "answer": answer_input.answer,
            }
        )

    missing_required = [
        question.question
        for question in questions.values()
        if question.is_required
        and str(question.id) not in answered_ids
    ]

    if missing_required:
        raise ApiHttpError(
            400,
            "Required application questions are missing.",
            code="missing_required_answers",
            details={
                "questions": missing_required,
            },
        )

    return answers


def serialize_question(question):
    return {
        "id": question.id,
        "listing_id": question.listing_id,
        "question": question.question,
        "question_type": question.question_type,
        "help_text": question.help_text,
        "options": question.options,
        "is_required": question.is_required,
        "is_active": question.is_active,
        "sort_order": question.sort_order,
    }


def serialize_note(note):
    return {
        "id": note.id,
        "author_id": note.author_id,
        "author_name": (
            str(note.author)
            if note.author
            else None
        ),
        "note": note.note,
        "is_private": note.is_private,
        "created_at": note.created_at,
    }


def serialize_application(application):
    return {
        "id": application.id,
        "listing_id": application.listing_id,
        "listing_reference_code": (
            application.listing.reference_code
        ),
        "position_title": (
            application.listing.position.title
        ),
        "applicant_name": application.applicant_name,
        "email": application.email,
        "phone": application.phone,
        "country": application.country,
        "city": application.city,
        "linkedin_url": application.linkedin_url,
        "portfolio_url": application.portfolio_url,
        "current_company": application.current_company,
        "current_position": application.current_position,
        "years_of_experience": (
            application.years_of_experience
        ),
        "expected_salary": application.expected_salary,
        "expected_salary_currency": (
            application.expected_salary_currency
        ),
        "availability_date": (
            application.availability_date.isoformat()
            if application.availability_date
            else None
        ),
        "cover_letter": application.cover_letter,
        "resume_asset_id": application.resume_asset_id,
        "status": application.status,
        "source": application.source,
        "assigned_to_id": application.assigned_to_id,
        "assigned_to_name": (
            str(application.assigned_to)
            if application.assigned_to
            else None
        ),
        "submitted_at": application.submitted_at,
        "reviewed_at": application.reviewed_at,
        "rating": application.rating,
        "internal_summary": application.internal_summary,
        "rejection_reason": application.rejection_reason,
        "consent_to_process": (
            application.consent_to_process
        ),
        "consent_to_retain": (
            application.consent_to_retain
        ),
        "answers": [
            {
                "id": answer.id,
                "question_id": answer.question_id,
                "question": answer.question.question,
                "answer": answer.answer,
            }
            for answer in application.answers.all()
        ],
        "notes": [
            serialize_note(note)
            for note in application.notes.all()
        ],
        "created_at": application.created_at,
        "updated_at": application.updated_at,
    }


@router.get(
    "/listings/{listing_id}/questions",
    response={
        200: list[ApplicationQuestionSchema],
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.view_applicationquestion")
def list_application_questions(
    request,
    listing_id: str,
    is_active: bool | None = None,
):
    get_listing(listing_id)

    return [
        serialize_question(question)
        for question in (
            ApplicationQuestionRepository.for_listing(
                listing_id,
                is_active=is_active,
            )
        )
    ]


@router.post(
    "/listings/{listing_id}/questions",
    response={
        201: ApplicationQuestionSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.add_applicationquestion")
def create_application_question(
    request,
    listing_id: str,
    payload: ApplicationQuestionCreateSchema,
):
    listing = get_listing(listing_id)

    question = ApplicationQuestion.objects.create(
        listing=listing,
        **payload.dict(),
    )

    return 201, serialize_question(question)


@router.get(
    "/applications",
    response={
        200: list[JobApplicationSchema],
        403: ErrorSchema,
    },
)
@require_permissions("careers.view_jobapplication")
def list_applications(
    request,
    search: str | None = None,
    listing_id: str | None = None,
    status: str | None = None,
    source: str | None = None,
    assigned_to_id: str | None = None,
    ordering: str | None = None,
):
    return [
        serialize_application(application)
        for application in JobApplicationRepository.search(
            search=search,
            listing_id=listing_id,
            status=status,
            source=source,
            assigned_to_id=assigned_to_id,
            ordering=ordering,
        )
    ]


@router.post(
    "/applications",
    response={
        201: JobApplicationSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.add_jobapplication")
def create_application(
    request,
    payload: JobApplicationCreateSchema,
):
    listing = get_listing(payload.listing_id)

    if JobApplication.all_objects.filter(
        listing=listing,
        email__iexact=payload.email,
        is_deleted=False,
    ).exists():
        raise ApiHttpError(
            400,
            "An application already exists for this email.",
            code="duplicate_job_application",
        )

    raw = payload.dict()

    raw.pop("listing_id")
    raw.pop("answers")
    resume_asset_id = raw.pop("resume_asset_id")
    assigned_to_id = raw.pop("assigned_to_id")

    availability_date = raw.get("availability_date")

    if availability_date:
        try:
            raw["availability_date"] = (
                date.fromisoformat(availability_date)
            )
        except ValueError as exc:
            raise ApiHttpError(
                400,
                "Availability date must use YYYY-MM-DD.",
                code="invalid_availability_date",
            ) from exc

    raw["listing"] = listing
    raw["resume_asset"] = resolve_resume_asset(
        resume_asset_id
    )
    raw["assigned_to"] = resolve_assigned_user(
        assigned_to_id
    )

    answers = resolve_application_answers(
        listing,
        payload.answers,
    )

    application = (
        JobApplicationService.create_application(
            request=request,
            values=raw,
            answers=answers,
        )
    )

    return 201, serialize_application(
        get_application(application.id)
    )


@router.get(
    "/applications/{application_id}",
    response={
        200: JobApplicationSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.view_jobapplication")
def application_detail(request, application_id: str):
    return serialize_application(
        get_application(application_id)
    )


@router.post(
    "/applications/{application_id}/status",
    response={
        200: JobApplicationSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.change_jobapplication")
def update_application_status(
    request,
    application_id: str,
    payload: JobApplicationStatusSchema,
):
    application = JobApplicationService.update_status(
        request=request,
        application=get_application(application_id),
        status=payload.status,
        rejection_reason=payload.rejection_reason,
    )

    return serialize_application(
        get_application(application.id)
    )


@router.post(
    "/applications/{application_id}/notes",
    response={
        201: ApplicationNoteSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.add_applicationnote")
def add_application_note(
    request,
    application_id: str,
    payload: ApplicationNoteCreateSchema,
):
    note = JobApplicationService.add_note(
        request=request,
        application=get_application(application_id),
        note=payload.note,
        is_private=payload.is_private,
    )

    return 201, serialize_note(note)



from django.core.exceptions import ValidationError

from .models import (
    ApplicationEvaluation,
    Interview,
    InterviewParticipant,
)
from .repositories import (
    ApplicationEvaluationRepository,
    InterviewRepository,
)
from .schemas import (
    ApplicationEvaluationCreateSchema,
    ApplicationEvaluationSchema,
    InterviewCreateSchema,
    InterviewSchema,
    InterviewStatusSchema,
)
from .services import (
    ApplicationEvaluationService,
    InterviewService,
)


def get_interview(interview_id):
    interview = InterviewRepository.find_by_id(
        interview_id
    )

    if interview is None:
        raise ApiHttpError(
            404,
            "Interview not found.",
            code="interview_not_found",
        )

    return interview


def resolve_user(user_id, *, field_name):
    if user_id is None:
        return None

    user = User.objects.filter(pk=user_id).first()

    if user is None:
        raise ApiHttpError(
            400,
            f"{field_name} user not found.",
            code=f"invalid_{field_name}_user",
        )

    return user


def resolve_interview_participants(items):
    participants = []
    seen_user_ids = set()

    for item in items:
        user_id = str(item.user_id)

        if user_id in seen_user_ids:
            raise ApiHttpError(
                400,
                "An interviewer was added more than once.",
                code="duplicate_interview_participant",
            )

        seen_user_ids.add(user_id)

        participants.append(
            {
                "user": resolve_user(
                    item.user_id,
                    field_name="participant",
                ),
                "is_lead": item.is_lead,
            }
        )

    lead_count = sum(
        1
        for participant in participants
        if participant["is_lead"]
    )

    if lead_count > 1:
        raise ApiHttpError(
            400,
            "Only one lead interviewer is allowed.",
            code="multiple_lead_interviewers",
        )

    return participants


def serialize_interview(interview):
    return {
        "id": interview.id,
        "application_id": interview.application_id,
        "applicant_name": (
            interview.application.applicant_name
        ),
        "position_title": (
            interview.application.listing.position.title
        ),
        "title": interview.title,
        "interview_type": interview.interview_type,
        "status": interview.status,
        "scheduled_start": interview.scheduled_start,
        "scheduled_end": interview.scheduled_end,
        "timezone_name": interview.timezone_name,
        "location": interview.location,
        "meeting_url": interview.meeting_url,
        "instructions": interview.instructions,
        "organizer_id": interview.organizer_id,
        "organizer_name": (
            str(interview.organizer)
            if interview.organizer
            else None
        ),
        "completed_at": interview.completed_at,
        "cancellation_reason": (
            interview.cancellation_reason
        ),
        "participants": [
            {
                "id": participant.id,
                "user_id": participant.user_id,
                "user_name": str(participant.user),
                "is_lead": participant.is_lead,
                "attendance_confirmed": (
                    participant.attendance_confirmed
                ),
            }
            for participant in interview.participants.all()
        ],
        "created_at": interview.created_at,
        "updated_at": interview.updated_at,
    }


def serialize_evaluation(evaluation):
    return {
        "id": evaluation.id,
        "application_id": evaluation.application_id,
        "applicant_name": (
            evaluation.application.applicant_name
        ),
        "interview_id": evaluation.interview_id,
        "evaluator_id": evaluation.evaluator_id,
        "evaluator_name": str(evaluation.evaluator),
        "technical_score": evaluation.technical_score,
        "communication_score": (
            evaluation.communication_score
        ),
        "culture_score": evaluation.culture_score,
        "overall_score": evaluation.overall_score,
        "recommendation": evaluation.recommendation,
        "strengths": evaluation.strengths,
        "concerns": evaluation.concerns,
        "comments": evaluation.comments,
        "submitted_at": evaluation.submitted_at,
        "created_at": evaluation.created_at,
        "updated_at": evaluation.updated_at,
    }


@router.get(
    "/interviews",
    response={
        200: list[InterviewSchema],
        403: ErrorSchema,
    },
)
@require_permissions("careers.view_interview")
def list_interviews(
    request,
    application_id: str | None = None,
    status: str | None = None,
    interview_type: str | None = None,
    organizer_id: str | None = None,
    ordering: str | None = None,
):
    return [
        serialize_interview(interview)
        for interview in InterviewRepository.search(
            application_id=application_id,
            status=status,
            interview_type=interview_type,
            organizer_id=organizer_id,
            ordering=ordering,
        )
    ]


@router.post(
    "/interviews",
    response={
        201: InterviewSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.add_interview")
def create_interview(
    request,
    payload: InterviewCreateSchema,
):
    application = get_application(
        payload.application_id
    )

    organizer = resolve_user(
        payload.organizer_id,
        field_name="organizer",
    )

    participants = resolve_interview_participants(
        payload.participants
    )

    values = payload.dict()
    values.pop("application_id")
    values.pop("organizer_id")
    values.pop("participants")

    values["application"] = application
    values["organizer"] = organizer

    interview = Interview(
        **values,
    )

    try:
        interview.full_clean()
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Interview validation failed.",
            code="invalid_interview",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    interview = InterviewService.create_interview(
        request=request,
        values=values,
        participants=participants,
    )

    return 201, serialize_interview(
        get_interview(interview.id)
    )


@router.get(
    "/interviews/{interview_id}",
    response={
        200: InterviewSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.view_interview")
def interview_detail(request, interview_id: str):
    return serialize_interview(
        get_interview(interview_id)
    )


@router.post(
    "/interviews/{interview_id}/status",
    response={
        200: InterviewSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.change_interview")
def update_interview_status(
    request,
    interview_id: str,
    payload: InterviewStatusSchema,
):
    interview = InterviewService.update_status(
        request=request,
        interview=get_interview(interview_id),
        status=payload.status,
        cancellation_reason=(
            payload.cancellation_reason
        ),
    )

    return serialize_interview(
        get_interview(interview.id)
    )


@router.get(
    "/applications/{application_id}/evaluations",
    response={
        200: list[ApplicationEvaluationSchema],
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "careers.view_applicationevaluation"
)
def list_application_evaluations(
    request,
    application_id: str,
):
    get_application(application_id)

    return [
        serialize_evaluation(evaluation)
        for evaluation in (
            ApplicationEvaluationRepository
            .for_application(application_id)
        )
    ]


@router.post(
    "/evaluations",
    response={
        201: ApplicationEvaluationSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "careers.add_applicationevaluation"
)
def create_application_evaluation(
    request,
    payload: ApplicationEvaluationCreateSchema,
):
    application = get_application(
        payload.application_id
    )

    interview = None

    if payload.interview_id:
        interview = get_interview(
            payload.interview_id
        )

        if interview.application_id != application.id:
            raise ApiHttpError(
                400,
                "Interview belongs to another application.",
                code="evaluation_interview_mismatch",
            )

    evaluator = (
        resolve_user(
            payload.evaluator_id,
            field_name="evaluator",
        )
        if payload.evaluator_id
        else request.auth
    )

    raw = payload.dict()
    raw.pop("application_id")
    raw.pop("interview_id")
    raw.pop("evaluator_id")

    raw["application"] = application
    raw["interview"] = interview
    raw["evaluator"] = evaluator

    evaluation = ApplicationEvaluation(**raw)

    try:
        evaluation.full_clean()
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Evaluation validation failed.",
            code="invalid_application_evaluation",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    evaluation = (
        ApplicationEvaluationService
        .create_evaluation(
            request=request,
            values=raw,
        )
    )

    return 201, serialize_evaluation(evaluation)



from .repositories import CareersDashboardRepository
from .schemas import (
    CareersDashboardSchema,
    JobApplicationReviewSchema,
    JobListingScheduleSchema,
)
from .services import JobListingService


@router.post(
    "/listings/{listing_id}/publish",
    response={
        200: JobListingSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.change_joblisting")
def publish_job_listing(request, listing_id: str):
    listing = JobListingService.publish_listing(
        request=request,
        listing=get_listing(listing_id),
    )

    return serialize_listing(
        JobListingRepository.find_by_id(listing.id)
    )


@router.post(
    "/listings/{listing_id}/schedule",
    response={
        200: JobListingSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.change_joblisting")
def schedule_job_listing(
    request,
    listing_id: str,
    payload: JobListingScheduleSchema,
):
    try:
        listing = JobListingService.schedule_listing(
            request=request,
            listing=get_listing(listing_id),
            scheduled_for=payload.scheduled_for,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_listing_schedule",
        ) from exc

    return serialize_listing(
        JobListingRepository.find_by_id(listing.id)
    )


@router.post(
    "/listings/{listing_id}/close",
    response={
        200: JobListingSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.change_joblisting")
def close_job_listing(request, listing_id: str):
    listing = JobListingService.close_listing(
        request=request,
        listing=get_listing(listing_id),
    )

    return serialize_listing(
        JobListingRepository.find_by_id(listing.id)
    )


@router.post(
    "/listings/{listing_id}/archive",
    response={
        200: JobListingSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.change_joblisting")
def archive_job_listing(request, listing_id: str):
    listing = JobListingService.archive_listing(
        request=request,
        listing=get_listing(listing_id),
    )

    return serialize_listing(
        JobListingRepository.find_by_id(listing.id)
    )


@router.put(
    "/applications/{application_id}/review",
    response={
        200: JobApplicationSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.change_jobapplication")
def review_application(
    request,
    application_id: str,
    payload: JobApplicationReviewSchema,
):
    assigned_to = resolve_assigned_user(
        payload.assigned_to_id
    )

    try:
        application = (
            JobApplicationService.review_application(
                request=request,
                application=get_application(
                    application_id
                ),
                assigned_to=assigned_to,
                rating=payload.rating,
                internal_summary=(
                    payload.internal_summary
                ),
            )
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_application_review",
        ) from exc

    return serialize_application(
        get_application(application.id)
    )


@router.get(
    "/dashboard",
    response={
        200: CareersDashboardSchema,
        403: ErrorSchema,
    },
)
@require_permissions("careers.view_jobapplication")
def careers_dashboard(request):
    return CareersDashboardRepository.statistics()
