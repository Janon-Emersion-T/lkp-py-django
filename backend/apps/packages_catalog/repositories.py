from django.db.models import QuerySet
from django.utils import timezone

from apps.common.query import (
    apply_ordering,
    apply_search,
)
from apps.common.repositories import BaseRepository

from .models import (
    Package,
    PackageStatus,
)


class PackageRepository(BaseRepository[Package]):
    model = Package

    @classmethod
    def queryset(cls) -> QuerySet[Package]:
        return (
            Package.objects.select_related(
                "service",
                "created_by",
                "updated_by",
            )
            .prefetch_related(
                "features",
                "addons",
                "target_audiences",
                "faqs",
                "revisions",
                "comparison_items__comparison_group",
            )
        )

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        category: str | None = None,
        status: str | None = None,
        service_id: str | None = None,
        currency: str | None = None,
        billing_cycle: str | None = None,
        is_featured: bool | None = None,
        is_popular: bool | None = None,
        is_active: bool | None = None,
        ordering: str | None = None,
    ) -> QuerySet[Package]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "name",
                "slug",
                "short_description",
                "badge_text",
                "service__title",
            ),
        )

        if category:
            queryset = queryset.filter(category=category)

        if status:
            queryset = queryset.filter(status=status)

        if service_id:
            queryset = queryset.filter(
                service_id=service_id,
            )

        if currency:
            queryset = queryset.filter(
                currency=currency.upper(),
            )

        if billing_cycle:
            queryset = queryset.filter(
                billing_cycle=billing_cycle,
            )

        if is_featured is not None:
            queryset = queryset.filter(
                is_featured=is_featured,
            )

        if is_popular is not None:
            queryset = queryset.filter(
                is_popular=is_popular,
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
                "category",
                "status",
                "price",
                "currency",
                "billing_cycle",
                "sort_order",
                "published_at",
                "scheduled_for",
                "created_at",
                "updated_at",
            ),
            default="sort_order",
        )

    @classmethod
    def public_packages(cls) -> QuerySet[Package]:
        return cls.queryset().filter(
            is_active=True,
            status=PackageStatus.PUBLISHED,
            published_at__lte=timezone.now(),
        )

    @classmethod
    def scheduled_due(cls) -> QuerySet[Package]:
        return cls.queryset().filter(
            is_active=True,
            status=PackageStatus.SCHEDULED,
            scheduled_for__lte=timezone.now(),
        )
