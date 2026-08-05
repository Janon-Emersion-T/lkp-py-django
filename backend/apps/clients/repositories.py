from django.db.models import QuerySet

from apps.common.query import (
    apply_ordering,
    apply_search,
)
from apps.common.repositories import BaseRepository

from .models import Client


class ClientRepository(BaseRepository[Client]):
    model = Client

    @classmethod
    def queryset(cls) -> QuerySet[Client]:
        return Client.objects.select_related(
            "source_lead",
            "created_by",
            "updated_by",
        ).prefetch_related(
            "contacts",
            "websites",
        )

    @classmethod
    def search(
        cls,
        *,
        search: str | None = None,
        status: str | None = None,
        client_type: str | None = None,
        country: str | None = None,
        industry: str | None = None,
        ordering: str | None = None,
    ) -> QuerySet[Client]:
        queryset = cls.queryset()

        queryset = apply_search(
            queryset,
            search=search,
            fields=(
                "company_name",
                "legal_name",
                "client_code",
                "email",
                "phone",
                "whatsapp",
                "country",
                "industry",
            ),
        )

        if status:
            queryset = queryset.filter(status=status)

        if client_type:
            queryset = queryset.filter(
                client_type=client_type,
            )

        if country:
            queryset = queryset.filter(
                country__iexact=country,
            )

        if industry:
            queryset = queryset.filter(
                industry__iexact=industry,
            )

        return apply_ordering(
            queryset,
            ordering=ordering,
            allowed_fields=(
                "company_name",
                "client_code",
                "created_at",
                "updated_at",
                "country",
                "industry",
            ),
            default="company_name",
        )
