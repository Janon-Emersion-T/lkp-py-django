from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.clients.models import Client
from apps.projects.models import Project

from .models import (
    Task,
    TaskDependencyType,
    TaskStatus,
)
from .services import TaskService


User = get_user_model()


class TaskServiceTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="task-admin",
            email="task-admin@example.com",
            password="StrongPassword123!",
        )

        self.developer = User.objects.create_user(
            username="task-developer",
            email="task-developer@example.com",
            password="StrongPassword123!",
        )

        self.client = Client.objects.create(
            company_name="Task Client",
            client_code="LKP-CL-00001",
            created_by=self.admin,
            updated_by=self.admin,
        )

        self.project = Project.objects.create(
            project_code="LKP-PR-2026-00001",
            client=self.client,
            title="Task Project",
            created_by=self.admin,
            updated_by=self.admin,
        )

        self.request = type(
            "Request",
            (),
            {
                "auth": self.admin,
                "META": {},
            },
        )()

    def create_task(self, title="Test Task"):
        return TaskService.create_task(
            request=self.request,
            values={
                "project": self.project,
                "title": title,
                "assignee": self.developer,
            },
        )

    def test_task_can_be_created(self):
        task = self.create_task()

        self.assertEqual(task.status, TaskStatus.TODO)
        self.assertEqual(task.assignee, self.developer)

    def test_completed_task_sets_progress_and_timestamp(self):
        task = self.create_task()

        TaskService.update_task(
            request=self.request,
            task=task,
            values={
                "status": TaskStatus.COMPLETED,
            },
        )

        task.refresh_from_db()

        self.assertEqual(task.progress, 100)
        self.assertIsNotNone(task.completed_at)

    def test_additional_assignee_can_be_added(self):
        task = self.create_task()

        assignment = (
            TaskService.assign_additional_user(
                request=self.request,
                task=task,
                user=self.admin,
            )
        )

        self.assertEqual(assignment.user, self.admin)

    def test_watcher_can_be_added(self):
        task = self.create_task()

        watcher = TaskService.add_watcher(
            request=self.request,
            task=task,
            user=self.admin,
        )

        self.assertEqual(watcher.user, self.admin)

    def test_checklist_item_can_be_completed(self):
        task = self.create_task()

        item = TaskService.add_checklist_item(
            request=self.request,
            task=task,
            title="Complete backend",
        )

        TaskService.toggle_checklist_item(
            request=self.request,
            item=item,
            is_completed=True,
        )

        item.refresh_from_db()

        self.assertTrue(item.is_completed)
        self.assertIsNotNone(item.completed_at)
        self.assertEqual(
            item.completed_by,
            self.admin,
        )

    def test_comment_can_be_added(self):
        task = self.create_task()

        comment = TaskService.add_comment(
            request=self.request,
            task=task,
            content="Task reviewed.",
        )

        self.assertEqual(
            comment.content,
            "Task reviewed.",
        )

    def test_dependency_can_be_added(self):
        first = self.create_task("First")
        second = self.create_task("Second")

        dependency = TaskService.add_dependency(
            request=self.request,
            task=second,
            related_task=first,
            dependency_type=TaskDependencyType.BLOCKED_BY,
        )

        self.assertEqual(dependency.task, second)
        self.assertEqual(
            dependency.related_task,
            first,
        )

    def test_task_cannot_depend_on_itself(self):
        task = self.create_task()

        with self.assertRaises(ValueError):
            TaskService.add_dependency(
                request=self.request,
                task=task,
                related_task=task,
                dependency_type=(
                    TaskDependencyType.BLOCKED_BY
                ),
            )

    def test_time_log_updates_actual_hours(self):
        task = self.create_task()

        TaskService.log_time(
            request=self.request,
            task=task,
            user=self.developer,
            work_date=date.today(),
            hours=Decimal("2.50"),
            description="Development work.",
        )

        TaskService.log_time(
            request=self.request,
            task=task,
            user=self.developer,
            work_date=date.today(),
            hours=Decimal("1.50"),
            description="Testing work.",
        )

        task.refresh_from_db()

        self.assertEqual(
            task.actual_hours,
            Decimal("4.00"),
        )

    def test_invalid_time_log_is_rejected(self):
        task = self.create_task()

        with self.assertRaises(ValueError):
            TaskService.log_time(
                request=self.request,
                task=task,
                user=self.developer,
                work_date=date.today(),
                hours=Decimal("0.00"),
            )

    def test_task_can_be_soft_deleted(self):
        task = self.create_task()

        TaskService.soft_delete(
            request=self.request,
            task=task,
        )

        self.assertFalse(
            Task.objects.filter(pk=task.pk).exists()
        )
        self.assertTrue(
            Task.all_objects.filter(pk=task.pk).exists()
        )


from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api


class TaskApiTests(TestCase):
    def setUp(self):
        self.api_client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="task-api-admin",
            email="task-api-admin@example.com",
            password="StrongPassword123!",
        )

        self.developer = User.objects.create_user(
            username="task-api-developer",
            email="task-api-developer@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(
            self.admin
        ).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

        self.client_record = Client.objects.create(
            company_name="Task API Client",
            client_code="LKP-CL-00980",
            created_by=self.admin,
            updated_by=self.admin,
        )

        self.project = Project.objects.create(
            project_code="LKP-PR-2026-00980",
            client=self.client_record,
            title="Task API Project",
            created_by=self.admin,
            updated_by=self.admin,
        )

    def create_task_via_api(self):
        return self.api_client.post(
            "/tasks",
            json={
                "project_id": str(self.project.pk),
                "assignee_id": self.developer.pk,
                "title": "Build authentication module",
                "description": "Implement authentication.",
                "status": "todo",
                "priority": "high",
                "estimated_hours": "8.00",
                "actual_hours": "0.00",
                "progress": 0,
                "sort_order": 1,
                "labels": [
                    "backend",
                    "security",
                ],
            },
            headers=self.headers,
        )

    def test_superuser_can_create_task(self):
        response = self.create_task_via_api()

        self.assertEqual(response.status_code, 201)

        body = response.json()

        self.assertEqual(
            body["title"],
            "Build authentication module",
        )
        self.assertEqual(
            body["project_title"],
            "Task API Project",
        )
        self.assertEqual(
            body["assignee"]["email"],
            self.developer.email,
        )

    def test_superuser_can_list_and_search_tasks(self):
        self.create_task_via_api()

        response = self.api_client.get(
            "/tasks",
            data={
                "search": "authentication",
                "status": "todo",
                "project_id": str(self.project.pk),
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["pagination"]["total_items"],
            1,
        )

    def test_superuser_can_update_task(self):
        created = self.create_task_via_api().json()

        response = self.api_client.put(
            f"/tasks/{created['id']}",
            json={
                "project_id": str(self.project.pk),
                "assignee_id": self.developer.pk,
                "title": "Complete authentication module",
                "description": "Complete JWT and refresh tokens.",
                "status": "in_progress",
                "priority": "urgent",
                "estimated_hours": "10.00",
                "actual_hours": "2.00",
                "progress": 25,
                "sort_order": 1,
                "labels": [
                    "backend",
                    "security",
                ],
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            TaskStatus.IN_PROGRESS,
        )
        self.assertEqual(
            response.json()["progress"],
            25,
        )

    def test_superuser_can_complete_task(self):
        created = self.create_task_via_api().json()

        response = self.api_client.put(
            f"/tasks/{created['id']}",
            json={
                "project_id": str(self.project.pk),
                "assignee_id": self.developer.pk,
                "title": created["title"],
                "description": created["description"],
                "status": "completed",
                "priority": created["priority"],
                "estimated_hours": created[
                    "estimated_hours"
                ],
                "actual_hours": "8.00",
                "progress": 50,
                "sort_order": created["sort_order"],
                "labels": created["labels"],
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["progress"],
            100,
        )
        self.assertIsNotNone(
            response.json()["completed_at"]
        )

    def test_superuser_can_add_assignee_and_watcher(self):
        created = self.create_task_via_api().json()

        assignee_response = self.api_client.post(
            f"/tasks/{created['id']}/assignees",
            json={
                "user_id": self.admin.pk,
            },
            headers=self.headers,
        )

        watcher_response = self.api_client.post(
            f"/tasks/{created['id']}/watchers",
            json={
                "user_id": self.admin.pk,
            },
            headers=self.headers,
        )

        self.assertEqual(
            assignee_response.status_code,
            201,
        )
        self.assertEqual(
            watcher_response.status_code,
            201,
        )

    def test_superuser_can_manage_checklist(self):
        created = self.create_task_via_api().json()

        item_response = self.api_client.post(
            f"/tasks/{created['id']}/checklist",
            json={
                "title": "Write tests",
                "sort_order": 1,
            },
            headers=self.headers,
        )

        self.assertEqual(item_response.status_code, 201)

        item = item_response.json()

        toggle_response = self.api_client.put(
            f"/tasks/checklist/{item['id']}",
            json={
                "is_completed": True,
            },
            headers=self.headers,
        )

        self.assertEqual(toggle_response.status_code, 200)
        self.assertTrue(
            toggle_response.json()["is_completed"]
        )

    def test_superuser_can_add_comment(self):
        created = self.create_task_via_api().json()

        response = self.api_client.post(
            f"/tasks/{created['id']}/comments",
            json={
                "content": "Authentication is ready for review.",
                "is_internal": True,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["author"]["email"],
            self.admin.email,
        )

    def test_superuser_can_add_dependency(self):
        first = self.create_task_via_api().json()

        second_response = self.api_client.post(
            "/tasks",
            json={
                "project_id": str(self.project.pk),
                "title": "Build dashboard",
                "status": "todo",
                "priority": "normal",
            },
            headers=self.headers,
        )

        second = second_response.json()

        response = self.api_client.post(
            f"/tasks/{second['id']}/dependencies",
            json={
                "related_task_id": first["id"],
                "dependency_type": "blocked_by",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["related_task_id"],
            first["id"],
        )

    def test_self_dependency_is_rejected(self):
        created = self.create_task_via_api().json()

        response = self.api_client.post(
            f"/tasks/{created['id']}/dependencies",
            json={
                "related_task_id": created["id"],
                "dependency_type": "blocked_by",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "invalid_task_dependency",
        )

    def test_superuser_can_log_time(self):
        created = self.create_task_via_api().json()

        response = self.api_client.post(
            f"/tasks/{created['id']}/time-logs",
            json={
                "user_id": self.developer.pk,
                "work_date": str(date.today()),
                "hours": "2.50",
                "description": "Authentication development.",
                "is_billable": True,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["hours"],
            "2.50",
        )

        detail = self.api_client.get(
            f"/tasks/{created['id']}",
            headers=self.headers,
        )

        self.assertEqual(
            detail.json()["actual_hours"],
            "2.50",
        )

    def test_superuser_can_soft_delete_task(self):
        created = self.create_task_via_api().json()

        response = self.api_client.delete(
            f"/tasks/{created['id']}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Task.objects.filter(
                pk=created["id"],
            ).exists()
        )
        self.assertTrue(
            Task.all_objects.filter(
                pk=created["id"],
            ).exists()
        )

    def test_unauthenticated_task_request_is_rejected(self):
        response = self.api_client.get("/tasks")

        self.assertEqual(response.status_code, 401)
