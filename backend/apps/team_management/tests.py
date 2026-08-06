from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import User

from .models import (
    EmploymentStatus,
    EngagementType,
    Team,
    TeamMember,
    TeamMembership,
    TeamType,
)
from .repositories import (
    PublicTeamRepository,
    TeamMemberRepository,
    TeamRepository,
)
from .services import TeamManagementService


class RequestStub:
    def __init__(self, user):
        self.auth = user
        self.user = user
        self.META = {}
        self.headers = {}


class TeamManagementModelTests(TestCase):
    def test_team_string(self):
        team = Team.objects.create(
            name="Engineering",
            slug="engineering",
            team_type=TeamType.ENGINEERING,
        )

        self.assertEqual(
            str(team),
            "Engineering",
        )

    def test_team_rejects_self_parent(self):
        team = Team.objects.create(
            name="Operations",
            slug="operations",
        )

        team.parent = team

        with self.assertRaises(ValidationError):
            team.full_clean()

    def test_member_display_name_prefers_preferred_name(self):
        member = TeamMember.objects.create(
            employee_code="LKP-001",
            first_name="Example",
            last_name="Person",
            preferred_name="Alex",
            job_title="Developer",
        )

        self.assertEqual(
            member.full_name,
            "Example Person",
        )
        self.assertEqual(
            member.display_name,
            "Alex",
        )

    def test_member_rejects_self_reporting(self):
        member = TeamMember.objects.create(
            employee_code="LKP-002",
            first_name="Self",
            job_title="Manager",
        )

        member.reports_to = member

        with self.assertRaises(ValidationError):
            member.full_clean()

    def test_member_rejects_invalid_employment_dates(self):
        joined_at = timezone.localdate()
        ended_at = joined_at - timedelta(days=1)

        member = TeamMember(
            employee_code="LKP-003",
            first_name="Date",
            job_title="Tester",
            joined_at=joined_at,
            employment_ended_at=ended_at,
        )

        with self.assertRaises(ValidationError):
            member.full_clean()

    def test_current_member_status(self):
        member = TeamMember.objects.create(
            employee_code="LKP-004",
            first_name="Current",
            job_title="Designer",
            employment_status=EmploymentStatus.ACTIVE,
        )

        self.assertTrue(member.is_current)


class TeamManagementRepositoryTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name="Marketing",
            slug="marketing",
            team_type=TeamType.MARKETING,
            is_active=True,
            is_public=True,
        )

        self.member = TeamMember.objects.create(
            employee_code="LKP-100",
            first_name="Marketing",
            last_name="Member",
            job_title="Marketing Executive",
            engagement_type=EngagementType.FULL_TIME,
            employment_status=EmploymentStatus.ACTIVE,
            country="Sri Lanka",
            is_public=True,
        )

        TeamMembership.objects.create(
            team=self.team,
            member=self.member,
            is_primary=True,
            is_active=True,
        )

    def test_search_team(self):
        queryset = TeamRepository.search(
            search="Marketing",
            team_type=TeamType.MARKETING,
            is_public=True,
        )

        self.assertEqual(queryset.count(), 1)

    def test_find_team_by_slug(self):
        team = TeamRepository.find_by_slug(
            "marketing"
        )

        self.assertEqual(team.id, self.team.id)

    def test_search_member_by_team(self):
        queryset = TeamMemberRepository.search(
            search="Marketing Member",
            team_id=self.team.id,
            employment_status=(
                EmploymentStatus.ACTIVE
            ),
        )

        self.assertEqual(queryset.count(), 1)

    def test_search_member_by_reversed_full_name(self):
        queryset = TeamMemberRepository.search(
            search="Member Marketing",
            team_id=self.team.id,
        )

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(
            queryset.first().id,
            self.member.id,
        )

    def test_search_member_requires_all_terms(self):
        TeamMember.objects.create(
            employee_code="LKP-101",
            first_name="Marketing",
            last_name="Different",
            job_title="Designer",
            employment_status=(
                EmploymentStatus.ACTIVE
            ),
        )

        queryset = TeamMemberRepository.search(
            search="Marketing Member",
        )

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(
            queryset.first().id,
            self.member.id,
        )

    def test_public_team_members(self):
        members = list(
            PublicTeamRepository.members_for_team(
                self.team.id
            )
        )

        self.assertEqual(len(members), 1)
        self.assertEqual(
            members[0].id,
            self.member.id,
        )


class TeamManagementServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="team_admin",
            email="team-admin@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.user)

        self.team = Team.objects.create(
            name="Development",
            slug="development",
            team_type=TeamType.ENGINEERING,
        )

    def test_create_team(self):
        team = TeamManagementService.create_team(
            request=self.request,
            values={
                "name": "Design",
                "slug": "design",
                "team_type": TeamType.DESIGN,
            },
        )

        self.assertEqual(
            team.team_type,
            TeamType.DESIGN,
        )

    def test_update_team(self):
        team = TeamManagementService.update_team(
            request=self.request,
            team=self.team,
            values={
                "description": (
                    "Software development team."
                ),
                "is_public": True,
            },
        )

        self.assertTrue(team.is_public)
        self.assertEqual(
            team.description,
            "Software development team.",
        )

    def test_create_member_with_primary_team(self):
        member = TeamManagementService.create_member(
            request=self.request,
            values={
                "employee_code": "LKP-200",
                "first_name": "New",
                "last_name": "Developer",
                "job_title": "Software Developer",
            },
            memberships=[
                {
                    "team": self.team,
                    "role_title": "Developer",
                    "is_primary": True,
                    "is_active": True,
                    "joined_at": timezone.localdate(),
                    "left_at": None,
                    "sort_order": 0,
                },
            ],
            services=[],
        )

        self.assertEqual(
            member.team_memberships.count(),
            1,
        )
        self.assertTrue(
            member.team_memberships.first().is_primary
        )

    def test_update_member_replaces_memberships(self):
        member = TeamMember.objects.create(
            employee_code="LKP-201",
            first_name="Existing",
            job_title="Developer",
        )

        TeamMembership.objects.create(
            team=self.team,
            member=member,
            is_primary=True,
        )

        second_team = Team.objects.create(
            name="Quality Assurance",
            slug="quality-assurance",
        )

        member = TeamManagementService.update_member(
            request=self.request,
            member=member,
            values={
                "job_title": "QA Engineer",
            },
            memberships=[
                {
                    "team": second_team,
                    "role_title": "QA Engineer",
                    "is_primary": True,
                    "is_active": True,
                    "joined_at": timezone.localdate(),
                    "left_at": None,
                    "sort_order": 0,
                },
            ],
            services=[],
        )

        membership = (
            member.team_memberships.get()
        )

        self.assertEqual(
            membership.team,
            second_team,
        )
        self.assertEqual(
            member.job_title,
            "QA Engineer",
        )



from .repositories import (
    TeamManagementDashboardRepository,
)


class TeamManagementFinalizationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="team_final_admin",
            email="team-final@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.user)

        self.team = Team.objects.create(
            name="Final Engineering",
            slug="final-engineering",
            team_type=TeamType.ENGINEERING,
            is_active=True,
            is_public=True,
        )

        self.manager = TeamMember.objects.create(
            employee_code="LKP-300",
            first_name="Team",
            last_name="Manager",
            job_title="Engineering Manager",
            employment_status=(
                EmploymentStatus.ACTIVE
            ),
            is_leadership=True,
            is_public=True,
            is_featured=True,
        )

        self.member = TeamMember.objects.create(
            employee_code="LKP-301",
            first_name="Team",
            last_name="Developer",
            job_title="Software Developer",
            employment_status=(
                EmploymentStatus.ACTIVE
            ),
            is_public=True,
        )

        TeamMembership.objects.create(
            team=self.team,
            member=self.manager,
            is_primary=True,
            is_active=True,
        )

        TeamMembership.objects.create(
            team=self.team,
            member=self.member,
            is_primary=False,
            is_active=True,
        )

    def test_set_team_manager(self):
        team = TeamManagementService.set_team_manager(
            request=self.request,
            team=self.team,
            manager=self.manager,
        )

        self.assertEqual(
            team.manager,
            self.manager,
        )

    def test_reject_manager_outside_team(self):
        outsider = TeamMember.objects.create(
            employee_code="LKP-302",
            first_name="Outside",
            last_name="Manager",
            job_title="Manager",
        )

        with self.assertRaises(ValueError):
            TeamManagementService.set_team_manager(
                request=self.request,
                team=self.team,
                manager=outsider,
            )

    def test_update_reporting_line(self):
        member = (
            TeamManagementService
            .update_reporting_line(
                request=self.request,
                member=self.member,
                reports_to=self.manager,
            )
        )

        self.assertEqual(
            member.reports_to,
            self.manager,
        )

    def test_reporting_line_rejects_cycle(self):
        self.member.reports_to = self.manager
        self.member.save()

        with self.assertRaises(ValidationError):
            TeamManagementService.update_reporting_line(
                request=self.request,
                member=self.manager,
                reports_to=self.member,
            )

    def test_update_member_status(self):
        member = (
            TeamManagementService
            .update_member_status(
                request=self.request,
                member=self.member,
                employment_status=(
                    EmploymentStatus.RESIGNED
                ),
                employment_ended_at=(
                    timezone.localdate()
                ),
            )
        )

        self.assertEqual(
            member.employment_status,
            EmploymentStatus.RESIGNED,
        )

        membership = TeamMembership.objects.get(
            member=member,
            team=self.team,
        )

        self.assertFalse(membership.is_active)

    def test_dashboard_statistics(self):
        self.member.reports_to = self.manager
        self.member.save()

        stats = (
            TeamManagementDashboardRepository
            .statistics()
        )

        self.assertEqual(stats["total_teams"], 1)
        self.assertEqual(stats["active_teams"], 1)
        self.assertEqual(stats["public_teams"], 1)
        self.assertEqual(stats["total_members"], 2)
        self.assertEqual(stats["active_members"], 2)
        self.assertEqual(stats["public_members"], 2)
        self.assertEqual(
            stats["leadership_members"],
            1,
        )
        self.assertEqual(
            stats["featured_members"],
            1,
        )
        self.assertEqual(
            stats["members_without_manager"],
            0,
        )
        self.assertEqual(
            stats["team_sizes"][str(self.team.id)],
            2,
        )
