from django.db.models import Count, Q
from django.utils import timezone

from .models import (
    ContactEnquiry,
    EnquiryNote,
    QuoteEnquiry,
)


class ContactEnquiryRepository:
    ALLOWED_ORDERING_FIELDS = {
        "reference_code",
        "name",
        "status",
        "priority",
        "submitted_at",
        "next_follow_up_at",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return ContactEnquiry.objects.select_related(
            "assigned_to",
            "client",
            "lead",
        ).prefetch_related(
            "notes",
            "notes__author",
        )

    @classmethod
    def find_by_id(cls, enquiry_id):
        return cls.queryset().filter(
            pk=enquiry_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        status=None,
        priority=None,
        source=None,
        assigned_to_id=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(reference_code__icontains=search)
                | Q(name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
                | Q(company_name__icontains=search)
                | Q(subject__icontains=search)
                | Q(message__icontains=search)
            )

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(
                priority=priority,
            )

        if source:
            queryset = queryset.filter(source=source)

        if assigned_to_id:
            queryset = queryset.filter(
                assigned_to_id=assigned_to_id,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset


class QuoteEnquiryRepository:
    ALLOWED_ORDERING_FIELDS = {
        "reference_code",
        "name",
        "company_name",
        "country",
        "status",
        "priority",
        "budget_min",
        "budget_max",
        "submitted_at",
        "next_follow_up_at",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return QuoteEnquiry.objects.select_related(
            "assigned_to",
            "client",
            "lead",
            "quotation",
            "preferred_package",
        ).prefetch_related(
            "service_links",
            "service_links__service",
            "notes",
            "notes__author",
        )

    @classmethod
    def find_by_id(cls, enquiry_id):
        return cls.queryset().filter(
            pk=enquiry_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        status=None,
        priority=None,
        source=None,
        country=None,
        assigned_to_id=None,
        service_id=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(reference_code__icontains=search)
                | Q(name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
                | Q(company_name__icontains=search)
                | Q(project_title__icontains=search)
                | Q(project_description__icontains=search)
            )

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(
                priority=priority,
            )

        if source:
            queryset = queryset.filter(source=source)

        if country:
            queryset = queryset.filter(
                country__iexact=country,
            )

        if assigned_to_id:
            queryset = queryset.filter(
                assigned_to_id=assigned_to_id,
            )

        if service_id:
            queryset = queryset.filter(
                service_links__service_id=service_id,
                service_links__is_deleted=False,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset.distinct()


class EnquiryNoteRepository:
    @staticmethod
    def for_contact_enquiry(enquiry_id):
        return EnquiryNote.objects.select_related(
            "author",
        ).filter(
            contact_enquiry_id=enquiry_id,
        )

    @staticmethod
    def for_quote_enquiry(enquiry_id):
        return EnquiryNote.objects.select_related(
            "author",
        ).filter(
            quote_enquiry_id=enquiry_id,
        )



class EnquiryDashboardRepository:
    @staticmethod
    def statistics():
        now = timezone.now()

        contact_queryset = ContactEnquiry.objects.all()
        quote_queryset = QuoteEnquiry.objects.all()

        active_statuses = [
            "new",
            "assigned",
            "contacted",
            "qualified",
            "proposal_sent",
        ]

        contact_by_status = {
            item["status"]: item["total"]
            for item in (
                contact_queryset.values(
                    "status"
                ).annotate(
                    total=Count("id")
                )
            )
        }

        quote_by_status = {
            item["status"]: item["total"]
            for item in (
                quote_queryset.values(
                    "status"
                ).annotate(
                    total=Count("id")
                )
            )
        }

        contact_by_source = {
            item["source"]: item["total"]
            for item in (
                contact_queryset.values(
                    "source"
                ).annotate(
                    total=Count("id")
                )
            )
        }

        quote_by_source = {
            item["source"]: item["total"]
            for item in (
                quote_queryset.values(
                    "source"
                ).annotate(
                    total=Count("id")
                )
            )
        }

        return {
            "total_contact_enquiries": (
                contact_queryset.count()
            ),
            "total_quote_enquiries": (
                quote_queryset.count()
            ),
            "new_contact_enquiries": (
                contact_queryset.filter(
                    status="new",
                ).count()
            ),
            "new_quote_enquiries": (
                quote_queryset.filter(
                    status="new",
                ).count()
            ),
            "active_contact_enquiries": (
                contact_queryset.filter(
                    status__in=active_statuses,
                ).count()
            ),
            "active_quote_enquiries": (
                quote_queryset.filter(
                    status__in=active_statuses,
                ).count()
            ),
            "won_contact_enquiries": (
                contact_queryset.filter(
                    status="won",
                ).count()
            ),
            "won_quote_enquiries": (
                quote_queryset.filter(
                    status="won",
                ).count()
            ),
            "lost_contact_enquiries": (
                contact_queryset.filter(
                    status="lost",
                ).count()
            ),
            "lost_quote_enquiries": (
                quote_queryset.filter(
                    status="lost",
                ).count()
            ),
            "urgent_contact_enquiries": (
                contact_queryset.filter(
                    priority="urgent",
                    status__in=active_statuses,
                ).count()
            ),
            "urgent_quote_enquiries": (
                quote_queryset.filter(
                    priority="urgent",
                    status__in=active_statuses,
                ).count()
            ),
            "overdue_contact_follow_ups": (
                contact_queryset.filter(
                    next_follow_up_at__lt=now,
                    status__in=active_statuses,
                ).count()
            ),
            "overdue_quote_follow_ups": (
                quote_queryset.filter(
                    next_follow_up_at__lt=now,
                    status__in=active_statuses,
                ).count()
            ),
            "contact_enquiries_by_status": (
                contact_by_status
            ),
            "quote_enquiries_by_status": (
                quote_by_status
            ),
            "contact_enquiries_by_source": (
                contact_by_source
            ),
            "quote_enquiries_by_source": (
                quote_by_source
            ),
        }
