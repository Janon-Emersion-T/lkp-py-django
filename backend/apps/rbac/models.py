from django.conf import settings
from django.contrib.auth.models import Permission
from django.db import models

from apps.common.models import BaseModel


class Role(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
    )
    description = models.TextField(blank=True)

    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="lkp_roles",
    )

    priority = models.PositiveIntegerField(default=100)
    is_system = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta(BaseModel.Meta):
        ordering = ("priority", "name")

    def __str__(self):
        return self.name


class UserRole(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="role_assignments",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="user_assignments",
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="role_assignments_created",
    )

    valid_from = models.DateTimeField(
        null=True,
        blank=True,
    )
    valid_until = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("user", "role"),
                condition=models.Q(is_deleted=False),
                name="unique_active_user_role",
            ),
        ]
        indexes = [
            models.Index(
                fields=("user", "is_active"),
            ),
            models.Index(
                fields=("role", "is_active"),
            ),
        ]

    def __str__(self):
        return f"{self.user} — {self.role}"
