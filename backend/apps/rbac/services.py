from collections.abc import Iterable
from functools import wraps
from typing import Any, Callable, TypeVar

from django.db.models import Q, QuerySet
from django.utils import timezone
from ninja.errors import HttpError

from apps.accounts.models import User

from .models import UserRole


Endpoint = TypeVar("Endpoint", bound=Callable[..., Any])


def get_active_role_assignments(user: User) -> QuerySet[UserRole]:
    now = timezone.now()

    return (
        UserRole.objects.select_related("role")
        .filter(
            user=user,
            is_active=True,
            role__is_active=True,
        )
        .filter(
            Q(valid_from__isnull=True) | Q(valid_from__lte=now),
            Q(valid_until__isnull=True) | Q(valid_until__gte=now),
        )
    )


def user_has_permission(
    user: User | None,
    permission: str,
) -> bool:
    if user is None or not user.is_authenticated or not user.is_active:
        return False

    if user.is_superuser:
        return True

    if user.has_perm(permission):
        return True

    try:
        app_label, codename = permission.split(".", maxsplit=1)
    except ValueError as exc:
        raise ValueError(
            "Permission must use the 'app_label.codename' format."
        ) from exc

    return get_active_role_assignments(user).filter(
        role__permissions__content_type__app_label=app_label,
        role__permissions__codename=codename,
    ).exists()


def user_has_any_permission(
    user: User | None,
    permissions: Iterable[str],
) -> bool:
    return any(
        user_has_permission(user, permission)
        for permission in permissions
    )


def user_has_all_permissions(
    user: User | None,
    permissions: Iterable[str],
) -> bool:
    return all(
        user_has_permission(user, permission)
        for permission in permissions
    )


def require_permissions(
    *permissions: str,
    require_all: bool = True,
) -> Callable[[Endpoint], Endpoint]:
    if not permissions:
        raise ValueError("At least one permission is required.")

    def decorator(endpoint: Endpoint) -> Endpoint:
        @wraps(endpoint)
        def wrapper(request, *args, **kwargs):
            user = getattr(request, "auth", None)

            allowed = (
                user_has_all_permissions(user, permissions)
                if require_all
                else user_has_any_permission(user, permissions)
            )

            if not allowed:
                raise HttpError(
                    403,
                    "You do not have permission to perform this action.",
                )

            return endpoint(request, *args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator
