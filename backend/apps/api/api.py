from django.contrib.auth import authenticate
from ninja import NinjaAPI
from ninja.errors import HttpError
from rest_framework_simplejwt.tokens import RefreshToken
from .schemas import HealthSchema, LoginSchema, RefreshSchema, TokenSchema

api = NinjaAPI(title="LK Professionals API", version="1.0.0", docs_url="/docs")


@api.get("/health", response=HealthSchema, tags=["system"])
def healthcheck(request):
    return {"status": "ok"}


@api.post("/auth/login", response=TokenSchema, tags=["auth"])
def login(request, payload: LoginSchema):
    user = authenticate(request, email=payload.email, password=payload.password)
    if user is None:
        raise HttpError(401, "Invalid credentials")

    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


@api.post("/auth/refresh", response=TokenSchema, tags=["auth"])
def refresh_token(request, payload: RefreshSchema):
    try:
        refresh = RefreshToken(payload.refresh)
        return {"access": str(refresh.access_token), "refresh": str(payload.refresh)}
    except Exception as exc:  # pragma: no cover
        raise HttpError(401, "Invalid refresh token") from exc
