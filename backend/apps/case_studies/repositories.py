from django.db.models import QuerySet
from django.utils import timezone

from apps.common.query import (
    apply_ordering,
    apply_search,
)
from apps.common.repositories import BaseRepository

from .models import (
    CaseStudy,
    CaseStudyStatus,
)


class CaseStudyRepository(BaseRepository[CaseStudy]):
    model = CaseStudy

    @classmethod
    def queryset(cls) -> QuerySet[CaseStudy]:
        return (
            CaseStudy.objects.select_related(
                "client",
                "project",
                "industry",
                "featured_image",
                "created_by",
                "updated_by",
            )
            .prefetch_related(
                "service_links__service",
                "technologies__logo",
                "media_items__asset",
                "metrics",
                "milestones",
                "revisions",
            )
        )

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        status: str | None = None,
        client_id: str | None = None,
        project_id: str | None = None,
        industry_id: str | None = None,
        service_id: str | None = None,
        is_featured: bool | None = None,
        is_active: bool | None = None,
        ordering: str | None = None,
    ) -> QuerySet[CaseStudy]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "title",
                "slug",
                "client_name",
                "location",
                "short_description",
                "client__company_name",
                "project__title",
                "industry__name",
                "service_links__service__title",
            ),
        ).distinct()

        if status:
            queryset = queryset.filter(status=status)

        if client_id:
            queryset = queryset.filter(
                client_id=client_id,
            )

        if project_id:
            queryset = queryset.filter(
                project_id=project_id,
            )

        if industry_id:
            queryset = queryset.filter(
                industry_id=industry_id,
            )

        if service_id:
            queryset = queryset.filter(
                service_links__service_id=service_id,
            )

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
                "title",
                "slug",
                "status",
                "sort_order",
                "published_at",
                "scheduled_for",
                "project_completion_date",
                "view_count",
                "created_at",
                "updated_at",
            ),
            default="sort_order",
        )

    @classmethod
    def public_case_studies(cls):
        return cls.queryset().filter(
            is_active=True,
            status=CaseStudyStatus.PUBLISHED,
            published_at__lte=timezone.now(),
        )
