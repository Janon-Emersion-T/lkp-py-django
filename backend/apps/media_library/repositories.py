from django.db.models import QuerySet

from apps.common.query import (
    apply_ordering,
    apply_search,
)
from apps.common.repositories import BaseRepository

from .models import (
    MediaAsset,
    MediaFolder,
    MediaUsage,
)


class MediaFolderRepository(BaseRepository[MediaFolder]):
    model = MediaFolder

    @classmethod
    def queryset(cls) -> QuerySet[MediaFolder]:
        return MediaFolder.objects.select_related(
            "parent",
            "created_by",
            "updated_by",
        ).prefetch_related(
            "children",
            "assets",
        )

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        parent_id: str | None = None,
        ordering: str | None = None,
    ) -> QuerySet[MediaFolder]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "name",
                "slug",
                "description",
            ),
        )

        if parent_id:
            queryset = queryset.filter(
                parent_id=parent_id,
            )

        return apply_ordering(
            queryset,
            ordering=ordering,
            allowed_fields=(
                "name",
                "slug",
                "created_at",
                "updated_at",
            ),
            default="name",
        )


class MediaAssetRepository(BaseRepository[MediaAsset]):
    model = MediaAsset

    @classmethod
    def queryset(cls) -> QuerySet[MediaAsset]:
        return MediaAsset.objects.select_related(
            "folder",
            "uploaded_by",
            "created_by",
            "updated_by",
        ).prefetch_related(
            "usages",
        )

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        media_type: str | None = None,
        folder_id: str | None = None,
        is_public: bool | None = None,
        ordering: str | None = None,
    ) -> QuerySet[MediaAsset]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "title",
                "original_name",
                "alt_text",
                "caption",
                "description",
                "mime_type",
                "extension",
            ),
        )

        if media_type:
            queryset = queryset.filter(
                media_type=media_type,
            )

        if folder_id:
            queryset = queryset.filter(
                folder_id=folder_id,
            )

        if is_public is not None:
            queryset = queryset.filter(
                is_public=is_public,
            )

        return apply_ordering(
            queryset,
            ordering=ordering,
            allowed_fields=(
                "title",
                "original_name",
                "media_type",
                "size",
                "created_at",
                "updated_at",
            ),
            default="-created_at",
        )


class MediaUsageRepository(BaseRepository[MediaUsage]):
    model = MediaUsage

    @classmethod
    def queryset(cls) -> QuerySet[MediaUsage]:
        return MediaUsage.objects.select_related(
            "asset",
            "created_by",
            "updated_by",
        )
