from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.clients.models import Client
from apps.quotations.models import (
    Quotation,
    QuotationItem,
    QuotationStatus,
)

from .models import (
    MilestoneStatus,
    Project,
    ProjectStatus,
    ProjectTeamMember,
)
from .services import ProjectService


User = get_user_model()


class ProjectServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="project-admin",
            email="project-admin@example.com",
            password="StrongPassword123!",
        )

        self.staff = User.objects.create_user(
            username="project-staff",
            email="project-staff@example.com",
            password="StrongPassword123!",
        )

        self.client = Client.objects.create(
            company_name="Project Client",
            client_code="LKP-CL-00001",
            created_by=self.user,
            updated_by=self.user,
        )

        self.request = type(
            "Request",
            (),
            {
                "auth": self.user,
                "META": {},
            },
        )()

    def test_project_code_is_generated(self):
        first = ProjectService.create_project(
            request=self.request,
            values={
                "client": self.client,
                "title": "First Project",
            },
        )

        second = ProjectService.create_project(
            request=self.request,
            values={
                "client": self.client,
                "title": "Second Project",
            },
        )

        self.assertNotEqual(
            first.project_code,
            second.project_code,
        )
        self.assertTrue(
            first.project_code.startswith("LKP-PR-")
        )

    def test_project_progress_is_limited(self):
        project = ProjectService.create_project(
            request=self.request,
            values={
                "client": self.client,
                "title": "Progress Project",
            },
        )

        ProjectService.update_project(
            request=self.request,
            project=project,
            values={
                "progress": 150,
            },
        )

        project.refresh_from_db()

        self.assertEqual(project.progress, 100)

    def test_completed_project_sets_completion_data(self):
        project = ProjectService.create_project(
            request=self.request,
            values={
                "client": self.client,
                "title": "Completion Project",
            },
        )

        ProjectService.update_project(
            request=self.request,
            project=project,
            values={
                "status": ProjectStatus.COMPLETED,
            },
        )

        project.refresh_from_db()

        self.assertEqual(project.progress, 100)
        self.assertIsNotNone(project.completed_at)

    def test_team_member_can_be_assigned(self):
        project = ProjectService.create_project(
            request=self.request,
            values={
                "client": self.client,
                "title": "Team Project",
            },
        )

        assignment = (
            ProjectService.assign_team_member(
                request=self.request,
                project=project,
                user=self.staff,
                role="Developer",
                allocation_percentage=75,
            )
        )

        self.assertEqual(
            assignment.allocation_percentage,
            75,
        )
        self.assertTrue(
            ProjectTeamMember.objects.filter(
                project=project,
                user=self.staff,
            ).exists()
        )

    def test_milestone_can_be_created_and_completed(self):
        project = ProjectService.create_project(
            request=self.request,
            values={
                "client": self.client,
                "title": "Milestone Project",
            },
        )

        milestone = ProjectService.create_milestone(
            request=self.request,
            project=project,
            values={
                "title": "Development",
                "amount": Decimal("50000.00"),
            },
        )

        ProjectService.update_milestone(
            request=self.request,
            milestone=milestone,
            values={
                "status": MilestoneStatus.COMPLETED,
            },
        )

        milestone.refresh_from_db()

        self.assertEqual(milestone.progress, 100)
        self.assertIsNotNone(milestone.completed_at)

    def test_accepted_quotation_converts_to_project(self):
        quotation = Quotation.objects.create(
            quotation_number="LKP-QT-2026-00001",
            client=self.client,
            title="Accepted Website",
            description="Website development",
            status=QuotationStatus.ACCEPTED,
            total_amount=Decimal("100000.00"),
            currency="LKR",
            created_by=self.user,
            updated_by=self.user,
        )

        QuotationItem.objects.create(
            quotation=quotation,
            title="Website",
            total_amount=Decimal("70000.00"),
            created_by=self.user,
            updated_by=self.user,
        )

        QuotationItem.objects.create(
            quotation=quotation,
            title="SEO",
            total_amount=Decimal("30000.00"),
            created_by=self.user,
            updated_by=self.user,
        )

        project = ProjectService.convert_quotation(
            request=self.request,
            quotation=quotation,
        )

        self.assertEqual(
            project.quotation,
            quotation,
        )
        self.assertEqual(
            project.budget,
            Decimal("100000.00"),
        )
        self.assertEqual(
            project.milestones.count(),
            2,
        )

    def test_non_accepted_quotation_cannot_convert(self):
        quotation = Quotation.objects.create(
            quotation_number="LKP-QT-2026-00002",
            client=self.client,
            title="Draft Website",
            status=QuotationStatus.DRAFT,
            created_by=self.user,
            updated_by=self.user,
        )

        with self.assertRaises(ValueError):
            ProjectService.convert_quotation(
                request=self.request,
                quotation=quotation,
            )


from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api


class ProjectApiTests(TestCase):
    def setUp(self):
        self.api_client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="project-api-admin",
            email="project-api-admin@example.com",
            password="StrongPassword123!",
        )

        self.developer = User.objects.create_user(
            username="project-api-developer",
            email="project-api-developer@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(
            self.admin
        ).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

        self.client_record = Client.objects.create(
            company_name="Project API Client",
            client_code="LKP-CL-00990",
            country="Sri Lanka",
            created_by=self.admin,
            updated_by=self.admin,
        )

    def create_project_via_api(self):
        return self.api_client.post(
            "/projects",
            json={
                "client_id": str(
                    self.client_record.pk
                ),
                "project_manager_id": self.admin.pk,
                "title": "Business Website Project",
                "description": "Build a new business website.",
                "status": "planning",
                "priority": "high",
                "budget": "150000.00",
                "currency": "LKR",
                "progress": 0,
                "repository_url": (
                    "https://github.com/example/project"
                ),
                "tags": [
                    "website",
                    "priority",
                ],
            },
            headers=self.headers,
        )

    def test_superuser_can_create_project(self):
        response = self.create_project_via_api()

        self.assertEqual(response.status_code, 201)

        body = response.json()

        self.assertTrue(
            body["project_code"].startswith("LKP-PR-")
        )
        self.assertEqual(
            body["title"],
            "Business Website Project",
        )
        self.assertEqual(
            body["client_name"],
            "Project API Client",
        )
        self.assertEqual(
            body["budget"],
            "150000.00",
        )

    def test_superuser_can_list_and_search_projects(self):
        self.create_project_via_api()

        response = self.api_client.get(
            "/projects",
            data={
                "search": "Business Website",
                "status": "planning",
                "page": 1,
                "page_size": 10,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["pagination"][
                "total_items"
            ],
            1,
        )
        self.assertEqual(
            response.json()["items"][0]["title"],
            "Business Website Project",
        )

    def test_superuser_can_get_project_detail(self):
        created = self.create_project_via_api().json()

        response = self.api_client.get(
            f"/projects/{created['id']}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["id"],
            created["id"],
        )

    def test_superuser_can_update_project(self):
        created = self.create_project_via_api().json()

        response = self.api_client.put(
            f"/projects/{created['id']}",
            json={
                "client_id": str(
                    self.client_record.pk
                ),
                "project_manager_id": self.admin.pk,
                "title": "Updated Website Project",
                "description": "Updated description.",
                "status": "development",
                "priority": "urgent",
                "budget": "175000.00",
                "currency": "LKR",
                "progress": 40,
                "repository_url": (
                    "https://github.com/example/project"
                ),
                "staging_url": (
                    "https://staging.example.com"
                ),
                "production_url": "",
                "notes": "Development started.",
                "tags": [
                    "website",
                    "development",
                ],
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["title"],
            "Updated Website Project",
        )
        self.assertEqual(
            response.json()["status"],
            ProjectStatus.DEVELOPMENT,
        )
        self.assertEqual(
            response.json()["progress"],
            40,
        )

    def test_superuser_can_assign_team_member(self):
        created = self.create_project_via_api().json()

        response = self.api_client.post(
            f"/projects/{created['id']}/team",
            json={
                "user_id": self.developer.pk,
                "role": "Backend Developer",
                "allocation_percentage": 75,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["user"]["email"],
            self.developer.email,
        )
        self.assertEqual(
            response.json()["allocation_percentage"],
            75,
        )

    def test_superuser_can_create_and_update_milestone(self):
        created = self.create_project_via_api().json()

        milestone_response = self.api_client.post(
            f"/projects/{created['id']}/milestones",
            json={
                "title": "Backend Development",
                "description": "Develop backend APIs.",
                "status": "pending",
                "progress": 0,
                "sort_order": 1,
                "amount": "75000.00",
            },
            headers=self.headers,
        )

        self.assertEqual(
            milestone_response.status_code,
            201,
        )

        milestone = milestone_response.json()

        update_response = self.api_client.put(
            f"/projects/milestones/{milestone['id']}",
            json={
                "title": "Backend Development",
                "description": "Develop backend APIs.",
                "status": "completed",
                "progress": 50,
                "sort_order": 1,
                "amount": "75000.00",
            },
            headers=self.headers,
        )

        self.assertEqual(
            update_response.status_code,
            200,
        )
        self.assertEqual(
            update_response.json()["status"],
            MilestoneStatus.COMPLETED,
        )
        self.assertEqual(
            update_response.json()["progress"],
            100,
        )
        self.assertIsNotNone(
            update_response.json()["completed_at"]
        )

    def test_superuser_can_add_project_note(self):
        created = self.create_project_via_api().json()

        response = self.api_client.post(
            f"/projects/{created['id']}/notes",
            json={
                "content": (
                    "Client approved the initial design."
                ),
                "is_pinned": True,
                "is_client_visible": False,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["is_pinned"])

    def test_accepted_quotation_can_convert_to_project(self):
        quotation = Quotation.objects.create(
            quotation_number="LKP-QT-2026-00990",
            client=self.client_record,
            title="Converted Project",
            description="Converted quotation project.",
            status=QuotationStatus.ACCEPTED,
            total_amount=Decimal("200000.00"),
            currency="LKR",
            created_by=self.admin,
            updated_by=self.admin,
        )

        QuotationItem.objects.create(
            quotation=quotation,
            title="Application Development",
            description="Develop the application.",
            total_amount=Decimal("200000.00"),
            created_by=self.admin,
            updated_by=self.admin,
        )

        response = self.api_client.post(
            (
                "/projects/convert-quotation/"
                f"{quotation.pk}"
            ),
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["quotation_id"],
            str(quotation.pk),
        )
        self.assertEqual(
            response.json()["budget"],
            "200000.00",
        )
        self.assertEqual(
            len(response.json()["milestones"]),
            1,
        )

    def test_draft_quotation_cannot_convert_to_project(self):
        quotation = Quotation.objects.create(
            quotation_number="LKP-QT-2026-00991",
            client=self.client_record,
            title="Draft Conversion",
            status=QuotationStatus.DRAFT,
            created_by=self.admin,
            updated_by=self.admin,
        )

        response = self.api_client.post(
            (
                "/projects/convert-quotation/"
                f"{quotation.pk}"
            ),
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "invalid_project_conversion",
        )

    def test_superuser_can_soft_delete_project(self):
        created = self.create_project_via_api().json()

        response = self.api_client.delete(
            f"/projects/{created['id']}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Project.objects.filter(
                pk=created["id"],
            ).exists()
        )
        self.assertTrue(
            Project.all_objects.filter(
                pk=created["id"],
            ).exists()
        )

    def test_unauthenticated_project_request_is_rejected(self):
        response = self.api_client.get("/projects")

        self.assertEqual(response.status_code, 401)
