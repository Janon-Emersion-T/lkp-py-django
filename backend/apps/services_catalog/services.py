from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    Service,
    ServiceFaq,
    ServiceFeature,
    ServiceProcessStep,
    ServiceRevision,
    ServiceSeo,
    ServiceStatus,
    ServiceTechnology,
)


class ServiceCatalogService:
    @staticmethod
    def service_snapshot(service: Service) -> dict[str, Any]:
        try:
            seo = service.seo
        except ServiceSeo.DoesNotExist:
            seo = None

        return {
            "title": service.title,
            "slug": service.slug,
            "short_description": service.short_description,
            "description": service.description,
            "hero_title": service.hero_title,
            "hero_description": service.hero_description,
            "hero_image_id": (
                str(service.hero_image_id)
                if service.hero_image_id
                else None
            ),
            "status": service.status,
            "icon": service.icon,
            "sort_order": service.sort_order,
            "is_featured": service.is_featured,
            "is_active": service.is_active,
            "cta_title": service.cta_title,
            "cta_text": service.cta_text,
            "cta_label": service.cta_label,
            "cta_url": service.cta_url,
            "features": [
                {
                    "title": feature.title,
                    "description": feature.description,
                    "icon": feature.icon,
                    "sort_order": feature.sort_order,
                }
                for feature in service.features.all()
            ],
            "process_steps": [
                {
                    "title": step.title,
                    "description": step.description,
                    "step_number": step.step_number,
                    "sort_order": step.sort_order,
                }
                for step in service.process_steps.all()
            ],
            "technologies": [
                {
                    "name": technology.name,
                    "description": technology.description,
                    "logo_id": (
                        str(technology.logo_id)
                        if technology.logo_id
                        else None
                    ),
                    "sort_order": technology.sort_order,
                }
                for technology in service.technologies.all()
            ],
            "faqs": [
                {
                    "question": faq.question,
                    "answer": faq.answer,
                    "sort_order": faq.sort_order,
                }
                for faq in service.faqs.all()
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
        service: Service,
        actor,
        change_summary: str = "",
    ) -> ServiceRevision:
        latest = (
            ServiceRevision.all_objects.filter(
                service=service,
            )
            .order_by("-revision_number")
            .values_list("revision_number", flat=True)
            .first()
        )

        revision_number = (latest or 0) + 1

        revision = ServiceRevision.objects.create(
            service=service,
            revision_number=revision_number,
            snapshot=(
                ServiceCatalogService.service_snapshot(
                    service
                )
            ),
            change_summary=change_summary,
            created_by=actor,
            updated_by=actor,
        )

        service.current_revision_number = revision_number
        service.save(
            update_fields=[
                "current_revision_number",
                "updated_at",
            ],
        )

        return revision

    @staticmethod
    def replace_related_content(
        *,
        request,
        service: Service,
        features: list[dict[str, Any]],
        process_steps: list[dict[str, Any]],
        technologies: list[dict[str, Any]],
        faqs: list[dict[str, Any]],
    ) -> None:
        service.features.all().delete()
        service.process_steps.all().delete()
        service.technologies.all().delete()
        service.faqs.all().delete()

        for index, values in enumerate(features):
            ServiceFeature.objects.create(
                service=service,
                sort_order=values.get(
                    "sort_order",
                    index,
                ),
                created_by=request.auth,
                updated_by=request.auth,
                **{
                    key: value
                    for key, value in values.items()
                    if key != "sort_order"
                },
            )

        for index, values in enumerate(process_steps):
            ServiceProcessStep.objects.create(
                service=service,
                sort_order=values.get(
                    "sort_order",
                    index,
                ),
                created_by=request.auth,
                updated_by=request.auth,
                **{
                    key: value
                    for key, value in values.items()
                    if key != "sort_order"
                },
            )

        for index, values in enumerate(technologies):
            ServiceTechnology.objects.create(
                service=service,
                sort_order=values.get(
                    "sort_order",
                    index,
                ),
                created_by=request.auth,
                updated_by=request.auth,
                **{
                    key: value
                    for key, value in values.items()
                    if key != "sort_order"
                },
            )

        for index, values in enumerate(faqs):
            ServiceFaq.objects.create(
                service=service,
                sort_order=values.get(
                    "sort_order",
                    index,
                ),
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
    def create_service(
        *,
        request,
        values: dict[str, Any],
        features: list[dict[str, Any]],
        process_steps: list[dict[str, Any]],
        technologies: list[dict[str, Any]],
        faqs: list[dict[str, Any]],
        seo_values: dict[str, Any],
    ) -> Service:
        service = Service.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        ServiceSeo.objects.create(
            service=service,
            created_by=request.auth,
            updated_by=request.auth,
            **seo_values,
        )

        ServiceCatalogService.replace_related_content(
            request=request,
            service=service,
            features=features,
            process_steps=process_steps,
            technologies=technologies,
            faqs=faqs,
        )

        ServiceCatalogService.create_revision(
            service=service,
            actor=request.auth,
            change_summary="Initial service revision.",
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="service_created",
            module="services_catalog",
            description="Service created.",
            entity_type="services_catalog.Service",
            entity_id=str(service.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="services_catalog",
            message="Service created.",
            target_type="services_catalog.Service",
            target_id=str(service.pk),
            after={
                "title": service.title,
                "slug": service.slug,
                "status": service.status,
            },
        )

        return service

    @staticmethod
    @transaction.atomic
    def update_service(
        *,
        request,
        service: Service,
        values: dict[str, Any],
        features: list[dict[str, Any]],
        process_steps: list[dict[str, Any]],
        technologies: list[dict[str, Any]],
        faqs: list[dict[str, Any]],
        seo_values: dict[str, Any],
        change_summary: str = "",
    ) -> Service:
        before = {
            "title": service.title,
            "slug": service.slug,
            "status": service.status,
            "current_revision_number": (
                service.current_revision_number
            ),
        }

        for field, value in values.items():
            setattr(service, field, value)

        service.updated_by = request.auth
        service.save()

        seo, _ = ServiceSeo.objects.get_or_create(
            service=service,
            defaults={
                "created_by": request.auth,
                "updated_by": request.auth,
            },
        )

        for field, value in seo_values.items():
            setattr(seo, field, value)

        seo.updated_by = request.auth
        seo.save()

        ServiceCatalogService.replace_related_content(
            request=request,
            service=service,
            features=features,
            process_steps=process_steps,
            technologies=technologies,
            faqs=faqs,
        )

        ServiceCatalogService.create_revision(
            service=service,
            actor=request.auth,
            change_summary=change_summary,
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="services_catalog",
            message="Service updated.",
            target_type="services_catalog.Service",
            target_id=str(service.pk),
            before=before,
            after={
                "title": service.title,
                "slug": service.slug,
                "status": service.status,
                "current_revision_number": (
                    service.current_revision_number
                ),
            },
        )

        return service

    @staticmethod
    @transaction.atomic
    def publish_service(
        *,
        request,
        service: Service,
    ) -> Service:
        service.status = ServiceStatus.PUBLISHED
        service.published_at = timezone.now()
        service.scheduled_for = None
        service.updated_by = request.auth
        service.save(
            update_fields=[
                "status",
                "published_at",
                "scheduled_for",
                "updated_by",
                "updated_at",
            ],
        )

        ServiceCatalogService.create_revision(
            service=service,
            actor=request.auth,
            change_summary="Service published.",
        )

        return service

    @staticmethod
    @transaction.atomic
    def schedule_service(
        *,
        request,
        service: Service,
        scheduled_for,
    ) -> Service:
        if scheduled_for <= timezone.now():
            raise ValueError(
                "Scheduled publication time must be in the future."
            )

        service.status = ServiceStatus.SCHEDULED
        service.scheduled_for = scheduled_for
        service.published_at = None
        service.updated_by = request.auth
        service.save(
            update_fields=[
                "status",
                "scheduled_for",
                "published_at",
                "updated_by",
                "updated_at",
            ],
        )

        return service

    @staticmethod
    @transaction.atomic
    def process_scheduled_services() -> int:
        services = list(
            Service.objects.filter(
                is_active=True,
                status=ServiceStatus.SCHEDULED,
                scheduled_for__lte=timezone.now(),
            )
        )

        for service in services:
            service.status = ServiceStatus.PUBLISHED
            service.published_at = service.scheduled_for
            service.scheduled_for = None
            service.save(
                update_fields=[
                    "status",
                    "published_at",
                    "scheduled_for",
                    "updated_at",
                ],
            )

        return len(services)

    @staticmethod
    @transaction.atomic
    def soft_delete_service(
        *,
        request,
        service: Service,
    ) -> None:
        service_id = str(service.pk)
        service.delete()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="services_catalog",
            message="Service soft deleted.",
            target_type="services_catalog.Service",
            target_id=service_id,
            after={"is_deleted": True},
        )
