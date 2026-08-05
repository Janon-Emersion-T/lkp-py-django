from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class TaskStatus(models.TextChoices):
    TODO = "todo", "To Do"
    IN_PROGRESS = "in_progress", "In Progress"
    TESTING = "testing", "Testing"
    REVIEW = "review", "Review"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class TaskPriority(models.TextChoices):
    LOW = "low", "Low"
    NORMAL = "normal", "Normal"
    HIGH = "high", "High"
    URGENT = "urgent", "Urgent"


class TaskDependencyType(models.TextChoices):
    BLOCKS = "blocks", "Blocks"
    BLOCKED_BY = "blocked_by", "Blocked By"
    RELATED = "related", "Related"


class Task(BaseModel):
    project = models.ForeignKey(
        "projects.Project",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    milestone = models.ForeignKey(
        "projects.ProjectMilestone",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tasks",
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subtasks",
    )

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=30,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
        db_index=True,
    )

    priority = models.CharField(
        max_length=30,
        choices=TaskPriority.choices,
        default=TaskPriority.NORMAL,
        db_index=True,
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_tasks",
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    estimated_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    actual_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    progress = models.PositiveSmallIntegerField(default=0)
    sort_order = models.PositiveIntegerField(default=0)

    labels = models.JSONField(
        default=list,
        blank=True,
    )

    is_recurring = models.BooleanField(default=False)
    recurrence_rule = models.CharField(
        max_length=255,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "-created_at",
        )
        indexes = [
            models.Index(
                fields=("project", "status"),
            ),
            models.Index(
                fields=("assignee", "status"),
            ),
            models.Index(
                fields=("priority", "due_date"),
            ),
            models.Index(
                fields=("milestone", "status"),
            ),
        ]

    def __str__(self):
        return self.title


class TaskAssignee(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="additional_assignees",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_assignments",
    )

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("task", "user"),
                condition=models.Q(is_deleted=False),
                name="unique_active_task_assignee",
            ),
        ]

    def __str__(self):
        return f"{self.task} — {self.user}"


class TaskWatcher(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="watchers",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watched_tasks",
    )

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("task", "user"),
                condition=models.Q(is_deleted=False),
                name="unique_active_task_watcher",
            ),
        ]

    def __str__(self):
        return f"{self.task} — {self.user}"


class TaskChecklistItem(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="checklist_items",
    )

    title = models.CharField(max_length=250)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="completed_task_checklist_items",
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        indexes = [
            models.Index(
                fields=("task", "is_completed"),
            ),
        ]

    def __str__(self):
        return self.title


class TaskComment(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    content = models.TextField()
    is_internal = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("task", "created_at"),
            ),
        ]

    def __str__(self):
        return f"Comment on {self.task}"


class TaskAttachment(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    title = models.CharField(max_length=250)
    file = models.FileField(
        upload_to="tasks/attachments/%Y/%m/",
    )
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(
        max_length=150,
        blank=True,
    )
    size = models.PositiveBigIntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("task", "created_at"),
            ),
        ]

    def __str__(self):
        return self.title


class TaskDependency(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="dependencies",
    )
    related_task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="dependent_tasks",
    )

    dependency_type = models.CharField(
        max_length=30,
        choices=TaskDependencyType.choices,
        default=TaskDependencyType.RELATED,
    )

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "task",
                    "related_task",
                    "dependency_type",
                ),
                condition=models.Q(is_deleted=False),
                name="unique_active_task_dependency",
            ),
            models.CheckConstraint(
                condition=~models.Q(
                    task=models.F("related_task"),
                ),
                name="task_dependency_not_self",
            ),
        ]

    def __str__(self):
        return f"{self.task} → {self.related_task}"


class TaskTimeLog(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="time_logs",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="task_time_logs",
    )

    work_date = models.DateField(db_index=True)
    hours = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
    description = models.TextField(blank=True)
    is_billable = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("task", "work_date"),
            ),
            models.Index(
                fields=("user", "work_date"),
            ),
        ]

    def __str__(self):
        return f"{self.task} — {self.hours}h"


class TaskEvent(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="events",
    )
    event_type = models.CharField(
        max_length=50,
        db_index=True,
    )
    description = models.TextField()
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("task", "created_at"),
            ),
        ]

    def __str__(self):
        return f"{self.task}: {self.event_type}"
