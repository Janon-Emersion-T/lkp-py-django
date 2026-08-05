from django.contrib.auth import authenticate
from ninja import NinjaAPI
from ninja.errors import HttpError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType, AuditSeverity
from apps.audit.services import log_audit_event

from .auth import jwt_auth
from .schemas import LoginSchema, LogoutSchema, RefreshSchema, TokenSchema, UserSchema


api = NinjaAPI(
    title="LKProfessionals API",
    version="1.0.0",
    description="REST API for the LKProfessionals website, dashboard, and client portal.",
    docs_url="/docs",
)


@api.get("/health", tags=["System"])
def health_check(request):
    return {
        "status": "ok",
        "service": "lkprofessionals-api",
    }


@api.post("/auth/login", response=TokenSchema, tags=["Authentication"])
def login(request, payload: LoginSchema):
    user = authenticate(
        request,
        email=payload.email,
        password=payload.password,
    )

    if user is None:
        log_audit_event(
            request=request,
            event_type=AuditEventType.LOGIN_FAILED,
            severity=AuditSeverity.WARNING,
            module="authentication",
            message="Failed login attempt.",
            metadata={"email": payload.email},
        )

        raise HttpError(401, "Invalid email or password")

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


@api.post("/auth/refresh", response=TokenSchema, tags=["Authentication"])
def refresh_token(request, payload: RefreshSchema):
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

        raise HttpError(401, "Invalid refresh token") from exc


@api.get(
    "/auth/me",
    response=UserSchema,
    auth=jwt_auth,
    tags=["Authentication"],
)
def current_user(request):
    return request.auth


@api.post(
    "/auth/logout",
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
            "message": "Signed out successfully",
        }
    except Exception as exc:
        raise HttpError(400, "Invalid refresh token") from exc
