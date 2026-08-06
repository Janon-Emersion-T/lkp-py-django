from django.db.models import Q

from .models import Testimonial, TestimonialStatus


class TestimonialRepository:
    ALLOWED_ORDERING_FIELDS = {
        "author_name",
        "company_name",
        "rating",
        "sort_order",
        "published_at",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return Testimonial.objects.select_related(
            "client",
            "project",
            "author_image",
            "company_logo",
        )

    @classmethod
    def find_by_id(cls, testimonial_id):
        return cls.queryset().filter(
            pk=testimonial_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        status=None,
        source=None,
        rating=None,
        is_featured=None,
        is_verified=None,
        is_active=None,
        client_id=None,
        project_id=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(author_name__icontains=search)
                | Q(author_position__icontains=search)
                | Q(company_name__icontains=search)
                | Q(content__icontains=search)
                | Q(short_content__icontains=search)
            )

        if status:
            queryset = queryset.filter(status=status)

        if source:
            queryset = queryset.filter(source=source)

        if rating is not None:
            queryset = queryset.filter(rating=rating)

        if is_featured is not None:
            queryset = queryset.filter(
                is_featured=is_featured,
            )

        if is_verified is not None:
            queryset = queryset.filter(
                is_verified=is_verified,
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        if client_id:
            queryset = queryset.filter(client_id=client_id)

        if project_id:
            queryset = queryset.filter(project_id=project_id)

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset

    @classmethod
    def public_queryset(cls):
        from django.utils import timezone

        return cls.queryset().filter(
            status=TestimonialStatus.PUBLISHED,
            is_active=True,
            published_at__isnull=False,
            published_at__lte=timezone.now(),
        )

    @staticmethod
    def create(**values):
        return Testimonial.objects.create(**values)

    @staticmethod
    def update(testimonial, **values):
        for field, value in values.items():
            setattr(testimonial, field, value)

        testimonial.save()

        return testimonial

    @staticmethod
    def soft_delete(testimonial):
        testimonial.delete()

        return testimonial
