from django.db.models import Q

from .models import (
    CampaignRecipient,
    CampaignRecipientStatus,
    CampaignStatus,
    NewsletterCampaign,
    NewsletterList,
    NewsletterTag,
    Subscriber,
    SubscriberStatus,
)


class NewsletterListRepository:
    @staticmethod
    def queryset():
        return NewsletterList.objects.all()

    @classmethod
    def find_by_id(cls, list_id):
        return cls.queryset().filter(
            pk=list_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        is_public=None,
        is_active=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(slug__icontains=search)
                | Q(description__icontains=search)
            )

        if is_public is not None:
            queryset = queryset.filter(
                is_public=is_public,
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        return queryset


class NewsletterTagRepository:
    @staticmethod
    def queryset():
        return NewsletterTag.objects.all()

    @classmethod
    def find_by_id(cls, tag_id):
        return cls.queryset().filter(
            pk=tag_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        is_active=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(slug__icontains=search)
                | Q(description__icontains=search)
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        return queryset


class SubscriberRepository:
    ALLOWED_ORDERING_FIELDS = {
        "email",
        "first_name",
        "last_name",
        "company_name",
        "country",
        "status",
        "subscribed_at",
        "confirmed_at",
        "unsubscribed_at",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return Subscriber.objects.prefetch_related(
            "list_memberships",
            "list_memberships__newsletter_list",
            "tag_assignments",
            "tag_assignments__tag",
        )

    @classmethod
    def find_by_id(cls, subscriber_id):
        return cls.queryset().filter(
            pk=subscriber_id,
        ).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.queryset().filter(
            email__iexact=email.strip(),
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        status=None,
        source=None,
        country=None,
        language=None,
        list_id=None,
        tag_id=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(email__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(company_name__icontains=search)
                | Q(phone__icontains=search)
            )

        if status:
            queryset = queryset.filter(status=status)

        if source:
            queryset = queryset.filter(source=source)

        if country:
            queryset = queryset.filter(
                country__iexact=country,
            )

        if language:
            queryset = queryset.filter(
                language__iexact=language,
            )

        if list_id:
            queryset = queryset.filter(
                list_memberships__newsletter_list_id=(
                    list_id
                ),
                list_memberships__is_deleted=False,
            )

        if tag_id:
            queryset = queryset.filter(
                tag_assignments__tag_id=tag_id,
                tag_assignments__is_deleted=False,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset.distinct()

    @classmethod
    def active_recipients(cls):
        return cls.queryset().filter(
            status=SubscriberStatus.ACTIVE,
            consent_given=True,
            confirmed_at__isnull=False,
        )



class NewsletterCampaignRepository:
    ALLOWED_ORDERING_FIELDS = {
        "name",
        "subject",
        "status",
        "scheduled_for",
        "sent_at",
        "recipient_count",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return NewsletterCampaign.objects.prefetch_related(
            "list_targets",
            "list_targets__newsletter_list",
            "tag_targets",
            "tag_targets__tag",
        )

    @classmethod
    def find_by_id(cls, campaign_id):
        return cls.queryset().filter(
            pk=campaign_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        status=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(subject__icontains=search)
                | Q(preview_text__icontains=search)
            )

        if status:
            queryset = queryset.filter(
                status=status,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset


class CampaignRecipientRepository:
    @staticmethod
    def queryset():
        return CampaignRecipient.objects.select_related(
            "campaign",
            "subscriber",
        )

    @classmethod
    def for_campaign(
        cls,
        campaign_id,
        *,
        status=None,
    ):
        queryset = cls.queryset().filter(
            campaign_id=campaign_id,
        )

        if status:
            queryset = queryset.filter(
                status=status,
            )

        return queryset


class NewsletterDashboardRepository:
    @staticmethod
    def statistics():
        return {
            "total_subscribers": (
                Subscriber.objects.count()
            ),
            "active_subscribers": (
                Subscriber.objects.filter(
                    status=SubscriberStatus.ACTIVE,
                    consent_given=True,
                    confirmed_at__isnull=False,
                ).count()
            ),
            "pending_subscribers": (
                Subscriber.objects.filter(
                    status=SubscriberStatus.PENDING,
                ).count()
            ),
            "unsubscribed_subscribers": (
                Subscriber.objects.filter(
                    status=SubscriberStatus.UNSUBSCRIBED,
                ).count()
            ),
            "bounced_subscribers": (
                Subscriber.objects.filter(
                    status=SubscriberStatus.BOUNCED,
                ).count()
            ),
            "total_campaigns": (
                NewsletterCampaign.objects.count()
            ),
            "draft_campaigns": (
                NewsletterCampaign.objects.filter(
                    status=CampaignStatus.DRAFT,
                ).count()
            ),
            "scheduled_campaigns": (
                NewsletterCampaign.objects.filter(
                    status=CampaignStatus.SCHEDULED,
                ).count()
            ),
            "sent_campaigns": (
                NewsletterCampaign.objects.filter(
                    status=CampaignStatus.SENT,
                ).count()
            ),
            "total_emails_sent": (
                CampaignRecipient.objects.filter(
                    status__in=[
                        CampaignRecipientStatus.SENT,
                        CampaignRecipientStatus.DELIVERED,
                        CampaignRecipientStatus.OPENED,
                        CampaignRecipientStatus.CLICKED,
                    ],
                ).count()
            ),
            "total_delivered": (
                CampaignRecipient.objects.filter(
                    status__in=[
                        CampaignRecipientStatus.DELIVERED,
                        CampaignRecipientStatus.OPENED,
                        CampaignRecipientStatus.CLICKED,
                    ],
                ).count()
            ),
            "total_opened": (
                CampaignRecipient.objects.filter(
                    opened_at__isnull=False,
                ).count()
            ),
            "total_clicked": (
                CampaignRecipient.objects.filter(
                    clicked_at__isnull=False,
                ).count()
            ),
        }
