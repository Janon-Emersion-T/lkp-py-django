from .models import Subscriber, SubscriberStatus, SubscriptionSource
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import User

from .models import (
    NewsletterList,
    NewsletterTag,
    Subscriber,
    SubscriberListMembership,
    SubscriberStatus,
    SubscriberTagAssignment,
    SubscriptionSource,
)
from .repositories import SubscriberRepository
from .services import SubscriberService


class RequestStub:
    def __init__(self, user):
        self.auth = user
        self.user = user
        self.META = {}
        self.headers = {}


class NewsletterFixtureMixin:
    def create_segments(self):
        newsletter_list = NewsletterList.objects.create(
            name="Business Insights",
            slug="business-insights",
            is_default=True,
            is_public=True,
        )

        tag = NewsletterTag.objects.create(
            name="Web Development",
            slug="web-development",
        )

        return newsletter_list, tag


class NewsletterModelTests(
    NewsletterFixtureMixin,
    TestCase,
):
    def test_subscriber_normalizes_email(self):
        subscriber = Subscriber.objects.create(
            email="  TEST@Example.COM  ",
            consent_given=True,
        )

        self.assertEqual(
            subscriber.email,
            "test@example.com",
        )

    def test_subscriber_generates_tokens(self):
        subscriber = Subscriber.objects.create(
            email="tokens@example.com",
        )

        self.assertTrue(
            subscriber.confirmation_token
        )
        self.assertTrue(
            subscriber.unsubscribe_token
        )
        self.assertNotEqual(
            subscriber.confirmation_token,
            subscriber.unsubscribe_token,
        )

    def test_active_confirmed_subscriber_can_receive(self):
        subscriber = Subscriber.objects.create(
            email="active@example.com",
            status=SubscriberStatus.ACTIVE,
            consent_given=True,
            confirmed_at=timezone.now(),
        )

        self.assertTrue(
            subscriber.can_receive_email
        )

    def test_unconfirmed_subscriber_cannot_receive(self):
        subscriber = Subscriber.objects.create(
            email="pending@example.com",
            status=SubscriberStatus.ACTIVE,
            consent_given=True,
        )

        self.assertFalse(
            subscriber.can_receive_email
        )

    def test_subscriber_full_name(self):
        subscriber = Subscriber.objects.create(
            email="person@example.com",
            first_name="Example",
            last_name="Person",
        )

        self.assertEqual(
            subscriber.full_name,
            "Example Person",
        )


class NewsletterRepositoryTests(
    NewsletterFixtureMixin,
    TestCase,
):
    def setUp(self):
        self.newsletter_list, self.tag = (
            self.create_segments()
        )

        self.subscriber = Subscriber.objects.create(
            email="repository@example.com",
            first_name="Repository",
            company_name="LKProfessionals",
            country="Sri Lanka",
            language="en",
            source=SubscriptionSource.WEBSITE,
            status=SubscriberStatus.ACTIVE,
            consent_given=True,
            confirmed_at=timezone.now(),
        )

        SubscriberListMembership.objects.create(
            subscriber=self.subscriber,
            newsletter_list=self.newsletter_list,
        )

        SubscriberTagAssignment.objects.create(
            subscriber=self.subscriber,
            tag=self.tag,
        )

    def test_search_subscriber(self):
        queryset = SubscriberRepository.search(
            search="Repository",
        )

        self.assertEqual(queryset.count(), 1)

    def test_filter_by_list_and_tag(self):
        queryset = SubscriberRepository.search(
            list_id=self.newsletter_list.id,
            tag_id=self.tag.id,
        )

        self.assertEqual(queryset.count(), 1)

    def test_active_recipients(self):
        queryset = (
            SubscriberRepository.active_recipients()
        )

        self.assertEqual(queryset.count(), 1)


class NewsletterServiceTests(
    NewsletterFixtureMixin,
    TestCase,
):
    def setUp(self):
        self.user = User.objects.create_user(
            username="newsletter_admin",
            email="newsletter-admin@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.user)

        self.newsletter_list, self.tag = (
            self.create_segments()
        )

    def create_subscriber(self):
        return SubscriberService.create_subscriber(
            request=self.request,
            values={
                "email": "service@example.com",
                "first_name": "Service",
                "source": SubscriptionSource.MANUAL,
                "consent_given": True,
            },
            newsletter_lists=[
                self.newsletter_list,
            ],
            tags=[self.tag],
        )

    def test_create_subscriber_with_segments(self):
        subscriber = self.create_subscriber()

        self.assertEqual(
            subscriber.list_memberships.count(),
            1,
        )
        self.assertEqual(
            subscriber.tag_assignments.count(),
            1,
        )

    def test_confirm_subscription(self):
        subscriber = self.create_subscriber()

        subscriber = (
            SubscriberService.confirm_subscription(
                request=self.request,
                subscriber=subscriber,
            )
        )

        self.assertEqual(
            subscriber.status,
            SubscriberStatus.ACTIVE,
        )
        self.assertIsNotNone(
            subscriber.confirmed_at,
        )
        self.assertTrue(
            subscriber.can_receive_email
        )

    def test_unsubscribe(self):
        subscriber = self.create_subscriber()

        subscriber = SubscriberService.unsubscribe(
            request=self.request,
            subscriber=subscriber,
        )

        self.assertEqual(
            subscriber.status,
            SubscriberStatus.UNSUBSCRIBED,
        )
        self.assertIsNotNone(
            subscriber.unsubscribed_at,
        )

    def test_resubscribe(self):
        subscriber = self.create_subscriber()

        SubscriberService.unsubscribe(
            request=self.request,
            subscriber=subscriber,
        )

        subscriber = SubscriberService.resubscribe(
            request=self.request,
            subscriber=subscriber,
        )

        self.assertEqual(
            subscriber.status,
            SubscriberStatus.ACTIVE,
        )
        self.assertIsNone(
            subscriber.unsubscribed_at,
        )

    def test_update_replaces_segments(self):
        subscriber = self.create_subscriber()

        second_list = NewsletterList.objects.create(
            name="SEO Updates",
            slug="seo-updates",
        )

        second_tag = NewsletterTag.objects.create(
            name="SEO",
            slug="seo",
        )

        subscriber = SubscriberService.update_subscriber(
            request=self.request,
            subscriber=subscriber,
            values={
                "email": subscriber.email,
                "first_name": "Updated",
            },
            newsletter_lists=[second_list],
            tags=[second_tag],
        )

        self.assertEqual(
            subscriber.first_name,
            "Updated",
        )
        self.assertEqual(
            subscriber.list_memberships.count(),
            1,
        )
        self.assertEqual(
            subscriber.list_memberships.first()
            .newsletter_list,
            second_list,
        )
        self.assertEqual(
            subscriber.tag_assignments.first().tag,
            second_tag,
        )



from datetime import timedelta

from .models import (
    CampaignRecipient,
    CampaignRecipientStatus,
    CampaignStatus,
    NewsletterCampaign,
)
from .repositories import (
    NewsletterCampaignRepository,
    NewsletterDashboardRepository,
)
from .services import NewsletterCampaignService


class NewsletterCampaignTests(
    NewsletterFixtureMixin,
    TestCase,
):
    def setUp(self):
        self.user = User.objects.create_user(
            username="campaign_admin",
            email="campaign-admin@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.user)

        self.newsletter_list, self.tag = (
            self.create_segments()
        )

        self.subscriber = Subscriber.objects.create(
            email="campaign-recipient@example.com",
            first_name="Campaign",
            last_name="Recipient",
            status=SubscriberStatus.ACTIVE,
            consent_given=True,
            confirmed_at=timezone.now(),
        )

        SubscriberListMembership.objects.create(
            subscriber=self.subscriber,
            newsletter_list=self.newsletter_list,
        )

        SubscriberTagAssignment.objects.create(
            subscriber=self.subscriber,
            tag=self.tag,
        )

    def create_campaign(self):
        return (
            NewsletterCampaignService.create_campaign(
                request=self.request,
                values={
                    "name": "August Technology Update",
                    "subject": "Technology insights",
                    "from_email": "info@example.com",
                    "html_content": (
                        "<p>Newsletter content</p>"
                    ),
                },
                newsletter_lists=[
                    self.newsletter_list,
                ],
                tags=[self.tag],
            )
        )

    def test_create_campaign_with_targets(self):
        campaign = self.create_campaign()

        self.assertEqual(
            campaign.list_targets.count(),
            1,
        )
        self.assertEqual(
            campaign.tag_targets.count(),
            1,
        )

    def test_schedule_campaign(self):
        campaign = self.create_campaign()

        scheduled_for = (
            timezone.now() + timedelta(days=1)
        )

        campaign = (
            NewsletterCampaignService.schedule_campaign(
                request=self.request,
                campaign=campaign,
                scheduled_for=scheduled_for,
            )
        )

        self.assertEqual(
            campaign.status,
            CampaignStatus.SCHEDULED,
        )
        self.assertEqual(
            campaign.scheduled_for,
            scheduled_for,
        )

    def test_schedule_requires_future_datetime(self):
        campaign = self.create_campaign()

        with self.assertRaises(ValueError):
            NewsletterCampaignService.schedule_campaign(
                request=self.request,
                campaign=campaign,
                scheduled_for=(
                    timezone.now()
                    - timedelta(minutes=1)
                ),
            )

    def test_prepare_campaign_recipients(self):
        campaign = self.create_campaign()

        campaign = (
            NewsletterCampaignService
            .prepare_recipients(
                request=self.request,
                campaign=campaign,
            )
        )

        self.assertEqual(
            campaign.status,
            CampaignStatus.QUEUED,
        )
        self.assertEqual(
            campaign.recipient_count,
            1,
        )
        self.assertEqual(
            campaign.recipients.count(),
            1,
        )

    def test_unconfirmed_subscriber_is_excluded(self):
        Subscriber.objects.create(
            email="excluded@example.com",
            status=SubscriberStatus.ACTIVE,
            consent_given=True,
        )

        campaign = self.create_campaign()

        campaign = (
            NewsletterCampaignService
            .prepare_recipients(
                request=self.request,
                campaign=campaign,
            )
        )

        self.assertEqual(
            campaign.recipient_count,
            1,
        )

    def test_mark_campaign_sent(self):
        campaign = self.create_campaign()

        campaign = (
            NewsletterCampaignService
            .prepare_recipients(
                request=self.request,
                campaign=campaign,
            )
        )

        campaign = (
            NewsletterCampaignService
            .mark_campaign_sent(
                request=self.request,
                campaign=campaign,
            )
        )

        self.assertEqual(
            campaign.status,
            CampaignStatus.SENT,
        )
        self.assertEqual(
            campaign.sent_count,
            1,
        )

        recipient = campaign.recipients.first()

        self.assertEqual(
            recipient.status,
            CampaignRecipientStatus.SENT,
        )
        self.assertIsNotNone(recipient.sent_at)

    def test_campaign_open_and_click_rates(self):
        campaign = NewsletterCampaign.objects.create(
            name="Metrics Campaign",
            subject="Metrics",
            from_email="info@example.com",
            delivered_count=10,
            opened_count=5,
            clicked_count=2,
        )

        self.assertEqual(campaign.open_rate, 50.0)
        self.assertEqual(campaign.click_rate, 20.0)

    def test_refresh_campaign_statistics(self):
        campaign = self.create_campaign()

        CampaignRecipient.objects.create(
            campaign=campaign,
            subscriber=self.subscriber,
            email=self.subscriber.email,
            status=CampaignRecipientStatus.CLICKED,
            sent_at=timezone.now(),
            delivered_at=timezone.now(),
            opened_at=timezone.now(),
            clicked_at=timezone.now(),
        )

        campaign = (
            NewsletterCampaignService
            .refresh_statistics(campaign)
        )

        self.assertEqual(
            campaign.recipient_count,
            1,
        )
        self.assertEqual(
            campaign.delivered_count,
            1,
        )
        self.assertEqual(
            campaign.opened_count,
            1,
        )
        self.assertEqual(
            campaign.clicked_count,
            1,
        )

    def test_campaign_repository_search(self):
        campaign = self.create_campaign()

        queryset = (
            NewsletterCampaignRepository.search(
                search="August",
                status=CampaignStatus.DRAFT,
            )
        )

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(
            queryset.first().id,
            campaign.id,
        )

    def test_newsletter_dashboard(self):
        self.create_campaign()

        stats = (
            NewsletterDashboardRepository.statistics()
        )

        self.assertEqual(
            stats["total_subscribers"],
            1,
        )
        self.assertEqual(
            stats["active_subscribers"],
            1,
        )
        self.assertEqual(
            stats["total_campaigns"],
            1,
        )
        self.assertEqual(
            stats["draft_campaigns"],
            1,
        )


class PublicNewsletterSubscriptionApiTests(TestCase):
    def setUp(self):
        self.url = "/api/v1/newsletter/subscribe"

    def test_public_user_can_subscribe(self):
        response = self.client.post(
            self.url,
            data={
                "email": "newsletter@example.com",
                "consent_given": True,
                "source_reference": "website-footer",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

        subscriber = Subscriber.objects.get(
            email="newsletter@example.com"
        )

        self.assertEqual(
            subscriber.status,
            SubscriberStatus.ACTIVE,
        )
        self.assertEqual(
            subscriber.source,
            SubscriptionSource.WEBSITE,
        )
        self.assertTrue(subscriber.consent_given)
        self.assertIsNotNone(subscriber.confirmed_at)

    def test_existing_subscriber_request_is_idempotent(self):
        Subscriber.objects.create(
            email="existing@example.com",
            status=SubscriberStatus.ACTIVE,
            source=SubscriptionSource.WEBSITE,
            consent_given=True,
        )

        response = self.client.post(
            self.url,
            data={
                "email": "existing@example.com",
                "consent_given": True,
                "source_reference": "website-footer",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Subscriber.objects.filter(
                email="existing@example.com"
            ).count(),
            1,
        )

    def test_invalid_email_is_rejected(self):
        response = self.client.post(
            self.url,
            data={
                "email": "not-an-email",
                "consent_given": True,
                "source_reference": "website-footer",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_subscription_requires_consent(self):
        response = self.client.post(
            self.url,
            data={
                "email": "no-consent@example.com",
                "consent_given": False,
                "source_reference": "website-footer",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
