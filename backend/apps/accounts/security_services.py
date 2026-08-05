from datetime import timedelta

import pyotp
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.audit.models import (
    AuditEventType,
    AuditSeverity,
)
from apps.audit.services import log_audit_event

from .models import User


MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


def is_account_locked(user: User) -> bool:
    if user.locked_until is None:
        return False

    if user.locked_until <= timezone.now():
        user.failed_login_attempts = 0
        user.locked_until = None
        user.save(
            update_fields=[
                "failed_login_attempts",
                "locked_until",
            ],
        )
        return False

    return True


@transaction.atomic
def register_failed_login(
    *,
    request,
    user: User,
) -> None:
    user.failed_login_attempts += 1

    if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
        user.locked_until = timezone.now() + timedelta(
            minutes=LOCKOUT_MINUTES,
        )

    user.save(
        update_fields=[
            "failed_login_attempts",
            "locked_until",
        ],
    )

    log_audit_event(
        request=request,
        actor=user,
        event_type=AuditEventType.LOGIN_FAILED,
        severity=AuditSeverity.WARNING,
        module="authentication",
        message="Failed login attempt recorded.",
        target_type="accounts.User",
        target_id=str(user.pk),
        metadata={
            "email": user.email,
            "failed_attempts": user.failed_login_attempts,
            "locked_until": (
                user.locked_until.isoformat()
                if user.locked_until
                else None
            ),
        },
    )


def reset_failed_logins(user: User) -> None:
    if user.failed_login_attempts == 0 and user.locked_until is None:
        return

    user.failed_login_attempts = 0
    user.locked_until = None
    user.save(
        update_fields=[
            "failed_login_attempts",
            "locked_until",
        ],
    )


def create_two_factor_secret(user: User) -> tuple[str, str]:
    secret = pyotp.random_base32()

    issuer = getattr(
        settings,
        "TWO_FACTOR_ISSUER",
        "LKProfessionals",
    )

    uri = pyotp.TOTP(secret).provisioning_uri(
        name=user.email,
        issuer_name=issuer,
    )

    return secret, uri


def verify_two_factor_code(
    *,
    secret: str,
    code: str,
) -> bool:
    if not secret:
        return False

    return pyotp.TOTP(secret).verify(
        code,
        valid_window=1,
    )
