from datetime import datetime
from typing import Any
from uuid import UUID

from ninja import Schema


class NotificationSchema(Schema):
    id: UUID
    notification_type: str
    channel: str
    title: str
    message: str
    action_url: str
    metadata: dict[str, Any]
    is_read: bool
    read_at: datetime | None
    created_at: datetime
