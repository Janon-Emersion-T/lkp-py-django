from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class TeamType(models.TextChoices):
    EXECUTIVE = "executive", "Executive"
    MANAGEMENT = "management", "Management"
    ENGINEERING = "engineering", "Engineering"
    DESIGN = "design", "Design"
    MARKETING = "marketing", "Marketing"
    SALES = "sales", "Sales"
    FINANCE = "finance", "Finance"
    OPERATIONS = "operations", "Operations"
    SUPPORT = "support", "Support"
    HR = "hr", "Human resources"
    LEGAL = "legal", "Legal"
    PROJECT = "project", "Project team"
    CUSTOM = "custom", "Custom"


class EmploymentStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    ON_LEAVE = "on_leave", "On leave"
    SUSPENDED = "suspended", "Suspended"
    RESIGNED = "resigned", "Resigned"
    TERMINATED = "terminated", "Terminated"
    CONTRACT_ENDED = "contract_ended", "Contract ended"
    INACTIVE = "inactive", "Inactive"


class EngagementType(models.TextChoices):
    FULL_TIME = "full_time", "Full-time"
    PART_TIME = "part_time", "Part-time"
    CONTRACT = "contract", "Contract"
    INTERN = "intern", "Intern"
    CONSULTANT = "consultant", "Consultant"
    VOLUNTEER = "volunteer", "Volunteer"


class WorkLocationType(models.TextChoices):
    ONSITE = "onsite", "On-site"
    REMOTE = "remote", "Remote"
    HYBRID = "hybrid", "Hybrid"


class Team(BaseModel):
    name = models.CharField(
        max_length=150,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=170,
        unique=True,
        db_index=True,
    )

    team_type = models.CharField(
        max_length=30,
        choices=TeamType.choices,
        default=TeamType.CUSTOM,
        db_index=True,
    )

    description = models.TextField(blank=True)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="child_teams",
    )

    manager = models.ForeignKey(
        "TeamMember",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="managed_teams",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    is_public = models.BooleanField(
        default=False,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "name",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("name",),
                condition=models.Q(is_deleted=False),
                name="unique_active_team_name",
            ),
        ]
        indexes = [
            models.Index(
                fields=("team_type", "is_active"),
            ),
            models.Index(
                fields=("parent", "sort_order"),
            ),
            models.Index(
                fields=("is_public", "sort_order"),
            ),
        ]

    def clean(self):
        super().clean()

        if self.parent_id == self.id:
            raise ValidationError(
                {
                    "parent": (
                        "A team cannot be its own parent."
                    ),
                }
            )

        ancestor = self.parent

        while ancestor is not None:
            if ancestor.pk == self.pk:
                raise ValidationError(
                    {
                        "parent": (
                            "Circular team nesting is not allowed."
                        ),
                    }
                )

            ancestor = ancestor.parent

        if (
            self.manager_id
            and self.pk
            and not self.manager.team_memberships.filter(
                team=self,
                is_primary=True,
                is_active=True,
            ).exists()
        ):
            raise ValidationError(
                {
                    "manager": (
                        "The manager must be an active primary "
                        "member of this team."
                    ),
                }
            )

    def __str__(self):
        return self.name


class TeamMember(BaseModel):
    user = models.OneToOneField(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="team_profile",
    )

    employee_code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    first_name = models.CharField(
        max_length=100,
        db_index=True,
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    preferred_name = models.CharField(
        max_length=100,
        blank=True,
    )

    job_title = models.CharField(
        max_length=200,
        db_index=True,
    )

    professional_title = models.CharField(
        max_length=200,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
        db_index=True,
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
    )

    public_email = models.EmailField(blank=True)

    public_phone = models.CharField(
        max_length=50,
        blank=True,
    )

    profile_image = models.ForeignKey(
        "media_library.MediaAsset",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="team_member_profile_usages",
    )

    bio = models.TextField(blank=True)

    short_bio = models.CharField(
        max_length=500,
        blank=True,
    )

    qualifications = models.TextField(blank=True)

    years_of_experience = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    engagement_type = models.CharField(
        max_length=30,
        choices=EngagementType.choices,
        default=EngagementType.FULL_TIME,
        db_index=True,
    )

    employment_status = models.CharField(
        max_length=30,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.ACTIVE,
        db_index=True,
    )

    work_location_type = models.CharField(
        max_length=20,
        choices=WorkLocationType.choices,
        default=WorkLocationType.ONSITE,
        db_index=True,
    )

    office_location = models.CharField(
        max_length=200,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    timezone_name = models.CharField(
        max_length=100,
        default="Asia/Colombo",
    )

    joined_at = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    employment_ended_at = models.DateField(
        null=True,
        blank=True,
    )

    reports_to = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="direct_reports",
    )

    linkedin_url = models.URLField(blank=True)

    github_url = models.URLField(blank=True)

    portfolio_url = models.URLField(blank=True)

    website_url = models.URLField(blank=True)

    is_leadership = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_public = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_featured = models.BooleanField(
        default=False,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    services = models.ManyToManyField(
        "services_catalog.Service",
        through="TeamMemberService",
        related_name="team_members",
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "first_name",
            "last_name",
        )
        indexes = [
            models.Index(
                fields=("employment_status", "sort_order"),
            ),
            models.Index(
                fields=("is_public", "is_featured"),
            ),
            models.Index(
                fields=("reports_to", "employment_status"),
            ),
            models.Index(
                fields=("country", "employment_status"),
            ),
        ]

    @property
    def full_name(self):
        return " ".join(
            part
            for part in (
                self.first_name,
                self.last_name,
            )
            if part
        )

    @property
    def display_name(self):
        return self.preferred_name or self.full_name

    @property
    def is_current(self):
        return (
            self.employment_status
            in {
                EmploymentStatus.ACTIVE,
                EmploymentStatus.ON_LEAVE,
            }
            and not self.is_deleted
        )

    def clean(self):
        super().clean()

        if self.reports_to_id == self.id:
            raise ValidationError(
                {
                    "reports_to": (
                        "A team member cannot report to themselves."
                    ),
                }
            )

        manager = self.reports_to

        while manager is not None:
            if manager.pk == self.pk:
                raise ValidationError(
                    {
                        "reports_to": (
                            "Circular reporting lines are not allowed."
                        ),
                    }
                )

            manager = manager.reports_to

        if (
            self.joined_at
            and self.employment_ended_at
            and self.employment_ended_at < self.joined_at
        ):
            raise ValidationError(
                {
                    "employment_ended_at": (
                        "Employment end date cannot be before "
                        "the joining date."
                    ),
                }
            )

    def __str__(self):
        return (
            f"{self.employee_code} — "
            f"{self.display_name}"
        )


class TeamMembership(BaseModel):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    member = models.ForeignKey(
        TeamMember,
        on_delete=models.CASCADE,
        related_name="team_memberships",
    )

    role_title = models.CharField(
        max_length=200,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    joined_at = models.DateField(
        default=timezone.localdate,
    )

    left_at = models.DateField(
        null=True,
        blank=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "-is_primary",
            "sort_order",
            "joined_at",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("team", "member"),
                condition=models.Q(is_deleted=False),
                name="unique_active_team_membership",
            ),
            models.UniqueConstraint(
                fields=("member",),
                condition=models.Q(
                    is_deleted=False,
                    is_primary=True,
                    is_active=True,
                ),
                name="unique_active_primary_team_membership",
            ),
        ]
        indexes = [
            models.Index(
                fields=("team", "is_active", "sort_order"),
            ),
            models.Index(
                fields=("member", "is_primary", "is_active"),
            ),
        ]

    def clean(self):
        super().clean()

        if (
            self.left_at
            and self.joined_at
            and self.left_at < self.joined_at
        ):
            raise ValidationError(
                {
                    "left_at": (
                        "Membership end date cannot be before "
                        "the joining date."
                    ),
                }
            )

        if self.left_at:
            self.is_active = False

    def __str__(self):
        return (
            f"{self.member.display_name} — "
            f"{self.team.name}"
        )


class ExpertiseLevel(models.TextChoices):
    AWARENESS = "awareness", "Awareness"
    WORKING = "working", "Working knowledge"
    PROFICIENT = "proficient", "Proficient"
    EXPERT = "expert", "Expert"
    LEAD = "lead", "Lead specialist"


class TeamMemberService(BaseModel):
    member = models.ForeignKey(
        TeamMember,
        on_delete=models.CASCADE,
        related_name="service_assignments",
    )

    service = models.ForeignKey(
        "services_catalog.Service",
        on_delete=models.PROTECT,
        related_name="team_assignments",
    )

    expertise_level = models.CharField(
        max_length=20,
        choices=ExpertiseLevel.choices,
        default=ExpertiseLevel.PROFICIENT,
        db_index=True,
    )

    years_of_experience = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_public = models.BooleanField(
        default=True,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "-is_primary",
            "sort_order",
            "service__title",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("member", "service"),
                condition=models.Q(is_deleted=False),
                name="unique_active_team_member_service",
            ),
        ]
        indexes = [
            models.Index(
                fields=("member", "is_primary"),
            ),
            models.Index(
                fields=("service", "expertise_level"),
            ),
            models.Index(
                fields=("is_public", "sort_order"),
            ),
        ]

    def __str__(self):
        return (
            f"{self.member.display_name} — "
            f"{self.service.title}"
        )
