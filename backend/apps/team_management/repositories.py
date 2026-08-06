from django.db.models import Count, Q

from .models import (
    EmploymentStatus,
    Team,
    TeamMember,
    TeamMembership,
)


class TeamRepository:
    ALLOWED_ORDERING_FIELDS = {
        "name",
        "team_type",
        "sort_order",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return Team.objects.select_related(
            "parent",
            "manager",
        ).prefetch_related(
            "memberships",
            "memberships__member",
        )

    @classmethod
    def find_by_id(cls, team_id):
        return cls.queryset().filter(
            pk=team_id,
        ).first()

    @classmethod
    def find_by_slug(cls, slug):
        return cls.queryset().filter(
            slug=slug,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        team_type=None,
        parent_id=None,
        is_active=None,
        is_public=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(slug__icontains=search)
                | Q(description__icontains=search)
            )

        if team_type:
            queryset = queryset.filter(
                team_type=team_type,
            )

        if parent_id == "root":
            queryset = queryset.filter(
                parent__isnull=True,
            )
        elif parent_id:
            queryset = queryset.filter(
                parent_id=parent_id,
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        if is_public is not None:
            queryset = queryset.filter(
                is_public=is_public,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset


class TeamMemberRepository:
    ALLOWED_ORDERING_FIELDS = {
        "employee_code",
        "first_name",
        "last_name",
        "job_title",
        "joined_at",
        "employment_status",
        "sort_order",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return TeamMember.objects.select_related(
            "user",
            "profile_image",
            "reports_to",
        ).prefetch_related(
            "team_memberships",
            "team_memberships__team",
            "service_assignments",
            "service_assignments__service",
            "direct_reports",
        )

    @classmethod
    def find_by_id(cls, member_id):
        return cls.queryset().filter(
            pk=member_id,
        ).first()

    @classmethod
    def find_by_employee_code(cls, employee_code):
        return cls.queryset().filter(
            employee_code__iexact=employee_code,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        employment_status=None,
        engagement_type=None,
        work_location_type=None,
        country=None,
        team_id=None,
        service_id=None,
        reports_to_id=None,
        is_public=None,
        is_featured=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            search_terms = [
                term
                for term in search.strip().split()
                if term
            ]

            for term in search_terms:
                queryset = queryset.filter(
                    Q(employee_code__icontains=term)
                    | Q(first_name__icontains=term)
                    | Q(last_name__icontains=term)
                    | Q(preferred_name__icontains=term)
                    | Q(job_title__icontains=term)
                    | Q(professional_title__icontains=term)
                    | Q(email__icontains=term)
                )

        if employment_status:
            queryset = queryset.filter(
                employment_status=employment_status,
            )

        if engagement_type:
            queryset = queryset.filter(
                engagement_type=engagement_type,
            )

        if work_location_type:
            queryset = queryset.filter(
                work_location_type=work_location_type,
            )

        if country:
            queryset = queryset.filter(
                country__iexact=country,
            )

        if team_id:
            queryset = queryset.filter(
                team_memberships__team_id=team_id,
                team_memberships__is_active=True,
                team_memberships__is_deleted=False,
            )

        if service_id:
            queryset = queryset.filter(
                service_assignments__service_id=service_id,
                service_assignments__is_deleted=False,
            )

        if reports_to_id:
            queryset = queryset.filter(
                reports_to_id=reports_to_id,
            )

        if is_public is not None:
            queryset = queryset.filter(
                is_public=is_public,
            )

        if is_featured is not None:
            queryset = queryset.filter(
                is_featured=is_featured,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset.distinct()

    @classmethod
    def public_members(cls):
        return cls.queryset().filter(
            employment_status=EmploymentStatus.ACTIVE,
            is_public=True,
        )


class PublicTeamRepository:
    @staticmethod
    def teams():
        return Team.objects.filter(
            is_active=True,
            is_public=True,
        ).order_by(
            "sort_order",
            "name",
        )

    @staticmethod
    def members_for_team(team_id):
        return TeamMember.objects.select_related(
            "profile_image",
            "reports_to",
        ).prefetch_related(
            "service_assignments",
            "service_assignments__service",
        ).filter(
            team_memberships__team_id=team_id,
            team_memberships__is_active=True,
            team_memberships__is_deleted=False,
            employment_status=EmploymentStatus.ACTIVE,
            is_public=True,
        ).distinct().order_by(
            "team_memberships__sort_order",
            "sort_order",
            "first_name",
        )



class TeamManagementDashboardRepository:
    @staticmethod
    def statistics():
        team_queryset = Team.objects.all()
        member_queryset = TeamMember.objects.all()

        active_statuses = [
            EmploymentStatus.ACTIVE,
            EmploymentStatus.ON_LEAVE,
        ]

        members_by_status = {
            item["employment_status"]: item["total"]
            for item in (
                member_queryset.values(
                    "employment_status"
                ).annotate(
                    total=Count("id")
                )
            )
        }

        members_by_engagement = {
            item["engagement_type"]: item["total"]
            for item in (
                member_queryset.values(
                    "engagement_type"
                ).annotate(
                    total=Count("id")
                )
            )
        }

        members_by_location = {
            item["work_location_type"]: item["total"]
            for item in (
                member_queryset.values(
                    "work_location_type"
                ).annotate(
                    total=Count("id")
                )
            )
        }

        members_by_country = {
            item["country"] or "unspecified": item["total"]
            for item in (
                member_queryset.values(
                    "country"
                ).annotate(
                    total=Count("id")
                )
            )
        }

        team_sizes = {
            str(item["team_id"]): item["total"]
            for item in (
                TeamMembership.objects.filter(
                    is_active=True,
                    is_deleted=False,
                ).values(
                    "team_id"
                ).annotate(
                    total=Count("member_id")
                )
            )
        }

        return {
            "total_teams": team_queryset.count(),
            "active_teams": team_queryset.filter(
                is_active=True,
            ).count(),
            "public_teams": team_queryset.filter(
                is_active=True,
                is_public=True,
            ).count(),
            "total_members": member_queryset.count(),
            "active_members": member_queryset.filter(
                employment_status=(
                    EmploymentStatus.ACTIVE
                ),
            ).count(),
            "members_on_leave": (
                member_queryset.filter(
                    employment_status=(
                        EmploymentStatus.ON_LEAVE
                    ),
                ).count()
            ),
            "inactive_members": (
                member_queryset.exclude(
                    employment_status__in=active_statuses,
                ).count()
            ),
            "public_members": member_queryset.filter(
                employment_status=(
                    EmploymentStatus.ACTIVE
                ),
                is_public=True,
            ).count(),
            "featured_members": member_queryset.filter(
                employment_status=(
                    EmploymentStatus.ACTIVE
                ),
                is_public=True,
                is_featured=True,
            ).count(),
            "leadership_members": (
                member_queryset.filter(
                    employment_status__in=active_statuses,
                    is_leadership=True,
                ).count()
            ),
            "members_without_primary_team": (
                member_queryset.filter(
                    employment_status__in=active_statuses,
                ).exclude(
                    team_memberships__is_primary=True,
                    team_memberships__is_active=True,
                    team_memberships__is_deleted=False,
                ).count()
            ),
            "members_without_manager": (
                member_queryset.filter(
                    employment_status__in=active_statuses,
                    reports_to__isnull=True,
                    is_leadership=False,
                ).count()
            ),
            "members_by_status": members_by_status,
            "members_by_engagement": (
                members_by_engagement
            ),
            "members_by_location": (
                members_by_location
            ),
            "members_by_country": members_by_country,
            "team_sizes": team_sizes,
        }
