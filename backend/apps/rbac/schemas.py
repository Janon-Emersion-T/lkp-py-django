from uuid import UUID

from ninja import Schema
from pydantic import Field


class PermissionSchema(Schema):
    id: int
    app_label: str
    codename: str
    name: str


class RoleSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str
    priority: int
    is_system: bool
    is_active: bool
    permissions: list[PermissionSchema]


class RoleUpdateSchema(Schema):
    description: str = ""
    priority: int = Field(ge=1)
    is_active: bool = True
    permission_ids: list[int] = Field(default_factory=list)


class UserRoleAssignSchema(Schema):
    role_id: UUID
