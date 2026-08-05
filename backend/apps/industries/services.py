from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    Industry,
    IndustryFaq,
    IndustryRevision,
    IndustrySeo,
    IndustryService,
    IndustryStatus,
)


class IndustryServiceLayer:
    @staticmethod
    def snapshot(industry: Industry) -> dict[str, Any]:
        try:
            seo = industry.seo
        except IndustrySeo.DoesNotExist:
            seo = None

        return {
            "name": industry.name,
            "slug": industry.slug,
            "short_description": industry.short_description,
            "description": industry.description,
            "hero_title": industry.hero_title,
            "hero_description": industry.hero_description,
            "hero_image_id": (
                str(industry.hero_image_id)
                if industry.hero_image_id
                else None
            ),
            "icon": industry.icon,
            "status": industry.status,
            "is_featured": industry.is_featured,
            "is_active": industry.is_active,
            "sort_order": industry.sort_order,
            "challenges": industry.challenges,
            "solutions": industry.solutions,
            "benefits": industry.benefits,
            "cta_title": industry.cta_title,
            "cta_text": industry.cta_text,
            "cta_label": industry.cta_label,
            "cta_url": industry.cta_url,
            "services": [
                {
                    "service_id": str(item.service_id),
                    "description": item.description,
                    "sort_order": item.sort_order,
                    "is_featured": item.is_featured,
                }
                for item in industry.service_links.all()
            ],
            "faqs": [
                {
                    "question": item.question,
                    "answer": item.answer,
                    "sort_order": item.sort_order,
                }
                for item in industry.faqs.all()
            ],
            "seo": (
                {
                    "meta_title": seo.meta_title,
                    "meta_description": seo.meta_description,
                    "canonical_url": seo.canonical_url,
                    "robots_index": seo.robots_index,
                    "robots_follow": seo.robots_follow,
                    "open_graph_title": seo.open_graph_title,
                    "open_graph_description": (
                        seo.open_graph_description
                    ),
                    "open_graph_image_id": (
                        str(seo.open_graph_image_id)
                        if seo.open_graph_image_id
                        else None
                    ),
                    "twitter_title": seo.twitter_title,
                    "twitter_description": (
                        seo.twitter_description
                    ),
                    "structured_data": seo.structured_data,
                }
                if seo
                else {}
            ),
        }

    @staticmethod
    def create_revision(
        *,
        industry,
        actor,
        change_summary="",
    ):
        latest = (
            IndustryRevision.all_objects.filter(
                industry=industry,
            )
            .order_by("-revision_number")
            .values_list("revision_number", flat=True)
            .first()
        )

        number = (latest or 0) + 1

        revision = IndustryRevision.objects.create(
            industry=industry,
            revision_number=number,
            snapshot=IndustryServiceLayer.snapshot(
                industry
            ),
            change_summary=change_summary,
            created_by=actor,
            updated_by=actor,
        )

        industry.current_revision_number = number
        industry.save(
            update_fields=[
                "current_revision_number",
                "updated_at",
            ],
        )

        return revision

    @staticmethod
    def replace_related(
        *,
        request,
        industry,
        services,
        faqs,
    ):
        industry.service_links.all().delete()
        industry.faqs.all().delete()

        for index, values in enumerate(services):
            IndustryService.objects.create(
                industry=industry,
                sort_order=values.get("sort_order", index),
                created_by=request.auth,
                updated_by=request.auth,
                **{
                    key: value
                    for key, value in values.items()
                    if key != "sort_order"
                },
            )

        for index, values in enumerate(faqs):
            IndustryFaq.objects.create(
                industry=industry,
                sort_order=values.get("sort_order", index),
                created_by=request.auth,
                updated_by=request.auth,
                **{
                    key: value
                    for key, value in values.items()
                    if key != "sort_order"
                },
            )

    @staticmethod
    @transaction.atomic
    def create_industry(
        *,
        request,
        values,
        services,
        faqs,
        seo_values,
    ):
        industry = Industry.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        IndustrySeo.objects.create(
            industry=industry,
            created_by=request.auth,
            updated_by=request.auth,
            **seo_values,
        )

        IndustryServiceLayer.replace_related(
            request=request,
            industry=industry,
            services=services,
            faqs=faqs,
        )

        IndustryServiceLayer.create_revision(
            industry=industry,
            actor=request.auth,
            change_summary="Initial industry revision.",
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="industry_created",
            module="industries",
            description="Industry created.",
            entity_type="industries.Industry",
            entity_id=str(industry.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="industries",
            message="Industry created.",
            target_type="industries.Industry",
            target_id=str(industry.pk),
            after={
                "name": industry.name,
                "slug": industry.slug,
                "status": industry.status,
            },
        )

        return industry

    @staticmethod
    @transaction.atomic
    def update_industry(
        *,
        request,
        industry,
        values,
        services,
        faqs,
        seo_values,
        change_summary="",
    ):
        for field, value in values.items():
            setattr(industry, field, value)

        industry.updated_by = request.auth
        industry.save()

        seo, _ = IndustrySeo.objects.get_or_create(
            industry=industry,
            defaults={
                "created_by": request.auth,
                "updated_by": request.auth,
            },
        )

        for field, value in seo_values.items():
            setattr(seo, field, value)

        seo.updated_by = request.auth
        seo.save()

        IndustryServiceLayer.replace_related(
            request=request,
            industry=industry,
            services=services,
            faqs=faqs,
        )

        IndustryServiceLayer.create_revision(
            industry=industry,
            actor=request.auth,
            change_summary=change_summary,
        )

        return industry

    @staticmethod
    @transaction.atomic
    def publish_industry(*, request, industry):
        industry.status = IndustryStatus.PUBLISHED
        industry.published_at = timezone.now()
        industry.scheduled_for = None
        industry.updated_by = request.auth
        industry.save()

        IndustryServiceLayer.create_revision(
            industry=industry,
            actor=request.auth,
            change_summary="Industry published.",
        )

        return industry

    @staticmethod
    @transaction.atomic
    def schedule_industry(
        *,
        request,
        industry,
        scheduled_for,
    ):
        if scheduled_for <= timezone.now():
            raise ValueError(
                "Scheduled publication time must be in the future."
            )

        industry.status = IndustryStatus.SCHEDULED
        industry.scheduled_for = scheduled_for
        industry.published_at = None
        industry.updated_by = request.auth
        industry.save()

        return industry

    @staticmethod
    @transaction.atomic
    def process_scheduled_industries():
        industries = list(
            Industry.objects.filter(
                is_active=True,
                status=IndustryStatus.SCHEDULED,
                scheduled_for__lte=timezone.now(),
            )
        )

        for industry in industries:
            industry.status = IndustryStatus.PUBLISHED
            industry.published_at = industry.scheduled_for
            industry.scheduled_for = None
            industry.save()

        return len(industries)

    @staticmethod
    @transaction.atomic
    def soft_delete(*, request, industry):
        industry_id = str(industry.pk)
        industry.delete()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="industries",
            message="Industry soft deleted.",
            target_type="industries.Industry",
            target_id=industry_id,
            after={"is_deleted": True},
        )
