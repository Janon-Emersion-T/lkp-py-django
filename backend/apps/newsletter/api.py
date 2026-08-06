from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from django.db import models, transaction
from django.utils import timezone
from django.utils.text import slugify
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema
from apps.api.exceptions import ApiHttpError
from apps.rbac.services import require_permissions

from .models import (
    NewsletterList,
    NewsletterTag,
    Subscriber,
    SubscriberListMembership,
    SubscriberStatus,
    SubscriptionSource,
)
from .repositories import (
    NewsletterListRepository,
    NewsletterTagRepository,
    SubscriberRepository,
)
from .schemas import (
    NewsletterListCreateSchema,
    PublicNewsletterSubscribeResponseSchema,
    PublicNewsletterSubscribeSchema,
    NewsletterListSchema,
    NewsletterTagCreateSchema,
    NewsletterTagSchema,
    SubscriberCreateSchema,
    SubscriberSchema,
    SubscriberUpdateSchema,
)
from .services import SubscriberService


router = Router(
    tags=["Newsletter"],
    auth=jwt_auth,
)


@router.post(
    "/subscribe",
    auth=None,
    response={
        200: PublicNewsletterSubscribeResponseSchema,
        201: PublicNewsletterSubscribeResponseSchema,
        400: ErrorSchema,
    },
)
@transaction.atomic
def public_newsletter_subscribe(
    request,
    payload: PublicNewsletterSubscribeSchema,
):
    normalized_email = payload.email.strip().lower()

    try:
        validate_email(normalized_email)
    except DjangoValidationError as exc:
        raise ApiHttpError(
            400,
            "Enter a valid email address.",
            code="invalid_newsletter_email",
        ) from exc

    if not payload.consent_given:
        raise ApiHttpError(
            400,
            "Newsletter consent is required.",
            code="newsletter_consent_required",
        )

    subscriber = Subscriber.all_objects.filter(
        email__iexact=normalized_email,
    ).first()

    now = timezone.now()

    if subscriber is None:
        subscriber = Subscriber.objects.create(
            email=normalized_email,
            status=SubscriberStatus.ACTIVE,
            source=SubscriptionSource.WEBSITE,
            source_reference=payload.source_reference,
            consent_given=True,
            consent_ip_address=request.META.get("REMOTE_ADDR"),
            consent_user_agent=request.META.get(
                "HTTP_USER_AGENT",
                "",
            ),
            subscribed_at=now,
            confirmed_at=now,
            metadata={
                "subscription_location": "website_footer",
            },
        )

        response_status = 201
        message = "You have been subscribed successfully."
    else:
        if subscriber.is_deleted:
            subscriber.is_deleted = False

        subscriber.status = SubscriberStatus.ACTIVE
        subscriber.source = SubscriptionSource.WEBSITE
        subscriber.source_reference = payload.source_reference
        subscriber.consent_given = True
        subscriber.consent_ip_address = request.META.get(
            "REMOTE_ADDR"
        )
        subscriber.consent_user_agent = request.META.get(
            "HTTP_USER_AGENT",
            "",
        )
        subscriber.subscribed_at = now
        subscriber.confirmed_at = now
        subscriber.unsubscribed_at = None

        metadata = dict(subscriber.metadata or {})
        metadata["subscription_location"] = "website_footer"
        subscriber.metadata = metadata

        subscriber.save()

        response_status = 200
        message = "Your newsletter subscription is active."

    newsletter_lists = NewsletterList.objects.filter(
        is_active=True,
        is_deleted=False,
    ).filter(
        models.Q(is_default=True)
        | models.Q(is_public=True)
    )

    for newsletter_list in newsletter_lists:
        SubscriberListMembership.objects.get_or_create(
            subscriber=subscriber,
            newsletter_list=newsletter_list,
        )

    return response_status, {
        "status": "ok",
        "message": message,
    }


def get_newsletter_list(list_id):
    newsletter_list = (
        NewsletterListRepository.find_by_id(list_id)
    )

    if newsletter_list is None:
        raise ApiHttpError(
            404,
            "Newsletter list not found.",
            code="newsletter_list_not_found",
        )

    return newsletter_list


def get_newsletter_tag(tag_id):
    tag = NewsletterTagRepository.find_by_id(tag_id)

    if tag is None:
        raise ApiHttpError(
            404,
            "Newsletter tag not found.",
            code="newsletter_tag_not_found",
        )

    return tag


def get_subscriber(subscriber_id):
    subscriber = SubscriberRepository.find_by_id(
        subscriber_id
    )

    if subscriber is None:
        raise ApiHttpError(
            404,
            "Newsletter subscriber not found.",
            code="newsletter_subscriber_not_found",
        )

    return subscriber


def resolve_lists(list_ids):
    if not list_ids:
        return []

    newsletter_lists = list(
        NewsletterList.objects.filter(
            id__in=list_ids,
        )
    )

    if len(newsletter_lists) != len(set(list_ids)):
        raise ApiHttpError(
            400,
            "One or more newsletter lists are invalid.",
            code="invalid_newsletter_lists",
        )

    return newsletter_lists


def resolve_tags(tag_ids):
    if not tag_ids:
        return []

    tags = list(
        NewsletterTag.objects.filter(
            id__in=tag_ids,
        )
    )

    if len(tags) != len(set(tag_ids)):
        raise ApiHttpError(
            400,
            "One or more newsletter tags are invalid.",
            code="invalid_newsletter_tags",
        )

    return tags


def serialize_list(newsletter_list):
    return {
        "id": newsletter_list.id,
        "name": newsletter_list.name,
        "slug": newsletter_list.slug,
        "description": newsletter_list.description,
        "is_default": newsletter_list.is_default,
        "is_public": newsletter_list.is_public,
        "is_active": newsletter_list.is_active,
        "sort_order": newsletter_list.sort_order,
        "subscriber_count": (
            newsletter_list.memberships.filter(
                is_deleted=False,
            ).count()
        ),
    }


def serialize_tag(tag):
    return {
        "id": tag.id,
        "name": tag.name,
        "slug": tag.slug,
        "description": tag.description,
        "color": tag.color,
        "is_active": tag.is_active,
        "subscriber_count": (
            tag.assignments.filter(
                is_deleted=False,
            ).count()
        ),
    }


def serialize_subscriber(subscriber):
    return {
        "id": subscriber.id,
        "email": subscriber.email,
        "first_name": subscriber.first_name,
        "last_name": subscriber.last_name,
        "full_name": subscriber.full_name,
        "company_name": subscriber.company_name,
        "phone": subscriber.phone,
        "country": subscriber.country,
        "language": subscriber.language,
        "status": subscriber.status,
        "source": subscriber.source,
        "source_reference": (
            subscriber.source_reference
        ),
        "consent_given": subscriber.consent_given,
        "subscribed_at": subscriber.subscribed_at,
        "confirmed_at": subscriber.confirmed_at,
        "unsubscribed_at": (
            subscriber.unsubscribed_at
        ),
        "confirmation_token": (
            subscriber.confirmation_token
        ),
        "unsubscribe_token": (
            subscriber.unsubscribe_token
        ),
        "bounce_count": subscriber.bounce_count,
        "last_bounced_at": subscriber.last_bounced_at,
        "last_email_sent_at": (
            subscriber.last_email_sent_at
        ),
        "metadata": subscriber.metadata,
        "can_receive_email": (
            subscriber.can_receive_email
        ),
        "lists": [
            serialize_list(
                membership.newsletter_list
            )
            for membership in (
                subscriber.list_memberships.all()
            )
        ],
        "tags": [
            serialize_tag(assignment.tag)
            for assignment in (
                subscriber.tag_assignments.all()
            )
        ],
        "created_at": subscriber.created_at,
        "updated_at": subscriber.updated_at,
    }


def subscriber_payload(payload):
    values = payload.dict()

    list_ids = values.pop("list_ids")
    tag_ids = values.pop("tag_ids")

    values["email"] = payload.email.strip().lower()

    return (
        values,
        resolve_lists(list_ids),
        resolve_tags(tag_ids),
    )


@router.get(
    "/lists",
    response={
        200: list[NewsletterListSchema],
        403: ErrorSchema,
    },
)
@require_permissions("newsletter.view_newsletterlist")
def list_newsletter_lists(
    request,
    search: str | None = None,
    is_public: bool | None = None,
    is_active: bool | None = None,
):
    return [
        serialize_list(item)
        for item in NewsletterListRepository.search(
            search=search,
            is_public=is_public,
            is_active=is_active,
        )
    ]


@router.post(
    "/lists",
    response={
        201: NewsletterListSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("newsletter.add_newsletterlist")
def create_newsletter_list(
    request,
    payload: NewsletterListCreateSchema,
):
    normalized_slug = slugify(payload.slug)

    if NewsletterList.all_objects.filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Newsletter list slug already exists.",
            code="duplicate_newsletter_list_slug",
        )

    values = payload.dict()
    values["slug"] = normalized_slug

    newsletter_list = NewsletterList.objects.create(
        **values,
    )

    return 201, serialize_list(newsletter_list)


@router.get(
    "/tags",
    response={
        200: list[NewsletterTagSchema],
        403: ErrorSchema,
    },
)
@require_permissions("newsletter.view_newslettertag")
def list_newsletter_tags(
    request,
    search: str | None = None,
    is_active: bool | None = None,
):
    return [
        serialize_tag(item)
        for item in NewsletterTagRepository.search(
            search=search,
            is_active=is_active,
        )
    ]


@router.post(
    "/tags",
    response={
        201: NewsletterTagSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("newsletter.add_newslettertag")
def create_newsletter_tag(
    request,
    payload: NewsletterTagCreateSchema,
):
    normalized_slug = slugify(payload.slug)

    if NewsletterTag.all_objects.filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Newsletter tag slug already exists.",
            code="duplicate_newsletter_tag_slug",
        )

    values = payload.dict()
    values["slug"] = normalized_slug

    tag = NewsletterTag.objects.create(**values)

    return 201, serialize_tag(tag)


@router.get(
    "/subscribers",
    response={
        200: list[SubscriberSchema],
        403: ErrorSchema,
    },
)
@require_permissions("newsletter.view_subscriber")
def list_subscribers(
    request,
    search: str | None = None,
    status: str | None = None,
    source: str | None = None,
    country: str | None = None,
    language: str | None = None,
    list_id: str | None = None,
    tag_id: str | None = None,
    ordering: str | None = None,
):
    return [
        serialize_subscriber(item)
        for item in SubscriberRepository.search(
            search=search,
            status=status,
            source=source,
            country=country,
            language=language,
            list_id=list_id,
            tag_id=tag_id,
            ordering=ordering,
        )
    ]


@router.post(
    "/subscribers",
    response={
        201: SubscriberSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("newsletter.add_subscriber")
def create_subscriber(
    request,
    payload: SubscriberCreateSchema,
):
    normalized_email = payload.email.strip().lower()

    if Subscriber.all_objects.filter(
        email__iexact=normalized_email,
        is_deleted=False,
    ).exists():
        raise ApiHttpError(
            400,
            "Newsletter subscriber already exists.",
            code="duplicate_newsletter_subscriber",
        )

    values, newsletter_lists, tags = (
        subscriber_payload(payload)
    )

    subscriber = SubscriberService.create_subscriber(
        request=request,
        values=values,
        newsletter_lists=newsletter_lists,
        tags=tags,
    )

    return 201, serialize_subscriber(
        get_subscriber(subscriber.id)
    )


@router.get(
    "/subscribers/{subscriber_id}",
    response={
        200: SubscriberSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("newsletter.view_subscriber")
def subscriber_detail(
    request,
    subscriber_id: str,
):
    return serialize_subscriber(
        get_subscriber(subscriber_id)
    )


@router.put(
    "/subscribers/{subscriber_id}",
    response={
        200: SubscriberSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("newsletter.change_subscriber")
def update_subscriber(
    request,
    subscriber_id: str,
    payload: SubscriberUpdateSchema,
):
    subscriber = get_subscriber(subscriber_id)
    normalized_email = payload.email.strip().lower()

    if Subscriber.all_objects.exclude(
        pk=subscriber.pk
    ).filter(
        email__iexact=normalized_email,
        is_deleted=False,
    ).exists():
        raise ApiHttpError(
            400,
            "Newsletter subscriber already exists.",
            code="duplicate_newsletter_subscriber",
        )

    values, newsletter_lists, tags = (
        subscriber_payload(payload)
    )

    subscriber = SubscriberService.update_subscriber(
        request=request,
        subscriber=subscriber,
        values=values,
        newsletter_lists=newsletter_lists,
        tags=tags,
    )

    return serialize_subscriber(
        get_subscriber(subscriber.id)
    )


@router.post(
    "/subscribers/{subscriber_id}/confirm",
    response={
        200: SubscriberSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("newsletter.change_subscriber")
def confirm_subscriber(
    request,
    subscriber_id: str,
):
    subscriber = SubscriberService.confirm_subscription(
        request=request,
        subscriber=get_subscriber(subscriber_id),
    )

    return serialize_subscriber(
        get_subscriber(subscriber.id)
    )


@router.post(
    "/subscribers/{subscriber_id}/unsubscribe",
    response={
        200: SubscriberSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("newsletter.change_subscriber")
def unsubscribe_subscriber(
    request,
    subscriber_id: str,
):
    subscriber = SubscriberService.unsubscribe(
        request=request,
        subscriber=get_subscriber(subscriber_id),
    )

    return serialize_subscriber(
        get_subscriber(subscriber.id)
    )


@router.post(
    "/subscribers/{subscriber_id}/resubscribe",
    response={
        200: SubscriberSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("newsletter.change_subscriber")
def resubscribe_subscriber(
    request,
    subscriber_id: str,
):
    subscriber = SubscriberService.resubscribe(
        request=request,
        subscriber=get_subscriber(subscriber_id),
    )

    return serialize_subscriber(
        get_subscriber(subscriber.id)
    )



from .repositories import (
    CampaignRecipientRepository,
    NewsletterCampaignRepository,
    NewsletterDashboardRepository,
)
from .schemas import (
    CampaignRecipientSchema,
    NewsletterCampaignCreateSchema,
    NewsletterCampaignScheduleSchema,
    NewsletterCampaignSchema,
    NewsletterCampaignUpdateSchema,
    NewsletterDashboardSchema,
)
from .services import NewsletterCampaignService


def get_campaign(campaign_id):
    campaign = NewsletterCampaignRepository.find_by_id(
        campaign_id
    )

    if campaign is None:
        raise ApiHttpError(
            404,
            "Newsletter campaign not found.",
            code="newsletter_campaign_not_found",
        )

    return campaign


def campaign_payload(payload):
    values = payload.dict()

    list_ids = values.pop("list_ids")
    tag_ids = values.pop("tag_ids")

    return (
        values,
        resolve_lists(list_ids),
        resolve_tags(tag_ids),
    )


def serialize_campaign(campaign):
    return {
        "id": campaign.id,
        "name": campaign.name,
        "subject": campaign.subject,
        "preview_text": campaign.preview_text,
        "from_name": campaign.from_name,
        "from_email": campaign.from_email,
        "reply_to_email": campaign.reply_to_email,
        "html_content": campaign.html_content,
        "text_content": campaign.text_content,
        "status": campaign.status,
        "scheduled_for": campaign.scheduled_for,
        "queued_at": campaign.queued_at,
        "sending_started_at": (
            campaign.sending_started_at
        ),
        "sent_at": campaign.sent_at,
        "completed_at": campaign.completed_at,
        "failure_reason": campaign.failure_reason,
        "recipient_count": campaign.recipient_count,
        "queued_count": campaign.queued_count,
        "sent_count": campaign.sent_count,
        "delivered_count": campaign.delivered_count,
        "opened_count": campaign.opened_count,
        "clicked_count": campaign.clicked_count,
        "bounced_count": campaign.bounced_count,
        "complained_count": campaign.complained_count,
        "unsubscribed_count": (
            campaign.unsubscribed_count
        ),
        "failed_count": campaign.failed_count,
        "open_rate": campaign.open_rate,
        "click_rate": campaign.click_rate,
        "metadata": campaign.metadata,
        "lists": [
            serialize_list(target.newsletter_list)
            for target in campaign.list_targets.all()
        ],
        "tags": [
            serialize_tag(target.tag)
            for target in campaign.tag_targets.all()
        ],
        "created_at": campaign.created_at,
        "updated_at": campaign.updated_at,
    }


def serialize_recipient(recipient):
    return {
        "id": recipient.id,
        "subscriber_id": recipient.subscriber_id,
        "email": recipient.email,
        "first_name": recipient.first_name,
        "last_name": recipient.last_name,
        "status": recipient.status,
        "queued_at": recipient.queued_at,
        "sent_at": recipient.sent_at,
        "delivered_at": recipient.delivered_at,
        "opened_at": recipient.opened_at,
        "clicked_at": recipient.clicked_at,
        "bounced_at": recipient.bounced_at,
        "complained_at": recipient.complained_at,
        "unsubscribed_at": recipient.unsubscribed_at,
        "failed_at": recipient.failed_at,
        "failure_reason": recipient.failure_reason,
        "provider_message_id": (
            recipient.provider_message_id
        ),
        "open_count": recipient.open_count,
        "click_count": recipient.click_count,
    }


@router.get(
    "/campaigns",
    response={
        200: list[NewsletterCampaignSchema],
        403: ErrorSchema,
    },
)
@require_permissions(
    "newsletter.view_newslettercampaign"
)
def list_campaigns(
    request,
    search: str | None = None,
    status: str | None = None,
    ordering: str | None = None,
):
    return [
        serialize_campaign(campaign)
        for campaign in (
            NewsletterCampaignRepository.search(
                search=search,
                status=status,
                ordering=ordering,
            )
        )
    ]


@router.post(
    "/campaigns",
    response={
        201: NewsletterCampaignSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "newsletter.add_newslettercampaign"
)
def create_campaign(
    request,
    payload: NewsletterCampaignCreateSchema,
):
    values, newsletter_lists, tags = (
        campaign_payload(payload)
    )

    campaign = (
        NewsletterCampaignService.create_campaign(
            request=request,
            values=values,
            newsletter_lists=newsletter_lists,
            tags=tags,
        )
    )

    return 201, serialize_campaign(
        get_campaign(campaign.id)
    )


@router.get(
    "/campaigns/{campaign_id}",
    response={
        200: NewsletterCampaignSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "newsletter.view_newslettercampaign"
)
def campaign_detail(request, campaign_id: str):
    return serialize_campaign(
        get_campaign(campaign_id)
    )


@router.put(
    "/campaigns/{campaign_id}",
    response={
        200: NewsletterCampaignSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "newsletter.change_newslettercampaign"
)
def update_campaign(
    request,
    campaign_id: str,
    payload: NewsletterCampaignUpdateSchema,
):
    values, newsletter_lists, tags = (
        campaign_payload(payload)
    )

    try:
        campaign = (
            NewsletterCampaignService.update_campaign(
                request=request,
                campaign=get_campaign(campaign_id),
                values=values,
                newsletter_lists=newsletter_lists,
                tags=tags,
            )
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_campaign_update",
        ) from exc

    return serialize_campaign(
        get_campaign(campaign.id)
    )


@router.post(
    "/campaigns/{campaign_id}/schedule",
    response={
        200: NewsletterCampaignSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "newsletter.change_newslettercampaign"
)
def schedule_campaign(
    request,
    campaign_id: str,
    payload: NewsletterCampaignScheduleSchema,
):
    try:
        campaign = (
            NewsletterCampaignService.schedule_campaign(
                request=request,
                campaign=get_campaign(campaign_id),
                scheduled_for=payload.scheduled_for,
            )
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_campaign_schedule",
        ) from exc

    return serialize_campaign(
        get_campaign(campaign.id)
    )


@router.post(
    "/campaigns/{campaign_id}/prepare",
    response={
        200: NewsletterCampaignSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "newsletter.change_newslettercampaign"
)
def prepare_campaign(
    request,
    campaign_id: str,
):
    try:
        campaign = (
            NewsletterCampaignService.prepare_recipients(
                request=request,
                campaign=get_campaign(campaign_id),
            )
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_campaign_preparation",
        ) from exc

    return serialize_campaign(
        get_campaign(campaign.id)
    )


@router.post(
    "/campaigns/{campaign_id}/mark-sent",
    response={
        200: NewsletterCampaignSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "newsletter.change_newslettercampaign"
)
def mark_campaign_sent(
    request,
    campaign_id: str,
):
    campaign = (
        NewsletterCampaignService.mark_campaign_sent(
            request=request,
            campaign=get_campaign(campaign_id),
        )
    )

    return serialize_campaign(
        get_campaign(campaign.id)
    )


@router.get(
    "/campaigns/{campaign_id}/recipients",
    response={
        200: list[CampaignRecipientSchema],
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions(
    "newsletter.view_campaignrecipient"
)
def list_campaign_recipients(
    request,
    campaign_id: str,
    status: str | None = None,
):
    get_campaign(campaign_id)

    return [
        serialize_recipient(recipient)
        for recipient in (
            CampaignRecipientRepository.for_campaign(
                campaign_id,
                status=status,
            )
        )
    ]


@router.get(
    "/dashboard",
    response={
        200: NewsletterDashboardSchema,
        403: ErrorSchema,
    },
)
@require_permissions("newsletter.view_subscriber")
def newsletter_dashboard(request):
    return NewsletterDashboardRepository.statistics()
