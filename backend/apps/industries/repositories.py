from django.db.models import QuerySet
from django.utils import timezone

from apps.common.query import apply_ordering, apply_search
from apps.common.repositories import BaseRepository

from .models import Industry, IndustryStatus


class IndustryRepository(BaseRepository[Industry]):
    model = Industry

    @classmethod
    def queryset(cls) -> QuerySet[Industry]:
        return (
            Industry.objects.select_related(
                "hero_image",
                "created_by",
                "updated_by",
            )
            .prefetch_related(
                "service_links__service",
                "faqs",
                "revisions",
            )
        )

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        status: str | None = None,
        is_featured: bool | None = None,
        is_active: bool | None = None,
        ordering: str | None = None,
    ) -> QuerySet[Industry]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "name",
                "slug",
                "short_description",
                "hero_title",
                "hero_description",
            ),
        )

        if status:
            queryset = queryset.filter(status=status)

        if is_featured is not None:
            queryset = queryset.filter(
                is_featured=is_featured,
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        return apply_ordering(
            queryset,
            ordering=ordering,
            allowed_fields=(
                "name",
                "slug",
                "status",
                "sort_order",
                "published_at",
                "scheduled_for",
                "created_at",
                "updated_at",
            ),
            default="sort_order",
        )

    @classmethod
    def public_industries(cls):
        return cls.queryset().filter(
            is_active=True,
            status=IndustryStatus.PUBLISHED,
            published_at__lte=timezone.now(),
        )
