from django.contrib.auth import authenticate
from django.db import connection
from django.db.utils import OperationalError
from ninja import NinjaAPI
from ninja.errors import HttpError, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.api import router as users_router
from apps.accounts.models import User
from apps.accounts.security_api import router as security_router
from apps.accounts.security_services import (
    is_account_locked,
    register_failed_login,
    reset_failed_logins,
)
from apps.activity.api import router as activity_router
from apps.activity.services import log_activity
from apps.audit.api import router as audit_router
from apps.audit.models import AuditEventType, AuditSeverity
from apps.clients.api import router as clients_router
from apps.crm.api import router as crm_router
from apps.quotations.api import router as quotations_router
from apps.projects.api import router as projects_router
from apps.notifications.api import router as notifications_router
from apps.settings_manager.api import router as settings_router
from apps.rbac.api import router as rbac_router
from apps.audit.services import log_audit_event

from .auth import jwt_auth
from .common_schemas import (
    ErrorSchema,
    HealthSchema,
    MessageSchema,
    ReadinessSchema,
)
from .exceptions import ApiHttpError
from .rate_limit import enforce_rate_limit
from .schemas import (
    LoginSchema,
    LogoutSchema,
    RefreshSchema,
    TokenSchema,
    UserSchema,
)


api = NinjaAPI(
    title="LKProfessionals API",
    version="1.0.0",
    description="REST API for the LKProfessionals website, dashboard, and client portal.",
    docs_url="/docs",
)


@api.exception_handler(ApiHttpError)
def api_http_error_handler(request, exc):
    return api.create_response(
        request,
        {
            "status": "error",
            "message": str(exc),
            "code": exc.code,
            "details": exc.details,
        },
        status=exc.status_code,
    )


@api.exception_handler(HttpError)
def http_error_handler(request, exc):
    return api.create_response(
        request,
        {
            "status": "error",
            "message": str(exc),
            "code": "http_error",
            "details": None,
        },
        status=exc.status_code,
    )


@api.exception_handler(ValidationError)
def validation_error_handler(request, exc):
    return api.create_response(
        request,
        {
            "status": "error",
            "message": "Request validation failed.",
            "code": "validation_error",
            "details": {
                "errors": exc.errors,
            },
        },
        status=422,
    )


@api.get(
    "/health",
    response={
        200: HealthSchema,
    },
    tags=["System"],
)
def health_check(request):
    return {
        "status": "ok",
        "service": "lkprofessionals-api",
        "version": api.version,
    }


@api.get(
    "/ready",
    response={
        200: ReadinessSchema,
        503: ErrorSchema,
    },
    tags=["System"],
)
def readiness_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except OperationalError as exc:
        raise ApiHttpError(
            503,
            "Database is unavailable.",
            code="database_unavailable",
        ) from exc

    return {
        "status": "ready",
        "database": "ok",
    }


@api.post(
    "/auth/login",
    response={
        200: TokenSchema,
        401: ErrorSchema,
        423: ErrorSchema,
    },
    tags=["Authentication"],
)
def login(request, payload: LoginSchema):
    enforce_rate_limit(
        request,
        scope="auth-login",
        limit=10,
        window_seconds=300,
    )

    existing_user = User.objects.filter(
        email__iexact=payload.email,
        is_deleted=False,
    ).first()

    if existing_user and is_account_locked(existing_user):
        raise ApiHttpError(
            423,
            "Account is temporarily locked.",
            code="account_locked",
            details={
                "locked_until": existing_user.locked_until.isoformat(),
            },
        )

    user = authenticate(
        request,
        email=payload.email,
        password=payload.password,
    )

    if user is None:
        if existing_user:
            register_failed_login(
                request=request,
                user=existing_user,
            )
        else:
            log_audit_event(
                request=request,
                event_type=AuditEventType.LOGIN_FAILED,
                severity=AuditSeverity.WARNING,
                module="authentication",
                message="Failed login attempt.",
                metadata={"email": payload.email},
            )

        raise ApiHttpError(
            401,
            "Invalid email or password.",
            code="invalid_credentials",
        )

    if user.two_factor_enabled:
        raise ApiHttpError(
            401,
            "Two-factor authentication code is required.",
            code="two_factor_required",
        )

    reset_failed_logins(user)

    refresh = RefreshToken.for_user(user)

    log_audit_event(
        request=request,
        actor=user,
        event_type=AuditEventType.LOGIN_SUCCESS,
        module="authentication",
        message="User signed in successfully.",
        target_type="accounts.User",
        target_id=str(user.pk),
    )

    log_activity(
        request=request,
        actor=user,
        action="login",
        module="authentication",
        description="User signed in.",
        entity_type="accounts.User",
        entity_id=str(user.pk),
    )

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


@api.post(
    "/auth/refresh",
    response={
        200: TokenSchema,
        401: ErrorSchema,
    },
    tags=["Authentication"],
)
def refresh_token(request, payload: RefreshSchema):
    enforce_rate_limit(
        request,
        scope="auth-refresh",
        limit=30,
        window_seconds=300,
    )

    try:
        refresh = RefreshToken(payload.refresh)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
    except Exception as exc:
        log_audit_event(
            request=request,
            event_type=AuditEventType.SECURITY_EVENT,
            severity=AuditSeverity.WARNING,
            module="authentication",
            message="Invalid refresh token submitted.",
        )

        raise ApiHttpError(
            401,
            "Invalid refresh token.",
            code="invalid_refresh_token",
        ) from exc


@api.get(
    "/auth/me",
    response={
        200: UserSchema,
        401: ErrorSchema,
    },
    auth=jwt_auth,
    tags=["Authentication"],
)
def current_user(request):
    return request.auth


@api.post(
    "/auth/logout",
    response={
        200: MessageSchema,
        400: ErrorSchema,
        401: ErrorSchema,
    },
    auth=jwt_auth,
    tags=["Authentication"],
)
def logout(request, payload: LogoutSchema):
    try:
        refresh = RefreshToken(payload.refresh)
        refresh.blacklist()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.LOGOUT,
            module="authentication",
            message="User signed out successfully.",
            target_type="accounts.User",
            target_id=str(request.auth.pk),
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="logout",
            module="authentication",
            description="User signed out.",
            entity_type="accounts.User",
            entity_id=str(request.auth.pk),
        )

        return {
            "status": "ok",
            "message": "Signed out successfully.",
        }
    except Exception as exc:
        raise ApiHttpError(
            400,
            "Invalid refresh token.",
            code="invalid_refresh_token",
        ) from exc


api.add_router("/users", users_router)
api.add_router("/rbac", rbac_router)

api.add_router("/security", security_router)


api.add_router("/settings", settings_router)
api.add_router("/notifications", notifications_router)
api.add_router("/activity", activity_router)
api.add_router("/audit", audit_router)

api.add_router("/crm", crm_router)

api.add_router("/clients", clients_router)

api.add_router("/quotations", quotations_router)

api.add_router("/projects", projects_router)
