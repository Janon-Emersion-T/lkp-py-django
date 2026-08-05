from apps.common.pagination import PaginatedResult


def paginated_response(
    result: PaginatedResult,
    *,
    serializer,
) -> dict:
    return {
        "items": [
            serializer(item)
            for item in result.items
        ],
        "pagination": {
            "page": result.page,
            "page_size": result.page_size,
            "total_items": result.total_items,
            "total_pages": result.total_pages,
        },
    }
