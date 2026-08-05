from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from ninja import Router
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema, MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import User
from .security_schemas import (
    ChangePasswordSchema,
    LoginTwoFactorSchema,
    TwoFactorSetupSchema,
    TwoFactorStatusSchema,
    TwoFactorVerifySchema,
)
from .security_services import (
    create_two_factor_secret,
    is_account_locked,
    register_failed_login,
    reset_failed_logins,
    verify_two_factor_code,
)


router = Router(tags=["Account Security"])


@router.post(
    "/change-password",
    response={
        200: MessageSchema,
        400: ErrorSchema,
        401: ErrorSchema,
    },
    auth=jwt_auth,
)
def change_password(request, payload: ChangePasswordSchema):
    user = request.auth

    if not user.check_password(payload.current_password):
        raise ApiHttpError(
            400,
            "Current password is incorrect.",
            code="invalid_current_password",
        )

    try:
        validate_password(
            payload.new_password,
            user=user,
        )
    except ValidationError as exc:
        raise ApiHttpError(
            400,
            "New password does not meet security requirements.",
            code="weak_password",
            details={
                "errors": list(exc.messages),
            },
        ) from exc

    user.set_password(payload.new_password)
    user.must_change_password = False
    user.last_password_change_at = timezone.now()
    user.save(
        update_fields=[
            "password",
            "must_change_password",
            "last_password_change_at",
        ],
    )

    log_audit_event(
        request=request,
        actor=user,
        event_type=AuditEventType.PASSWORD_CHANGED,
        module="authentication",
        message="User changed account password.",
        target_type="accounts.User",
        target_id=str(user.pk),
    )

    return {
        "status": "ok",
        "message": "Password changed successfully.",
    }


@router.post(
    "/two-factor/setup",
    response={
        200: TwoFactorSetupSchema,
        400: ErrorSchema,
        401: ErrorSchema,
    },
    auth=jwt_auth,
)
def setup_two_factor(request):
    user = request.auth

    if user.two_factor_enabled:
        raise ApiHttpError(
            400,
            "Two-factor authentication is already enabled.",
            code="two_factor_already_enabled",
        )

    secret, provisioning_uri = create_two_factor_secret(user)

    user.two_factor_secret = secret
    user.save(update_fields=["two_factor_secret"])

    return {
        "secret": secret,
        "provisioning_uri": provisioning_uri,
    }


@router.post(
    "/two-factor/enable",
    response={
        200: TwoFactorStatusSchema,
        400: ErrorSchema,
        401: ErrorSchema,
    },
    auth=jwt_auth,
)
def enable_two_factor(request, payload: TwoFactorVerifySchema):
    user = request.auth

    if not verify_two_factor_code(
        secret=user.two_factor_secret,
        code=payload.code,
    ):
        raise ApiHttpError(
            400,
            "Invalid two-factor authentication code.",
            code="invalid_two_factor_code",
        )

    user.two_factor_enabled = True
    user.save(update_fields=["two_factor_enabled"])

    log_audit_event(
        request=request,
        actor=user,
        event_type=AuditEventType.SECURITY_EVENT,
        module="authentication",
        message="Two-factor authentication enabled.",
        target_type="accounts.User",
        target_id=str(user.pk),
    )

    return {
        "enabled": True,
    }


@router.post(
    "/two-factor/disable",
    response={
        200: TwoFactorStatusSchema,
        400: ErrorSchema,
        401: ErrorSchema,
    },
    auth=jwt_auth,
)
def disable_two_factor(request, payload: TwoFactorVerifySchema):
    user = request.auth

    if not user.two_factor_enabled:
        raise ApiHttpError(
            400,
            "Two-factor authentication is not enabled.",
            code="two_factor_not_enabled",
        )

    if not verify_two_factor_code(
        secret=user.two_factor_secret,
        code=payload.code,
    ):
        raise ApiHttpError(
            400,
            "Invalid two-factor authentication code.",
            code="invalid_two_factor_code",
        )

    user.two_factor_enabled = False
    user.two_factor_secret = ""
    user.save(
        update_fields=[
            "two_factor_enabled",
            "two_factor_secret",
        ],
    )

    log_audit_event(
        request=request,
        actor=user,
        event_type=AuditEventType.SECURITY_EVENT,
        module="authentication",
        message="Two-factor authentication disabled.",
        target_type="accounts.User",
        target_id=str(user.pk),
    )

    return {
        "enabled": False,
    }


@router.post(
    "/two-factor/login",
    response={
        200: dict,
        401: ErrorSchema,
        423: ErrorSchema,
    },
)
def two_factor_login(request, payload: LoginTwoFactorSchema):
    user = User.objects.filter(
        email__iexact=payload.email,
        is_deleted=False,
    ).first()

    if user is None:
        raise ApiHttpError(
            401,
            "Invalid authentication details.",
            code="invalid_credentials",
        )

    if is_account_locked(user):
        raise ApiHttpError(
            423,
            "Account is temporarily locked.",
            code="account_locked",
            details={
                "locked_until": user.locked_until.isoformat(),
            },
        )

    authenticated = authenticate(
        request,
        email=payload.email,
        password=payload.password,
    )

    if authenticated is None:
        register_failed_login(
            request=request,
            user=user,
        )

        raise ApiHttpError(
            401,
            "Invalid authentication details.",
            code="invalid_credentials",
        )

    if not user.two_factor_enabled:
        raise ApiHttpError(
            401,
            "Two-factor authentication is not enabled.",
            code="two_factor_not_enabled",
        )

    if not verify_two_factor_code(
        secret=user.two_factor_secret,
        code=payload.code,
    ):
        register_failed_login(
            request=request,
            user=user,
        )

        raise ApiHttpError(
            401,
            "Invalid authentication details.",
            code="invalid_two_factor_code",
        )

    reset_failed_logins(user)

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
