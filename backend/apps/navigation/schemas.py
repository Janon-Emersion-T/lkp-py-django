from typing import Literal
from uuid import UUID

from ninja import Schema
from pydantic import Field


NavigationLocationValue = Literal[
    "header_primary",
    "header_secondary",
    "footer_primary",
    "footer_secondary",
    "footer_legal",
    "mobile",
    "dashboard",
    "client_portal",
    "custom",
]

MenuItemLinkTypeValue = Literal[
    "internal",
    "external",
    "route",
    "cms_page",
    "service",
    "package",
    "industry",
    "insight",
    "case_study",
    "careers",
    "contact",
    "quote",
    "custom",
]

MenuItemVisibilityValue = Literal[
    "everyone",
    "guests",
    "authenticated",
    "staff",
    "superuser",
]


class NavigationMenuCreateSchema(Schema):
    name: str
    slug: str
    location: NavigationLocationValue = "custom"
    description: str = ""
    is_active: bool = True
    is_public: bool = True
    sort_order: int = 0
    metadata: dict = Field(default_factory=dict)


class NavigationMenuUpdateSchema(
    NavigationMenuCreateSchema
):
    pass


class NavigationMenuItemCreateSchema(Schema):
    parent_id: UUID | None = None
    label: str
    link_type: MenuItemLinkTypeValue = "internal"
    url: str = ""
    route_name: str = ""
    route_parameters: dict = Field(
        default_factory=dict
    )
    cms_page_id: UUID | None = None
    service_id: UUID | None = None
    package_id: UUID | None = None
    industry_id: UUID | None = None
    insight_id: UUID | None = None
    case_study_id: UUID | None = None
    visibility: MenuItemVisibilityValue = "everyone"
    icon: str = ""
    css_class: str = ""
    target_blank: bool = False
    rel_attribute: str = ""
    is_active: bool = True
    is_featured: bool = False
    sort_order: int = 0
    metadata: dict = Field(default_factory=dict)


class NavigationMenuItemUpdateSchema(
    NavigationMenuItemCreateSchema
):
    pass


class NavigationReorderItemSchema(Schema):
    id: UUID
    parent_id: UUID | None = None
    sort_order: int


class NavigationReorderSchema(Schema):
    items: list[
        NavigationReorderItemSchema
    ] = Field(default_factory=list)


class NavigationMenuItemSchema(Schema):
    id: UUID
    menu_id: UUID
    parent_id: UUID | None
    label: str
    link_type: str
    url: str
    resolved_url: str
    route_name: str
    route_parameters: dict
    cms_page_id: UUID | None
    service_id: UUID | None
    package_id: UUID | None
    industry_id: UUID | None
    insight_id: UUID | None
    case_study_id: UUID | None
    visibility: str
    icon: str
    css_class: str
    target_blank: bool
    rel_attribute: str
    is_active: bool
    is_featured: bool
    sort_order: int
    depth: int
    metadata: dict
    children: list["NavigationMenuItemSchema"]


class NavigationMenuSchema(Schema):
    id: UUID
    name: str
    slug: str
    location: str
    description: str
    is_active: bool
    is_public: bool
    sort_order: int
    metadata: dict
    item_count: int
    items: list[NavigationMenuItemSchema]



class PublicNavigationMenuItemSchema(Schema):
    id: UUID
    parent_id: UUID | None
    label: str
    link_type: str
    url: str
    icon: str
    css_class: str
    target_blank: bool
    rel_attribute: str
    is_featured: bool
    sort_order: int
    metadata: dict
    children: list[
        "PublicNavigationMenuItemSchema"
    ]


class PublicNavigationMenuSchema(Schema):
    id: UUID
    name: str
    slug: str
    location: str
    description: str
    metadata: dict
    items: list[PublicNavigationMenuItemSchema]
