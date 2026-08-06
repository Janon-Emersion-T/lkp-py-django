from django.db import transaction
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    CampaignListTarget,
    CampaignRecipient,
    CampaignRecipientStatus,
    CampaignStatus,
    CampaignTagTarget,
    NewsletterCampaign,
    Subscriber,
    SubscriberListMembership,
    SubscriberStatus,
    SubscriberTagAssignment,
)


class SubscriberService:
    @staticmethod
    def audit_snapshot(subscriber):
        return {
            "id": str(subscriber.id),
            "email": subscriber.email,
            "first_name": subscriber.first_name,
            "last_name": subscriber.last_name,
            "company_name": subscriber.company_name,
            "country": subscriber.country,
            "language": subscriber.language,
            "status": subscriber.status,
            "source": subscriber.source,
            "consent_given": subscriber.consent_given,
            "subscribed_at": (
                subscriber.subscribed_at.isoformat()
                if subscriber.subscribed_at
                else None
            ),
            "confirmed_at": (
                subscriber.confirmed_at.isoformat()
                if subscriber.confirmed_at
                else None
            ),
            "unsubscribed_at": (
                subscriber.unsubscribed_at.isoformat()
                if subscriber.unsubscribed_at
                else None
            ),
        }

    @classmethod
    @transaction.atomic
    def create_subscriber(
        cls,
        *,
        request,
        values,
        newsletter_lists,
        tags,
    ):
        subscriber = Subscriber.objects.create(**values)

        for newsletter_list in newsletter_lists:
            SubscriberListMembership.objects.create(
                subscriber=subscriber,
                newsletter_list=newsletter_list,
            )

        for tag in tags:
            SubscriberTagAssignment.objects.create(
                subscriber=subscriber,
                tag=tag,
            )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="newsletter",
            message="Newsletter subscriber created.",
            target_type="newsletter.Subscriber",
            target_id=str(subscriber.pk),
            metadata={
                "after": cls.audit_snapshot(subscriber),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="create",
            module="newsletter",
            description=(
                f"Created newsletter subscriber "
                f"{subscriber.email}."
            ),
            entity_type="newsletter.Subscriber",
            entity_id=str(subscriber.pk),
        )

        return subscriber

    @classmethod
    @transaction.atomic
    def update_subscriber(
        cls,
        *,
        request,
        subscriber,
        values,
        newsletter_lists,
        tags,
    ):
        before = cls.audit_snapshot(subscriber)

        for field, value in values.items():
            setattr(subscriber, field, value)

        subscriber.save()

        SubscriberListMembership.objects.filter(
            subscriber=subscriber,
        ).delete()

        SubscriberTagAssignment.objects.filter(
            subscriber=subscriber,
        ).delete()

        for newsletter_list in newsletter_lists:
            SubscriberListMembership.objects.create(
                subscriber=subscriber,
                newsletter_list=newsletter_list,
            )

        for tag in tags:
            SubscriberTagAssignment.objects.create(
                subscriber=subscriber,
                tag=tag,
            )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="newsletter",
            message="Newsletter subscriber updated.",
            target_type="newsletter.Subscriber",
            target_id=str(subscriber.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(subscriber),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="update",
            module="newsletter",
            description=(
                f"Updated newsletter subscriber "
                f"{subscriber.email}."
            ),
            entity_type="newsletter.Subscriber",
            entity_id=str(subscriber.pk),
        )

        return subscriber

    @classmethod
    @transaction.atomic
    def confirm_subscription(
        cls,
        *,
        request,
        subscriber,
    ):
        before = cls.audit_snapshot(subscriber)

        subscriber.status = SubscriberStatus.ACTIVE
        subscriber.confirmed_at = timezone.now()
        subscriber.unsubscribed_at = None
        subscriber.save(
            update_fields=[
                "status",
                "confirmed_at",
                "unsubscribed_at",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="newsletter",
            message="Newsletter subscription confirmed.",
            target_type="newsletter.Subscriber",
            target_id=str(subscriber.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(subscriber),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="confirm",
            module="newsletter",
            description=(
                f"Confirmed subscription for "
                f"{subscriber.email}."
            ),
            entity_type="newsletter.Subscriber",
            entity_id=str(subscriber.pk),
        )

        return subscriber

    @classmethod
    @transaction.atomic
    def unsubscribe(
        cls,
        *,
        request,
        subscriber,
    ):
        before = cls.audit_snapshot(subscriber)

        subscriber.status = SubscriberStatus.UNSUBSCRIBED
        subscriber.unsubscribed_at = timezone.now()
        subscriber.save(
            update_fields=[
                "status",
                "unsubscribed_at",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="newsletter",
            message="Newsletter subscriber unsubscribed.",
            target_type="newsletter.Subscriber",
            target_id=str(subscriber.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(subscriber),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="unsubscribe",
            module="newsletter",
            description=(
                f"Unsubscribed {subscriber.email}."
            ),
            entity_type="newsletter.Subscriber",
            entity_id=str(subscriber.pk),
        )

        return subscriber

    @classmethod
    @transaction.atomic
    def resubscribe(
        cls,
        *,
        request,
        subscriber,
    ):
        before = cls.audit_snapshot(subscriber)

        subscriber.status = SubscriberStatus.ACTIVE
        subscriber.confirmed_at = (
            subscriber.confirmed_at
            or timezone.now()
        )
        subscriber.unsubscribed_at = None
        subscriber.save(
            update_fields=[
                "status",
                "confirmed_at",
                "unsubscribed_at",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="newsletter",
            message="Newsletter subscriber resubscribed.",
            target_type="newsletter.Subscriber",
            target_id=str(subscriber.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(subscriber),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="resubscribe",
            module="newsletter",
            description=(
                f"Resubscribed {subscriber.email}."
            ),
            entity_type="newsletter.Subscriber",
            entity_id=str(subscriber.pk),
        )

        return subscriber



class NewsletterCampaignService:
    @staticmethod
    def audit_snapshot(campaign):
        return {
            "id": str(campaign.id),
            "name": campaign.name,
            "subject": campaign.subject,
            "status": campaign.status,
            "scheduled_for": (
                campaign.scheduled_for.isoformat()
                if campaign.scheduled_for
                else None
            ),
            "recipient_count": campaign.recipient_count,
            "sent_count": campaign.sent_count,
            "delivered_count": campaign.delivered_count,
            "opened_count": campaign.opened_count,
            "clicked_count": campaign.clicked_count,
        }

    @classmethod
    @transaction.atomic
    def create_campaign(
        cls,
        *,
        request,
        values,
        newsletter_lists,
        tags,
    ):
        campaign = NewsletterCampaign.objects.create(
            **values,
        )

        for newsletter_list in newsletter_lists:
            CampaignListTarget.objects.create(
                campaign=campaign,
                newsletter_list=newsletter_list,
            )

        for tag in tags:
            CampaignTagTarget.objects.create(
                campaign=campaign,
                tag=tag,
            )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="newsletter",
            message="Newsletter campaign created.",
            target_type="newsletter.NewsletterCampaign",
            target_id=str(campaign.pk),
            metadata={
                "after": cls.audit_snapshot(campaign),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="create_campaign",
            module="newsletter",
            description=(
                f"Created newsletter campaign "
                f"{campaign.name}."
            ),
            entity_type="newsletter.NewsletterCampaign",
            entity_id=str(campaign.pk),
        )

        return campaign

    @classmethod
    @transaction.atomic
    def update_campaign(
        cls,
        *,
        request,
        campaign,
        values,
        newsletter_lists,
        tags,
    ):
        if campaign.status not in {
            CampaignStatus.DRAFT,
            CampaignStatus.REVIEW,
            CampaignStatus.PAUSED,
        }:
            raise ValueError(
                "Only draft, review, or paused campaigns "
                "can be edited."
            )

        before = cls.audit_snapshot(campaign)

        for field, value in values.items():
            setattr(campaign, field, value)

        campaign.save()

        CampaignListTarget.objects.filter(
            campaign=campaign,
        ).delete()

        CampaignTagTarget.objects.filter(
            campaign=campaign,
        ).delete()

        for newsletter_list in newsletter_lists:
            CampaignListTarget.objects.create(
                campaign=campaign,
                newsletter_list=newsletter_list,
            )

        for tag in tags:
            CampaignTagTarget.objects.create(
                campaign=campaign,
                tag=tag,
            )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="newsletter",
            message="Newsletter campaign updated.",
            target_type="newsletter.NewsletterCampaign",
            target_id=str(campaign.pk),
            metadata={
                "before": before,
                "after": cls.audit_snapshot(campaign),
            },
        )

        return campaign

    @classmethod
    @transaction.atomic
    def schedule_campaign(
        cls,
        *,
        request,
        campaign,
        scheduled_for,
    ):
        if scheduled_for <= timezone.now():
            raise ValueError(
                "Campaign schedule must be in the future."
            )

        if not campaign.html_content and not campaign.text_content:
            raise ValueError(
                "Campaign content is required before scheduling."
            )

        campaign.status = CampaignStatus.SCHEDULED
        campaign.scheduled_for = scheduled_for
        campaign.failure_reason = ""
        campaign.save(
            update_fields=[
                "status",
                "scheduled_for",
                "failure_reason",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="newsletter",
            message="Newsletter campaign scheduled.",
            target_type="newsletter.NewsletterCampaign",
            target_id=str(campaign.pk),
            metadata={
                "after": cls.audit_snapshot(campaign),
            },
        )

        return campaign

    @classmethod
    @transaction.atomic
    def prepare_recipients(
        cls,
        *,
        request,
        campaign,
    ):
        if campaign.status not in {
            CampaignStatus.DRAFT,
            CampaignStatus.REVIEW,
            CampaignStatus.SCHEDULED,
            CampaignStatus.PAUSED,
        }:
            raise ValueError(
                "Recipients cannot be prepared in the "
                "campaign's current status."
            )

        queryset = Subscriber.objects.filter(
            status=SubscriberStatus.ACTIVE,
            consent_given=True,
            confirmed_at__isnull=False,
        )

        list_ids = list(
            campaign.list_targets.values_list(
                "newsletter_list_id",
                flat=True,
            )
        )

        tag_ids = list(
            campaign.tag_targets.values_list(
                "tag_id",
                flat=True,
            )
        )

        if list_ids:
            queryset = queryset.filter(
                list_memberships__newsletter_list_id__in=(
                    list_ids
                ),
                list_memberships__is_deleted=False,
            )

        if tag_ids:
            queryset = queryset.filter(
                tag_assignments__tag_id__in=tag_ids,
                tag_assignments__is_deleted=False,
            )

        queryset = queryset.distinct()

        CampaignRecipient.objects.filter(
            campaign=campaign,
        ).delete()

        recipients = [
            CampaignRecipient(
                campaign=campaign,
                subscriber=subscriber,
                email=subscriber.email,
                first_name=subscriber.first_name,
                last_name=subscriber.last_name,
                status=CampaignRecipientStatus.QUEUED,
                queued_at=timezone.now(),
            )
            for subscriber in queryset
            if subscriber.can_receive_email
        ]

        CampaignRecipient.objects.bulk_create(
            recipients
        )

        campaign.status = CampaignStatus.QUEUED
        campaign.queued_at = timezone.now()
        campaign.recipient_count = len(recipients)
        campaign.queued_count = len(recipients)
        campaign.save(
            update_fields=[
                "status",
                "queued_at",
                "recipient_count",
                "queued_count",
                "updated_at",
            ]
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="newsletter",
            message="Newsletter campaign recipients prepared.",
            target_type="newsletter.NewsletterCampaign",
            target_id=str(campaign.pk),
            metadata={
                "recipient_count": len(recipients),
            },
        )

        return campaign

    @classmethod
    @transaction.atomic
    def mark_campaign_sent(
        cls,
        *,
        request,
        campaign,
    ):
        now = timezone.now()

        CampaignRecipient.objects.filter(
            campaign=campaign,
            status=CampaignRecipientStatus.QUEUED,
        ).update(
            status=CampaignRecipientStatus.SENT,
            sent_at=now,
        )

        sent_count = CampaignRecipient.objects.filter(
            campaign=campaign,
            status__in=[
                CampaignRecipientStatus.SENT,
                CampaignRecipientStatus.DELIVERED,
                CampaignRecipientStatus.OPENED,
                CampaignRecipientStatus.CLICKED,
            ],
        ).count()

        campaign.status = CampaignStatus.SENT
        campaign.sending_started_at = (
            campaign.sending_started_at or now
        )
        campaign.sent_at = now
        campaign.completed_at = now
        campaign.sent_count = sent_count
        campaign.save(
            update_fields=[
                "status",
                "sending_started_at",
                "sent_at",
                "completed_at",
                "sent_count",
                "updated_at",
            ]
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="send_campaign",
            module="newsletter",
            description=(
                f"Marked campaign {campaign.name} as sent."
            ),
            entity_type="newsletter.NewsletterCampaign",
            entity_id=str(campaign.pk),
        )

        return campaign

    @staticmethod
    def refresh_statistics(campaign):
        recipients = CampaignRecipient.objects.filter(
            campaign=campaign,
        )

        campaign.recipient_count = recipients.count()
        campaign.queued_count = recipients.filter(
            status=CampaignRecipientStatus.QUEUED,
        ).count()
        campaign.sent_count = recipients.filter(
            status__in=[
                CampaignRecipientStatus.SENT,
                CampaignRecipientStatus.DELIVERED,
                CampaignRecipientStatus.OPENED,
                CampaignRecipientStatus.CLICKED,
            ],
        ).count()
        campaign.delivered_count = recipients.filter(
            status__in=[
                CampaignRecipientStatus.DELIVERED,
                CampaignRecipientStatus.OPENED,
                CampaignRecipientStatus.CLICKED,
            ],
        ).count()
        campaign.opened_count = recipients.filter(
            opened_at__isnull=False,
        ).count()
        campaign.clicked_count = recipients.filter(
            clicked_at__isnull=False,
        ).count()
        campaign.bounced_count = recipients.filter(
            status=CampaignRecipientStatus.BOUNCED,
        ).count()
        campaign.complained_count = recipients.filter(
            status=CampaignRecipientStatus.COMPLAINED,
        ).count()
        campaign.unsubscribed_count = recipients.filter(
            status=CampaignRecipientStatus.UNSUBSCRIBED,
        ).count()
        campaign.failed_count = recipients.filter(
            status=CampaignRecipientStatus.FAILED,
        ).count()

        campaign.save(
            update_fields=[
                "recipient_count",
                "queued_count",
                "sent_count",
                "delivered_count",
                "opened_count",
                "clicked_count",
                "bounced_count",
                "complained_count",
                "unsubscribed_count",
                "failed_count",
                "updated_at",
            ]
        )

        return campaign
