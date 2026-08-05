from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.rbac.services import require_permissions

from .models import ActivityLog
from .schemas import ActivityLogSchema


router = Router(
    tags=["Activity Logs"],
    auth=jwt_auth,
)


@router.get(
    "",
    response={
        200: list[ActivityLogSchema],
        403: ErrorSchema,
    },
)
@require_permissions("activity.view_activitylog")
def list_activity_logs(
    request,
    module: str | None = None,
    limit: int = 100,
):
    limit = min(max(limit, 1), 500)

    queryset = ActivityLog.objects.select_related("actor")

    if module:
        queryset = queryset.filter(module=module)

    return [
        {
            "id": log.id,
            "actor_email": (
                log.actor.email
                if log.actor
                else None
            ),
            "action": log.action,
            "module": log.module,
            "entity_type": log.entity_type,
            "entity_id": log.entity_id,
            "description": log.description,
            "metadata": log.metadata,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "created_at": log.created_at,
        }
        for log in queryset[:limit]
    ]
