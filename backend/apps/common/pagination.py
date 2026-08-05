from dataclasses import dataclass
from math import ceil
from typing import Generic, TypeVar

from django.db.models import QuerySet


T = TypeVar("T")


@dataclass(frozen=True)
class PaginationParams:
    page: int = 1
    page_size: int = 25

    def normalized(self) -> "PaginationParams":
        return PaginationParams(
            page=max(self.page, 1),
            page_size=min(max(self.page_size, 1), 100),
        )


@dataclass(frozen=True)
class PaginatedResult(Generic[T]):
    items: list[T]
    page: int
    page_size: int
    total_items: int
    total_pages: int


def paginate_queryset(
    queryset: QuerySet,
    *,
    page: int = 1,
    page_size: int = 25,
) -> PaginatedResult:
    params = PaginationParams(
        page=page,
        page_size=page_size,
    ).normalized()

    total_items = queryset.count()
    total_pages = (
        ceil(total_items / params.page_size)
        if total_items
        else 0
    )

    offset = (params.page - 1) * params.page_size

    items = list(
        queryset[offset : offset + params.page_size]
    )

    return PaginatedResult(
        items=items,
        page=params.page,
        page_size=params.page_size,
        total_items=total_items,
        total_pages=total_pages,
    )
