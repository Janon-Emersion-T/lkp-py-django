from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from ninja import Router

from apps.accounts.models import User
from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.api.exceptions import ApiHttpError
from apps.media_library.models import MediaAsset
from apps.rbac.services import require_permissions
from apps.services_catalog.models import Service

from .models import Team, TeamMember
from .repositories import (
    PublicTeamRepository,
    TeamMemberRepository,
    TeamRepository,
)
from .schemas import (
    PublicTeamSchema,
    TeamCreateSchema,
    TeamMemberCreateSchema,
    TeamMemberSchema,
    TeamMemberUpdateSchema,
    TeamSchema,
    TeamUpdateSchema,
)
from .services import TeamManagementService


router = Router(
    tags=["Team Management"],
    auth=jwt_auth,
)


def get_team(team_id):
    team = TeamRepository.find_by_id(team_id)

    if team is None:
        raise ApiHttpError(
            404,
            "Team not found.",
            code="team_not_found",
        )

    return team


def get_member(member_id):
    member = TeamMemberRepository.find_by_id(
        member_id
    )

    if member is None:
        raise ApiHttpError(
            404,
            "Team member not found.",
            code="team_member_not_found",
        )

    return member


def resolve_optional(model, object_id, label):
    if object_id is None:
        return None

    instance = model.objects.filter(
        pk=object_id,
    ).first()

    if instance is None:
        raise ApiHttpError(
            400,
            f"{label} not found.",
            code=(
                "invalid_"
                + label.lower().replace(" ", "_")
            ),
        )

    return instance


def resolve_memberships(items):
    team_ids = [
        item.team_id
        for item in items
    ]

    if len(team_ids) != len(set(team_ids)):
        raise ApiHttpError(
            400,
            "A team was assigned more than once.",
            code="duplicate_team_membership",
        )

    teams = {
        team.id: team
        for team in Team.objects.filter(
            id__in=team_ids,
        )
    }

    if len(teams) != len(team_ids):
        raise ApiHttpError(
            400,
            "One or more teams are invalid.",
            code="invalid_team_memberships",
        )

    primary_count = sum(
        1
        for item in items
        if item.is_primary and item.is_active
    )

    if primary_count > 1:
        raise ApiHttpError(
            400,
            "Only one active primary team is allowed.",
            code="multiple_primary_teams",
        )

    return [
        {
            "team": teams[item.team_id],
            "role_title": item.role_title,
            "is_primary": item.is_primary,
            "is_active": item.is_active,
            "joined_at": (
                item.joined_at
                or timezone.localdate()
            ),
            "left_at": item.left_at,
            "sort_order": item.sort_order,
        }
        for item in items
    ]


def resolve_services(items):
    service_ids = [
        item.service_id
        for item in items
    ]

    if len(service_ids) != len(set(service_ids)):
        raise ApiHttpError(
            400,
            "A service was assigned more than once.",
            code="duplicate_team_member_service",
        )

    services = {
        service.id: service
        for service in Service.objects.filter(
            id__in=service_ids,
        )
    }

    if len(services) != len(service_ids):
        raise ApiHttpError(
            400,
            "One or more services are invalid.",
            code="invalid_team_member_services",
        )

    return [
        {
            "service": services[item.service_id],
            "expertise_level": item.expertise_level,
            "years_of_experience": (
                item.years_of_experience
            ),
            "is_primary": item.is_primary,
            "is_public": item.is_public,
            "sort_order": item.sort_order,
        }
        for item in items
    ]


def team_values(payload):
    values = payload.dict()

    parent_id = values.pop("parent_id")
    manager_id = values.pop("manager_id")

    values["slug"] = slugify(payload.slug)
    values["parent"] = (
        get_team(parent_id)
        if parent_id
        else None
    )
    values["manager"] = (
        get_member(manager_id)
        if manager_id
        else None
    )

    return values


def member_values(payload):
    values = payload.dict()

    memberships = resolve_memberships(
        payload.memberships
    )
    services = resolve_services(
        payload.services
    )

    values.pop("memberships")
    values.pop("services")

    user_id = values.pop("user_id")
    profile_image_id = values.pop(
        "profile_image_id"
    )
    reports_to_id = values.pop("reports_to_id")

    values["user"] = resolve_optional(
        User,
        user_id,
        "User",
    )
    values["profile_image"] = resolve_optional(
        MediaAsset,
        profile_image_id,
        "Profile image",
    )
    values["reports_to"] = (
        get_member(reports_to_id)
        if reports_to_id
        else None
    )

    return values, memberships, services


def serialize_membership(membership):
    return {
        "id": membership.id,
        "team_id": membership.team_id,
        "team_name": membership.team.name,
        "role_title": membership.role_title,
        "is_primary": membership.is_primary,
        "is_active": membership.is_active,
        "joined_at": membership.joined_at,
        "left_at": membership.left_at,
        "sort_order": membership.sort_order,
    }


def serialize_service(assignment):
    return {
        "id": assignment.id,
        "service_id": assignment.service_id,
        "service_title": assignment.service.title,
        "expertise_level": (
            assignment.expertise_level
        ),
        "years_of_experience": (
            assignment.years_of_experience
        ),
        "is_primary": assignment.is_primary,
        "is_public": assignment.is_public,
        "sort_order": assignment.sort_order,
    }


def serialize_member(member):
    return {
        "id": member.id,
        "user_id": member.user_id,
        "employee_code": member.employee_code,
        "first_name": member.first_name,
        "last_name": member.last_name,
        "full_name": member.full_name,
        "preferred_name": member.preferred_name,
        "display_name": member.display_name,
        "job_title": member.job_title,
        "professional_title": (
            member.professional_title
        ),
        "email": member.email,
        "phone": member.phone,
        "public_email": member.public_email,
        "public_phone": member.public_phone,
        "profile_image_id": (
            member.profile_image_id
        ),
        "bio": member.bio,
        "short_bio": member.short_bio,
        "qualifications": member.qualifications,
        "years_of_experience": (
            member.years_of_experience
        ),
        "engagement_type": member.engagement_type,
        "employment_status": (
            member.employment_status
        ),
        "work_location_type": (
            member.work_location_type
        ),
        "office_location": member.office_location,
        "country": member.country,
        "timezone_name": member.timezone_name,
        "joined_at": member.joined_at,
        "employment_ended_at": (
            member.employment_ended_at
        ),
        "reports_to_id": member.reports_to_id,
        "reports_to_name": (
            member.reports_to.display_name
            if member.reports_to
            else None
        ),
        "linkedin_url": member.linkedin_url,
        "github_url": member.github_url,
        "portfolio_url": member.portfolio_url,
        "website_url": member.website_url,
        "is_leadership": member.is_leadership,
        "is_public": member.is_public,
        "is_featured": member.is_featured,
        "is_current": member.is_current,
        "sort_order": member.sort_order,
        "metadata": member.metadata,
        "memberships": [
            serialize_membership(item)
            for item in member.team_memberships.all()
        ],
        "services": [
            serialize_service(item)
            for item in member.service_assignments.all()
        ],
    }


def serialize_team(team):
    return {
        "id": team.id,
        "name": team.name,
        "slug": team.slug,
        "team_type": team.team_type,
        "description": team.description,
        "parent_id": team.parent_id,
        "parent_name": (
            team.parent.name
            if team.parent
            else None
        ),
        "manager_id": team.manager_id,
        "manager_name": (
            team.manager.display_name
            if team.manager
            else None
        ),
        "is_active": team.is_active,
        "is_public": team.is_public,
        "sort_order": team.sort_order,
        "metadata": team.metadata,
        "member_count": team.memberships.filter(
            is_active=True,
            is_deleted=False,
        ).count(),
    }


def serialize_public_member(member):
    return {
        "id": member.id,
        "display_name": member.display_name,
        "job_title": member.job_title,
        "professional_title": (
            member.professional_title
        ),
        "public_email": member.public_email,
        "public_phone": member.public_phone,
        "profile_image_id": (
            member.profile_image_id
        ),
        "profile_image_url": (
            member.profile_image.file.url
            if (
                member.profile_image
                and member.profile_image.file
            )
            else ""
        ),
        "short_bio": member.short_bio,
        "bio": member.bio,
        "qualifications": member.qualifications,
        "years_of_experience": (
            member.years_of_experience
        ),
        "country": member.country,
        "linkedin_url": member.linkedin_url,
        "github_url": member.github_url,
        "portfolio_url": member.portfolio_url,
        "website_url": member.website_url,
        "is_leadership": member.is_leadership,
        "is_featured": member.is_featured,
        "services": [
            serialize_service(item)
            for item in member.service_assignments.all()
            if item.is_public
        ],
    }


@router.get(
    "/teams",
    response={
        200: list[TeamSchema],
        403: ErrorSchema,
    },
)
@require_permissions("team_management.view_team")
def list_teams(
    request,
    search: str | None = None,
    team_type: str | None = None,
    parent_id: str | None = None,
    is_active: bool | None = None,
    is_public: bool | None = None,
    ordering: str | None = None,
):
    return [
        serialize_team(team)
        for team in TeamRepository.search(
            search=search,
            team_type=team_type,
            parent_id=parent_id,
            is_active=is_active,
            is_public=is_public,
            ordering=ordering,
        )
    ]


@router.post(
    "/teams",
    response={
        201: TeamSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("team_management.add_team")
def create_team(
    request,
    payload: TeamCreateSchema,
):
    values = team_values(payload)

    if Team.all_objects.filter(
        slug=values["slug"],
    ).exists():
        raise ApiHttpError(
            400,
            "Team slug already exists.",
            code="duplicate_team_slug",
        )

    try:
        team = TeamManagementService.create_team(
            request=request,
            values=values,
        )
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Team validation failed.",
            code="invalid_team",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    return 201, serialize_team(
        get_team(team.id)
    )


@router.get(
    "/teams/{team_id}",
    response={
        200: TeamSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("team_management.view_team")
def team_detail(request, team_id: str):
    return serialize_team(get_team(team_id))


@router.put(
    "/teams/{team_id}",
    response={
        200: TeamSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("team_management.change_team")
def update_team(
    request,
    team_id: str,
    payload: TeamUpdateSchema,
):
    team = get_team(team_id)
    values = team_values(payload)

    if Team.all_objects.exclude(
        pk=team.pk
    ).filter(
        slug=values["slug"],
    ).exists():
        raise ApiHttpError(
            400,
            "Team slug already exists.",
            code="duplicate_team_slug",
        )

    try:
        team = TeamManagementService.update_team(
            request=request,
            team=team,
            values=values,
        )
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Team validation failed.",
            code="invalid_team",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    return serialize_team(get_team(team.id))


@router.get(
    "/members",
    response={
        200: list[TeamMemberSchema],
        403: ErrorSchema,
    },
)
@require_permissions(
    "team_management.view_teammember"
)
def list_members(
    request,
    search: str | None = None,
    employment_status: str | None = None,
    engagement_type: str | None = None,
    work_location_type: str | None = None,
    country: str | None = None,
    team_id: str | None = None,
    service_id: str | None = None,
    reports_to_id: str | None = None,
    is_public: bool | None = None,
    is_featured: bool | None = None,
    ordering: str | None = None,
):
    return [
        serialize_member(member)
        for member in TeamMemberRepository.search(
            search=search,
            employment_status=employment_status,
            engagement_type=engagement_type,
            work_location_type=work_location_type,
            country=country,
            team_id=team_id,
            service_id=service_id,
            reports_to_id=reports_to_id,
            is_public=is_public,
            is_featured=is_featured,
            ordering=ordering,
        )
    ]


@router.post(
    "/members",
    response={
        201: TeamMemberSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "team_management.add_teammember"
)
def create_member(
    request,
    payload: TeamMemberCreateSchema,
):
    if TeamMember.all_objects.filter(
        employee_code__iexact=(
            payload.employee_code
        ),
    ).exists():
        raise ApiHttpError(
            400,
            "Employee code already exists.",
            code="duplicate_employee_code",
        )

    values, memberships, services = (
        member_values(payload)
    )

    try:
        member = (
            TeamManagementService.create_member(
                request=request,
                values=values,
                memberships=memberships,
                services=services,
            )
        )
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Team member validation failed.",
            code="invalid_team_member",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    return 201, serialize_member(
        get_member(member.id)
    )


@router.get(
    "/members/{member_id}",
    response={
        200: TeamMemberSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "team_management.view_teammember"
)
def member_detail(request, member_id: str):
    return serialize_member(
        get_member(member_id)
    )


@router.put(
    "/members/{member_id}",
    response={
        200: TeamMemberSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "team_management.change_teammember"
)
def update_member(
    request,
    member_id: str,
    payload: TeamMemberUpdateSchema,
):
    member = get_member(member_id)

    if TeamMember.all_objects.exclude(
        pk=member.pk
    ).filter(
        employee_code__iexact=(
            payload.employee_code
        ),
    ).exists():
        raise ApiHttpError(
            400,
            "Employee code already exists.",
            code="duplicate_employee_code",
        )

    values, memberships, services = (
        member_values(payload)
    )

    try:
        member = (
            TeamManagementService.update_member(
                request=request,
                member=member,
                values=values,
                memberships=memberships,
                services=services,
            )
        )
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Team member validation failed.",
            code="invalid_team_member",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    return serialize_member(
        get_member(member.id)
    )


@router.get(
    "/public/teams",
    auth=None,
    response={
        200: list[PublicTeamSchema],
    },
)
def public_teams(request):
    output = []

    for team in PublicTeamRepository.teams():
        members = (
            PublicTeamRepository.members_for_team(
                team.id
            )
        )

        output.append(
            {
                "id": team.id,
                "name": team.name,
                "slug": team.slug,
                "team_type": team.team_type,
                "description": team.description,
                "members": [
                    serialize_public_member(member)
                    for member in members
                ],
            }
        )

    return output


@router.get(
    "/public/members",
    auth=None,
    response={
        200: list[PublicTeamSchema],
    },
)
def public_members_grouped(request):
    return public_teams(request)



from .repositories import (
    TeamManagementDashboardRepository,
)
from .schemas import (
    TeamManagementDashboardSchema,
    TeamManagerUpdateSchema,
    TeamMemberReportingLineSchema,
    TeamMemberStatusUpdateSchema,
)


@router.post(
    "/members/{member_id}/status",
    response={
        200: TeamMemberSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "team_management.change_teammember"
)
def update_member_status(
    request,
    member_id: str,
    payload: TeamMemberStatusUpdateSchema,
):
    try:
        member = (
            TeamManagementService
            .update_member_status(
                request=request,
                member=get_member(member_id),
                employment_status=(
                    payload.employment_status
                ),
                employment_ended_at=(
                    payload.employment_ended_at
                ),
            )
        )
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Team member status validation failed.",
            code="invalid_team_member_status",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    return serialize_member(
        get_member(member.id)
    )


@router.put(
    "/members/{member_id}/reporting-line",
    response={
        200: TeamMemberSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "team_management.change_teammember"
)
def update_member_reporting_line(
    request,
    member_id: str,
    payload: TeamMemberReportingLineSchema,
):
    reports_to = (
        get_member(payload.reports_to_id)
        if payload.reports_to_id
        else None
    )

    try:
        member = (
            TeamManagementService
            .update_reporting_line(
                request=request,
                member=get_member(member_id),
                reports_to=reports_to,
            )
        )
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "Reporting line validation failed.",
            code="invalid_reporting_line",
            details={
                "errors": exc.message_dict,
            },
        ) from exc

    return serialize_member(
        get_member(member.id)
    )


@router.put(
    "/teams/{team_id}/manager",
    response={
        200: TeamSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("team_management.change_team")
def update_team_manager(
    request,
    team_id: str,
    payload: TeamManagerUpdateSchema,
):
    manager = (
        get_member(payload.manager_id)
        if payload.manager_id
        else None
    )

    try:
        team = TeamManagementService.set_team_manager(
            request=request,
            team=get_team(team_id),
            manager=manager,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_team_manager",
        ) from exc

    return serialize_team(
        get_team(team.id)
    )


@router.get(
    "/dashboard",
    response={
        200: TeamManagementDashboardSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "team_management.view_teammember"
)
def team_management_dashboard(request):
    return (
        TeamManagementDashboardRepository.statistics()
    )
