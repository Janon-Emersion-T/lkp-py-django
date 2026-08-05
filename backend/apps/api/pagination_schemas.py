from typing import Generic, TypeVar

from ninja import Schema


ItemType = TypeVar("ItemType")


class PaginationMetaSchema(Schema):
    page: int
    page_size: int
    total_items: int
    total_pages: int


class PaginatedResponseSchema(
    Schema,
    Generic[ItemType],
):
    items: list[ItemType]
    pagination: PaginationMetaSchema
