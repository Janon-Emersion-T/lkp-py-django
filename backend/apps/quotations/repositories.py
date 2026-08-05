from django.db.models import QuerySet
from django.utils import timezone

from apps.common.query import (
    apply_ordering,
    apply_search,
)
from apps.common.repositories import BaseRepository

from .models import Quotation, QuotationStatus


class QuotationRepository(BaseRepository[Quotation]):
    model = Quotation

    @classmethod
    def queryset(cls) -> QuerySet[Quotation]:
        return (
            Quotation.objects.select_related(
                "client",
                "lead",
                "duplicated_from",
                "created_by",
                "updated_by",
            )
            .prefetch_related(
                "items",
                "recipients",
                "events",
            )
        )

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        status: str | None = None,
        client_id: str | None = None,
        currency: str | None = None,
        ordering: str | None = None,
    ) -> QuerySet[Quotation]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "quotation_number",
                "title",
                "subject",
                "client__company_name",
                "client__client_code",
            ),
        )

        if status:
            queryset = queryset.filter(status=status)

        if client_id:
            queryset = queryset.filter(client_id=client_id)

        if currency:
            queryset = queryset.filter(
                currency__iexact=currency,
            )

        return apply_ordering(
            queryset,
            ordering=ordering,
            allowed_fields=(
                "quotation_number",
                "issue_date",
                "expiry_date",
                "created_at",
                "updated_at",
                "total_amount",
                "status",
            ),
            default="-created_at",
        )

    @classmethod
    def pending(cls) -> QuerySet[Quotation]:
        return cls.queryset().filter(
            status__in=(
                QuotationStatus.DRAFT,
                QuotationStatus.SENT,
                QuotationStatus.VIEWED,
            ),
        )

    @classmethod
    def expired_candidates(cls) -> QuerySet[Quotation]:
        return cls.queryset().filter(
            expiry_date__lt=timezone.localdate(),
            status__in=(
                QuotationStatus.DRAFT,
                QuotationStatus.SENT,
                QuotationStatus.VIEWED,
            ),
        )
