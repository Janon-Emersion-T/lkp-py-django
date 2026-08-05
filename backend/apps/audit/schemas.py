from datetime import datetime
from typing import Any

from ninja import Schema


class AuditLogSchema(Schema):
    id: int
    actor_email: str | None
    event_type: str
    severity: str
    module: str
    target_type: str
    target_id: str
    message: str
    before: dict[str, Any] | None
    after: dict[str, Any] | None
    metadata: dict[str, Any]
    ip_address: str | None
    user_agent: str
    created_at: datetime
