from typing import Any

from django.http import HttpRequest

from apps.accounts.models import User
from apps.common.request_context import (
    get_client_ip,
    get_user_agent,
)

from .models import ActivityLog


def log_activity(
    *,
    request: HttpRequest,
    action: str,
    module: str,
    description: str = "",
    actor: User | None = None,
    entity_type: str = "",
    entity_id: str = "",
    metadata: dict[str, Any] | None = None,
) -> ActivityLog:
    return ActivityLog.objects.create(
        actor=actor,
        action=action,
        module=module,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
        metadata=metadata or {},
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
    )
