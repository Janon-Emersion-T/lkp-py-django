from collections.abc import Iterable

from django.db.models import Q, QuerySet


def apply_search(
    queryset: QuerySet,
    *,
    search: str | None,
    fields: Iterable[str],
) -> QuerySet:
    if not search:
        return queryset

    value = search.strip()

    if not value:
        return queryset

    query = Q()

    for field in fields:
        query |= Q(**{f"{field}__icontains": value})

    return queryset.filter(query)


def apply_ordering(
    queryset: QuerySet,
    *,
    ordering: str | None,
    allowed_fields: Iterable[str],
    default: str,
) -> QuerySet:
    allowed = set(allowed_fields)

    if not ordering:
        return queryset.order_by(default)

    field = ordering.removeprefix("-")

    if field not in allowed:
        return queryset.order_by(default)

    return queryset.order_by(ordering)
