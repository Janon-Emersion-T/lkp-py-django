from django.test import TestCase

from .models import (
    EmploymentStatus,
    Team,
    TeamMember,
    TeamMembership,
)


class PublicTeamApiTests(TestCase):
    url = "/api/v1/team-management/public/teams"

    def setUp(self):
        self.team = Team.objects.create(
            name="Engineering",
            slug="engineering-public-test",
            team_type="engineering",
            description="Engineering team",
            is_active=True,
            is_public=True,
        )

        self.member = TeamMember.objects.create(
            employee_code="PUB-TEAM-001",
            first_name="Public",
            last_name="Member",
            job_title="Software Engineer",
            employment_status=EmploymentStatus.ACTIVE,
            is_public=True,
            is_featured=True,
            is_leadership=False,
        )

        TeamMembership.objects.create(
            team=self.team,
            member=self.member,
            is_primary=True,
            is_active=True,
        )

    def test_public_team_endpoint_requires_no_auth(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_public_member_contains_image_url(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

        payload = response.json()

        self.assertEqual(
            len(payload),
            1,
        )

        member = payload[0]["members"][0]

        self.assertIn(
            "profile_image_url",
            member,
        )

        self.assertEqual(
            member["display_name"],
            "Public Member",
        )

    def test_private_member_is_not_exposed(self):
        private = TeamMember.objects.create(
            employee_code="PUB-TEAM-002",
            first_name="Private",
            last_name="Member",
            job_title="Engineer",
            employment_status=EmploymentStatus.ACTIVE,
            is_public=False,
        )

        TeamMembership.objects.create(
            team=self.team,
            member=private,
            is_active=True,
        )

        response = self.client.get(self.url)

        names = [
            member["display_name"]
            for member
            in response.json()[0]["members"]
        ]

        self.assertNotIn(
            "Private Member",
            names,
        )
