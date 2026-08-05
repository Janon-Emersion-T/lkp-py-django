from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        db_index=True,
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
    )
    job_title = models.CharField(
        max_length=150,
        blank=True,
    )
    department = models.CharField(
        max_length=150,
        blank=True,
    )
    timezone = models.CharField(
        max_length=64,
        default="Asia/Colombo",
    )
    preferred_language = models.CharField(
        max_length=10,
        default="en",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/%Y/%m/",
        blank=True,
        null=True,
    )

    must_change_password = models.BooleanField(default=False)
    last_password_change_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(
        max_length=64,
        blank=True,
    )

    failed_login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ("email",)

    def __str__(self) -> str:
        return self.email
