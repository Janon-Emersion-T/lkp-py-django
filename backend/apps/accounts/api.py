from django.core.exceptions import ObjectDoesNotExist
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema, MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.rbac.services import require_permissions

from .repositories import UserRepository
from .schemas import (
    RoleSummarySchema,
    UserCreateSchema,
    UserDetailSchema,
    UserListSchema,
    UserUpdateSchema,
)
from .services import UserService


router = Router(
    tags=["Users"],
    auth=jwt_auth,
)


def serialize_user(user):
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "job_title": user.job_title,
        "department": user.department,
        "timezone": user.timezone,
        "preferred_language": user.preferred_language,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "must_change_password": user.must_change_password,
        "last_login": user.last_login,
        "date_joined": user.date_joined,
        "roles": [
            {
                "id": assignment.role.id,
                "name": assignment.role.name,
                "slug": assignment.role.slug,
            }
            for assignment in user.role_assignments.filter(
                is_active=True,
                role__is_active=True,
            ).select_related("role")
        ],
    }


@router.get(
    "",
    response={
        200: list[UserListSchema],
        403: ErrorSchema,
    },
)
@require_permissions("accounts.view_user")
def list_users(request):
    return UserRepository.list_active()


@router.get(
    "/{user_id}",
    response={
        200: UserDetailSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("accounts.view_user")
def get_user(request, user_id: int):
    try:
        user = UserRepository.get_by_id(user_id)
    except ObjectDoesNotExist as exc:
        raise ApiHttpError(
            404,
            "User not found.",
            code="user_not_found",
        ) from exc

    return serialize_user(user)


@router.post(
    "",
    response={
        201: UserDetailSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("accounts.add_user")
def create_user(request, payload: UserCreateSchema):
    try:
        user = UserService.create_user(
            request=request,
            email=str(payload.email),
            username=payload.username,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
            phone=payload.phone,
            job_title=payload.job_title,
            department=payload.department,
            role_ids=[str(role_id) for role_id in payload.role_ids],
            is_active=payload.is_active,
            is_staff=payload.is_staff,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_user",
        ) from exc

    return 201, serialize_user(user)


@router.put(
    "/{user_id}",
    response={
        200: UserDetailSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("accounts.change_user")
def update_user(
    request,
    user_id: int,
    payload: UserUpdateSchema,
):
    try:
        user = UserRepository.get_by_id(user_id)
    except ObjectDoesNotExist as exc:
        raise ApiHttpError(
            404,
            "User not found.",
            code="user_not_found",
        ) from exc

    user = UserService.update_user(
        request=request,
        user=user,
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone=payload.phone,
        job_title=payload.job_title,
        department=payload.department,
        timezone_name=payload.timezone,
        preferred_language=payload.preferred_language,
        is_active=payload.is_active,
        is_staff=payload.is_staff,
    )

    return serialize_user(user)


@router.delete(
    "/{user_id}",
    response={
        200: MessageSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("accounts.delete_user")
def delete_user(request, user_id: int):
    try:
        user = UserRepository.get_by_id(user_id)
        UserService.soft_delete_user(
            request=request,
            user=user,
        )
    except ObjectDoesNotExist as exc:
        raise ApiHttpError(
            404,
            "User not found.",
            code="user_not_found",
        ) from exc
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_user_operation",
        ) from exc

    return {
        "status": "ok",
        "message": "User deleted successfully.",
    }
