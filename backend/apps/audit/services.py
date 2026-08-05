from typing import Any

from django.http import HttpRequest

from apps.accounts.models import User
from apps.common.request_context import (
    get_client_ip,
    get_user_agent,
)

from .models import (
    AuditEventType,
    AuditLog,
    AuditSeverity,
)


def log_audit_event(
    *,
    request: HttpRequest,
    event_type: AuditEventType | str,
    module: str,
    message: str,
    actor: User | None = None,
    severity: AuditSeverity | str = AuditSeverity.INFO,
    target_type: str = "",
    target_id: str = "",
    before: dict[str, Any] | None = None,
    after: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> AuditLog:
    return AuditLog.objects.create(
        actor=actor,
        event_type=event_type,
        severity=severity,
        module=module,
        target_type=target_type,
        target_id=target_id,
        message=message,
        before=before,
        after=after,
        metadata=metadata or {},
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
    )
