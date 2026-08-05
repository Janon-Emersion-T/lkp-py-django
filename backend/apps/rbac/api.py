from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from ninja import Router

from apps.accounts.repositories import UserRepository
from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema, MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import Role, UserRole
from .schemas import (
    PermissionSchema,
    RoleSchema,
    RoleUpdateSchema,
    UserRoleAssignSchema,
)
from .services import require_permissions


router = Router(
    tags=["Roles and Permissions"],
    auth=jwt_auth,
)


def serialize_role(role):
    return {
        "id": role.id,
        "name": role.name,
        "slug": role.slug,
        "description": role.description,
        "priority": role.priority,
        "is_system": role.is_system,
        "is_active": role.is_active,
        "permissions": [
            {
                "id": permission.id,
                "app_label": permission.content_type.app_label,
                "codename": permission.codename,
                "name": permission.name,
            }
            for permission in role.permissions.select_related(
                "content_type"
            ).order_by(
                "content_type__app_label",
                "codename",
            )
        ],
    }


@router.get(
    "/roles",
    response={
        200: list[RoleSchema],
        403: ErrorSchema,
    },
)
@require_permissions("rbac.view_role")
def list_roles(request):
    return [
        serialize_role(role)
        for role in Role.objects.prefetch_related(
            "permissions__content_type"
        )
    ]


@router.put(
    "/roles/{role_id}",
    response={
        200: RoleSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("rbac.change_role")
@transaction.atomic
def update_role(request, role_id: str, payload: RoleUpdateSchema):
    try:
        role = Role.objects.get(pk=role_id)
    except ObjectDoesNotExist as exc:
        raise ApiHttpError(
            404,
            "Role not found.",
            code="role_not_found",
        ) from exc

    before = {
        "description": role.description,
        "priority": role.priority,
        "is_active": role.is_active,
        "permissions": list(
            role.permissions.values_list("id", flat=True)
        ),
    }

    role.description = payload.description
    role.priority = payload.priority
    role.is_active = payload.is_active
    role.save()

    permissions = Permission.objects.filter(
        id__in=payload.permission_ids,
    )

    role.permissions.set(permissions)

    log_audit_event(
        request=request,
        actor=request.auth,
        event_type=AuditEventType.PERMISSION_CHANGED,
        module="rbac",
        message="Role permissions updated.",
        target_type="rbac.Role",
        target_id=str(role.pk),
        before=before,
        after={
            "description": role.description,
            "priority": role.priority,
            "is_active": role.is_active,
            "permissions": list(
                role.permissions.values_list("id", flat=True)
            ),
        },
    )

    return serialize_role(role)


@router.get(
    "/permissions",
    response={
        200: list[PermissionSchema],
        403: ErrorSchema,
    },
)
@require_permissions("auth.view_permission")
def list_permissions(request):
    return [
        {
            "id": permission.id,
            "app_label": permission.content_type.app_label,
            "codename": permission.codename,
            "name": permission.name,
        }
        for permission in Permission.objects.select_related(
            "content_type"
        ).order_by(
            "content_type__app_label",
            "codename",
        )
    ]


@router.post(
    "/users/{user_id}/roles",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("rbac.add_userrole")
def assign_role(
    request,
    user_id: int,
    payload: UserRoleAssignSchema,
):
    try:
        user = UserRepository.get_by_id(user_id)
        role = Role.objects.get(
            pk=payload.role_id,
            is_active=True,
        )
    except ObjectDoesNotExist as exc:
        raise ApiHttpError(
            404,
            "User or role not found.",
            code="assignment_target_not_found",
        ) from exc

    assignment, created = UserRole.objects.get_or_create(
        user=user,
        role=role,
        defaults={
            "assigned_by": request.auth,
            "created_by": request.auth,
            "is_active": True,
        },
    )

    if not created and not assignment.is_active:
        assignment.is_active = True
        assignment.assigned_by = request.auth
        assignment.save()

    log_audit_event(
        request=request,
        actor=request.auth,
        event_type=AuditEventType.ROLE_ASSIGNED,
        module="rbac",
        message="Role assigned to user.",
        target_type="accounts.User",
        target_id=str(user.pk),
        metadata={
            "role_id": str(role.pk),
            "role": role.slug,
        },
    )

    return {
        "status": "ok",
        "message": "Role assigned successfully.",
    }
