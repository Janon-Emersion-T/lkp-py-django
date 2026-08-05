from django.db.models import QuerySet
from django.utils import timezone

from apps.common.query import (
    apply_ordering,
    apply_search,
)
from apps.common.repositories import BaseRepository

from .models import Lead, LeadStatus


class LeadRepository(BaseRepository[Lead]):
    model = Lead

    @classmethod
    def queryset(cls) -> QuerySet[Lead]:
        return (
            Lead.objects.select_related(
                "assigned_to",
                "created_by",
                "updated_by",
            )
            .all()
        )

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        status: str | None = None,
        source: str | None = None,
        assigned_to_id: int | None = None,
        country: str | None = None,
        ordering: str | None = None,
    ) -> QuerySet[Lead]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "name",
                "company",
                "email",
                "phone",
                "whatsapp",
                "country",
            ),
        )

        if status:
            queryset = queryset.filter(status=status)

        if source:
            queryset = queryset.filter(source=source)

        if assigned_to_id:
            queryset = queryset.filter(
                assigned_to_id=assigned_to_id,
            )

        if country:
            queryset = queryset.filter(
                country__iexact=country,
            )

        return apply_ordering(
            queryset,
            ordering=ordering,
            allowed_fields=(
                "created_at",
                "updated_at",
                "name",
                "company",
                "lead_score",
                "estimated_value",
                "next_follow_up_at",
            ),
            default="-created_at",
        )

    @classmethod
    def new_leads(cls) -> QuerySet[Lead]:
        return cls.queryset().filter(
            status=LeadStatus.NEW,
        )

    @classmethod
    def overdue_follow_ups(cls) -> QuerySet[Lead]:
        return cls.queryset().filter(
            next_follow_up_at__lt=timezone.now(),
        ).exclude(
            status__in=(
                LeadStatus.WON,
                LeadStatus.LOST,
                LeadStatus.SPAM,
            ),
        )
