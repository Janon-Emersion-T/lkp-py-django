from typing import Any
from uuid import UUID

from ninja import Schema
from pydantic import Field


class SystemSettingSchema(Schema):
    id: UUID
    group: str
    key: str
    value: Any | None
    data_type: str
    description: str
    is_public: bool
    is_editable: bool
    is_required: bool


class SystemSettingUpsertSchema(Schema):
    group: str = Field(min_length=1, max_length=100)
    key: str = Field(min_length=1, max_length=150)
    value: Any | None = None
    data_type: str
    description: str = ""
    is_public: bool = False
    is_editable: bool = True
    is_required: bool = False
