from django.contrib.auth import authenticate
from ninja import NinjaAPI
from ninja.errors import HttpError
from rest_framework_simplejwt.tokens import RefreshToken

from .schemas import LoginSchema, RefreshSchema, TokenSchema, UserSchema


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
        raise HttpError(401, "Invalid email or password")

    refresh = RefreshToken.for_user(user)

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
        raise HttpError(401, "Invalid refresh token") from exc
