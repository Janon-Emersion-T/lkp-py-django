from typing import Literal
from uuid import UUID

from ninja import Schema
from pydantic import Field


SettingValueTypeValue = Literal[
    "string",
    "text",
    "integer",
    "decimal",
    "boolean",
    "json",
    "email",
    "url",
    "color",
    "media",
]

SettingEnvironmentValue = Literal[
    "global",
    "development",
    "staging",
    "production",
]


class WebsiteSettingGroupCreateSchema(Schema):
    name: str
    slug: str
    description: str = ""
    icon: str = ""
    is_active: bool = True
    sort_order: int = 0


class WebsiteSettingGroupUpdateSchema(
    WebsiteSettingGroupCreateSchema
):
    pass


class WebsiteSettingCreateSchema(Schema):
    group_id: UUID
    key: str
    label: str
    description: str = ""
    value_type: SettingValueTypeValue = "string"
    environment: SettingEnvironmentValue = "global"
    value: str = ""
    json_value: object = Field(default_factory=dict)
    media_asset_id: UUID | None = None
    default_value: str = ""
    validation_rules: dict = Field(default_factory=dict)
    is_public: bool = False
    is_editable: bool = True
    is_required: bool = False
    is_active: bool = True
    sort_order: int = 0


class WebsiteSettingUpdateSchema(
    WebsiteSettingCreateSchema
):
    pass


class WebsiteSettingBulkItemSchema(Schema):
    setting_id: UUID
    value: str | None = None
    json_value: object | None = None
    media_asset_id: UUID | None = None


class WebsiteSettingBulkUpdateSchema(Schema):
    settings: list[
        WebsiteSettingBulkItemSchema
    ] = Field(default_factory=list)


class WebsiteSettingSchema(Schema):
    id: UUID
    group_id: UUID
    group_name: str
    key: str
    label: str
    description: str
    value_type: str
    environment: str
    value: str
    json_value: object
    media_asset_id: UUID | None
    default_value: str
    validation_rules: dict
    typed_value: object
    is_public: bool
    is_editable: bool
    is_required: bool
    is_active: bool
    sort_order: int


class WebsiteSettingGroupSchema(Schema):
    id: UUID
    name: str
    slug: str
    description: str
    icon: str
    is_active: bool
    sort_order: int
    setting_count: int
    settings: list[WebsiteSettingSchema]


class PublicWebsiteSettingsSchema(Schema):
    environment: str
    settings: dict
