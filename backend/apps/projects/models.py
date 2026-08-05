from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class ProjectStatus(models.TextChoices):
    PLANNING = "planning", "Planning"
    DEVELOPMENT = "development", "Development"
    TESTING = "testing", "Testing"
    REVIEW = "review", "Review"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class ProjectPriority(models.TextChoices):
    LOW = "low", "Low"
    NORMAL = "normal", "Normal"
    HIGH = "high", "High"
    URGENT = "urgent", "Urgent"


class MilestoneStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class Project(BaseModel):
    project_code = models.CharField(
        max_length=40,
        unique=True,
        db_index=True,
    )

    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.PROTECT,
        related_name="projects",
    )

    quotation = models.OneToOneField(
        "quotations.Quotation",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="project",
    )

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=30,
        choices=ProjectStatus.choices,
        default=ProjectStatus.PLANNING,
        db_index=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=ProjectPriority.choices,
        default=ProjectPriority.NORMAL,
        db_index=True,
    )

    budget = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    currency = models.CharField(
        max_length=3,
        default="LKR",
    )

    start_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    progress = models.PositiveSmallIntegerField(default=0)

    project_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="managed_projects",
    )

    repository_url = models.URLField(blank=True)
    staging_url = models.URLField(blank=True)
    production_url = models.URLField(blank=True)

    notes = models.TextField(blank=True)
    tags = models.JSONField(
        default=list,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("client", "status"),
            ),
            models.Index(
                fields=("status", "deadline"),
            ),
            models.Index(
                fields=("project_manager", "status"),
            ),
        ]

    def __str__(self):
        return self.project_code


class ProjectTeamMember(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="team_members",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_assignments",
    )

    role = models.CharField(
        max_length=150,
        blank=True,
    )
    allocation_percentage = models.PositiveSmallIntegerField(
        default=100,
    )
    is_active = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("project", "user"),
                condition=models.Q(is_deleted=False),
                name="unique_active_project_team_member",
            ),
        ]
        indexes = [
            models.Index(
                fields=("project", "is_active"),
            ),
        ]

    def __str__(self):
        return f"{self.project} — {self.user}"


class ProjectMilestone(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="milestones",
    )

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=30,
        choices=MilestoneStatus.choices,
        default=MilestoneStatus.PENDING,
        db_index=True,
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

    progress = models.PositiveSmallIntegerField(default=0)
    sort_order = models.PositiveIntegerField(default=0)

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "due_date",
            "created_at",
        )
        indexes = [
            models.Index(
                fields=("project", "status"),
            ),
            models.Index(
                fields=("project", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.title


class ProjectNote(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_notes",
    )

    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    is_client_visible = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("project", "is_pinned"),
            ),
        ]

    def __str__(self):
        return f"Note for {self.project}"


class ProjectFile(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="files",
    )

    title = models.CharField(max_length=250)
    file = models.FileField(
        upload_to="projects/files/%Y/%m/",
    )

    original_name = models.CharField(max_length=255)
    content_type = models.CharField(
        max_length=150,
        blank=True,
    )
    size = models.PositiveBigIntegerField(default=0)

    description = models.TextField(blank=True)
    is_client_visible = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("project", "created_at"),
            ),
        ]

    def __str__(self):
        return self.title


class ProjectEvent(BaseModel):
    project = models.ForeignKey(
        Project,
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
                fields=("project", "created_at"),
            ),
        ]

    def __str__(self):
        return f"{self.project}: {self.event_type}"
