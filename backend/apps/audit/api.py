from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.rbac.services import require_permissions

from .models import AuditLog
from .schemas import AuditLogSchema


router = Router(
    tags=["Audit Logs"],
    auth=jwt_auth,
)


@router.get(
    "",
    response={
        200: list[AuditLogSchema],
        403: ErrorSchema,
    },
)
@require_permissions("audit.view_auditlog")
def list_audit_logs(
    request,
    module: str | None = None,
    severity: str | None = None,
    limit: int = 100,
):
    limit = min(max(limit, 1), 500)

    queryset = AuditLog.objects.select_related("actor")

    if module:
        queryset = queryset.filter(module=module)

    if severity:
        queryset = queryset.filter(severity=severity)

    return [
        {
            "id": log.id,
            "actor_email": (
                log.actor.email
                if log.actor
                else None
            ),
            "event_type": log.event_type,
            "severity": log.severity,
            "module": log.module,
            "target_type": log.target_type,
            "target_id": log.target_id,
            "message": log.message,
            "before": log.before,
            "after": log.after,
            "metadata": log.metadata,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "created_at": log.created_at,
        }
        for log in queryset[:limit]
    ]
