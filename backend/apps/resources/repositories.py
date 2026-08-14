from django.db.models import Q
from django.utils import timezone

from .models import (
    Resource,
    ResourceStatus,
)


class ResourceRepository:
    ALLOWED_ORDERING_FIELDS = {
        "title",
        "resource_type",
        "sort_order",
        "download_count",
        "published_at",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return Resource.objects.select_related(
            "seo",
        )

    @classmethod
    def find_by_id(cls, resource_id):
        return cls.queryset().filter(
            pk=resource_id,
        ).first()

    @classmethod
    def find_by_slug(cls, slug):
        return cls.queryset().filter(
            slug=slug,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        resource_type=None,
        status=None,
        is_featured=None,
        is_active=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(slug__icontains=search)
                | Q(excerpt__icontains=search)
            )

        if resource_type:
            queryset = queryset.filter(
                resource_type=resource_type,
            )

        if status:
            queryset = queryset.filter(
                status=status,
            )

        if is_featured is not None:
            queryset = queryset.filter(
                is_featured=is_featured,
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}"
                    if descending
                    else field
                )

        return queryset

    @classmethod
    def public_resources(
        cls,
        *,
        resource_type=None,
        featured_only=False,
    ):
        queryset = cls.queryset().filter(
            status=ResourceStatus.PUBLISHED,
            is_active=True,
            published_at__isnull=False,
            published_at__lte=timezone.now(),
        ).filter(
            Q(scheduled_for__isnull=True)
            | Q(scheduled_for__lte=timezone.now())
        )

        if resource_type:
            queryset = queryset.filter(
                resource_type=resource_type,
            )

        if featured_only:
            queryset = queryset.filter(
                is_featured=True,
            )

        return queryset.order_by(
            "sort_order",
            "-published_at",
            "-created_at",
        )

    @staticmethod
    def create(**values):
        return Resource.objects.create(**values)

    @staticmethod
    def update(resource, **values):
        for field, value in values.items():
            setattr(resource, field, value)

        resource.save()

        return resource
