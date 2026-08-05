from django.db.models import QuerySet
from django.utils import timezone

from apps.common.query import (
    apply_ordering,
    apply_search,
)
from apps.common.repositories import BaseRepository

from .models import (
    ArticleStatus,
    InsightArticle,
    InsightCategory,
    InsightTag,
)


class InsightArticleRepository(
    BaseRepository[InsightArticle]
):
    model = InsightArticle

    @classmethod
    def queryset(cls) -> QuerySet[InsightArticle]:
        return (
            InsightArticle.objects.select_related(
                "category",
                "author",
                "featured_image",
                "created_by",
                "updated_by",
            )
            .prefetch_related(
                "article_tags__tag",
                "related_articles",
                "revisions",
                "publishing_events",
                "outgoing_internal_links__target_article",
            )
        )

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        status: str | None = None,
        category_id: str | None = None,
        author_id: int | None = None,
        tag_id: str | None = None,
        is_featured: bool | None = None,
        is_active: bool | None = None,
        ordering: str | None = None,
    ) -> QuerySet[InsightArticle]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "title",
                "slug",
                "excerpt",
                "category__name",
                "author__email",
                "article_tags__tag__name",
            ),
        ).distinct()

        if status:
            queryset = queryset.filter(status=status)

        if category_id:
            queryset = queryset.filter(
                category_id=category_id,
            )

        if author_id:
            queryset = queryset.filter(
                author_id=author_id,
            )

        if tag_id:
            queryset = queryset.filter(
                article_tags__tag_id=tag_id,
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
                "published_at",
                "scheduled_for",
                "view_count",
                "reading_time_minutes",
                "created_at",
                "updated_at",
            ),
            default="-created_at",
        )

    @classmethod
    def public_articles(cls):
        return cls.queryset().filter(
            is_active=True,
            status=ArticleStatus.PUBLISHED,
            published_at__lte=timezone.now(),
        )


class InsightCategoryRepository(
    BaseRepository[InsightCategory]
):
    model = InsightCategory


class InsightTagRepository(BaseRepository[InsightTag]):
    model = InsightTag
