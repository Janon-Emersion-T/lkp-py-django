from typing import Any

from ninja import Schema


class MessageSchema(Schema):
    status: str
    message: str


class ErrorSchema(Schema):
    status: str = "error"
    message: str
    code: str
    details: dict[str, Any] | None = None


class HealthSchema(Schema):
    status: str
    service: str
    version: str


class ReadinessSchema(Schema):
    status: str
    database: str
