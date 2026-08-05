from django.db.models import QuerySet
from django.utils import timezone

from apps.common.query import (
    apply_ordering,
    apply_search,
)
from apps.common.repositories import BaseRepository

from .models import (
    ContentStatus,
    Page,
    Redirect,
)


class PageRepository(BaseRepository[Page]):
    model = Page

    @classmethod
    def queryset(cls) -> QuerySet[Page]:
        return (
            Page.objects.select_related(
                "created_by",
                "updated_by",
            )
            .prefetch_related(
                "revisions",
                "publishing_events",
                "content_blocks__content_block",
            )
        )

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        status: str | None = None,
        page_type: str | None = None,
        is_indexable: bool | None = None,
        ordering: str | None = None,
    ) -> QuerySet[Page]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "title",
                "slug",
                "excerpt",
                "navigation_label",
            ),
        )

        if status:
            queryset = queryset.filter(status=status)

        if page_type:
            queryset = queryset.filter(
                page_type=page_type,
            )

        if is_indexable is not None:
            queryset = queryset.filter(
                is_indexable=is_indexable,
            )

        return apply_ordering(
            queryset,
            ordering=ordering,
            allowed_fields=(
                "title",
                "slug",
                "page_type",
                "status",
                "navigation_order",
                "published_at",
                "scheduled_for",
                "created_at",
                "updated_at",
            ),
            default="navigation_order",
        )

    @classmethod
    def public_pages(cls) -> QuerySet[Page]:
        return cls.queryset().filter(
            status=ContentStatus.PUBLISHED,
            published_at__lte=timezone.now(),
        )

    @classmethod
    def scheduled_due(cls) -> QuerySet[Page]:
        return cls.queryset().filter(
            status=ContentStatus.SCHEDULED,
            scheduled_for__lte=timezone.now(),
        )


class RedirectRepository(BaseRepository[Redirect]):
    model = Redirect

    @classmethod
    def active(cls) -> QuerySet[Redirect]:
        return Redirect.objects.filter(
            is_active=True,
        ).order_by("source_path")
