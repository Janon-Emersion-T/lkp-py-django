from datetime import datetime
from typing import Any

from ninja import Schema


class ActivityLogSchema(Schema):
    id: int
    actor_email: str | None
    action: str
    module: str
    entity_type: str
    entity_id: str
    description: str
    metadata: dict[str, Any]
    ip_address: str | None
    user_agent: str
    created_at: datetime
