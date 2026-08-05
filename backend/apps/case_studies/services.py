from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    CaseStudy,
    CaseStudyMedia,
    CaseStudyMetric,
    CaseStudyMilestone,
    CaseStudyRevision,
    CaseStudySeo,
    CaseStudyService,
    CaseStudyStatus,
    CaseStudyTechnology,
)


class CaseStudyServiceLayer:
    @staticmethod
    def snapshot(case_study: CaseStudy) -> dict[str, Any]:
        try:
            seo = case_study.seo
        except CaseStudySeo.DoesNotExist:
            seo = None

        return {
            "title": case_study.title,
            "slug": case_study.slug,
            "client_id": (
                str(case_study.client_id)
                if case_study.client_id
                else None
            ),
            "project_id": (
                str(case_study.project_id)
                if case_study.project_id
                else None
            ),
            "industry_id": (
                str(case_study.industry_id)
                if case_study.industry_id
                else None
            ),
            "client_name": case_study.client_name,
            "location": case_study.location,
            "website_url": case_study.website_url,
            "short_description": (
                case_study.short_description
            ),
            "overview": case_study.overview,
            "challenge": case_study.challenge,
            "solution": case_study.solution,
            "implementation": case_study.implementation,
            "results": case_study.results,
            "testimonial": case_study.testimonial,
            "testimonial_author": (
                case_study.testimonial_author
            ),
            "testimonial_position": (
                case_study.testimonial_position
            ),
            "featured_image_id": (
                str(case_study.featured_image_id)
                if case_study.featured_image_id
                else None
            ),
            "status": case_study.status,
            "project_start_date": (
                case_study.project_start_date.isoformat()
                if case_study.project_start_date
                else None
            ),
            "project_completion_date": (
                case_study.project_completion_date.isoformat()
                if case_study.project_completion_date
                else None
            ),
            "project_duration": (
                case_study.project_duration
            ),
            "is_featured": case_study.is_featured,
            "is_active": case_study.is_active,
            "sort_order": case_study.sort_order,
            "services": [
                {
                    "service_id": str(item.service_id),
                    "description": item.description,
                    "sort_order": item.sort_order,
                }
                for item in case_study.service_links.all()
            ],
            "technologies": [
                {
                    "name": item.name,
                    "description": item.description,
                    "logo_id": (
                        str(item.logo_id)
                        if item.logo_id
                        else None
                    ),
                    "sort_order": item.sort_order,
                }
                for item in case_study.technologies.all()
            ],
            "media_items": [
                {
                    "asset_id": str(item.asset_id),
                    "title": item.title,
                    "caption": item.caption,
                    "media_role": item.media_role,
                    "sort_order": item.sort_order,
                }
                for item in case_study.media_items.all()
            ],
            "metrics": [
                {
                    "label": item.label,
                    "value": item.value,
                    "description": item.description,
                    "icon": item.icon,
                    "sort_order": item.sort_order,
                }
                for item in case_study.metrics.all()
            ],
            "milestones": [
                {
                    "title": item.title,
                    "description": item.description,
                    "milestone_date": (
                        item.milestone_date.isoformat()
                        if item.milestone_date
                        else None
                    ),
                    "sort_order": item.sort_order,
                }
                for item in case_study.milestones.all()
            ],
            "seo": (
                {
                    "meta_title": seo.meta_title,
                    "meta_description": seo.meta_description,
                    "canonical_url": seo.canonical_url,
                    "robots_index": seo.robots_index,
                    "robots_follow": seo.robots_follow,
                    "open_graph_title": (
                        seo.open_graph_title
                    ),
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
                    "structured_data": (
                        seo.structured_data
                    ),
                }
                if seo
                else {}
            ),
        }

    @staticmethod
    def create_revision(
        *,
        case_study,
        actor,
        change_summary="",
    ):
        latest = (
            CaseStudyRevision.all_objects.filter(
                case_study=case_study,
            )
            .order_by("-revision_number")
            .values_list("revision_number", flat=True)
            .first()
        )

        number = (latest or 0) + 1

        revision = CaseStudyRevision.objects.create(
            case_study=case_study,
            revision_number=number,
            snapshot=(
                CaseStudyServiceLayer.snapshot(
                    case_study
                )
            ),
            change_summary=change_summary,
            created_by=actor,
            updated_by=actor,
        )

        case_study.current_revision_number = number
        case_study.save(
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
        case_study,
        services,
        technologies,
        media_items,
        metrics,
        milestones,
    ):
        case_study.service_links.all().delete()
        case_study.technologies.all().delete()
        case_study.media_items.all().delete()
        case_study.metrics.all().delete()
        case_study.milestones.all().delete()

        mappings = (
            (CaseStudyService, services),
            (CaseStudyTechnology, technologies),
            (CaseStudyMedia, media_items),
            (CaseStudyMetric, metrics),
            (CaseStudyMilestone, milestones),
        )

        for model, rows in mappings:
            for index, values in enumerate(rows):
                model.objects.create(
                    case_study=case_study,
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
    def create_case_study(
        *,
        request,
        values,
        services,
        technologies,
        media_items,
        metrics,
        milestones,
        seo_values,
    ):
        case_study = CaseStudy.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        CaseStudySeo.objects.create(
            case_study=case_study,
            created_by=request.auth,
            updated_by=request.auth,
            **seo_values,
        )

        CaseStudyServiceLayer.replace_related(
            request=request,
            case_study=case_study,
            services=services,
            technologies=technologies,
            media_items=media_items,
            metrics=metrics,
            milestones=milestones,
        )

        CaseStudyServiceLayer.create_revision(
            case_study=case_study,
            actor=request.auth,
            change_summary=(
                "Initial case study revision."
            ),
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="case_study_created",
            module="case_studies",
            description="Case study created.",
            entity_type="case_studies.CaseStudy",
            entity_id=str(case_study.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="case_studies",
            message="Case study created.",
            target_type="case_studies.CaseStudy",
            target_id=str(case_study.pk),
            after={
                "title": case_study.title,
                "slug": case_study.slug,
                "status": case_study.status,
            },
        )

        return case_study

    @staticmethod
    @transaction.atomic
    def update_case_study(
        *,
        request,
        case_study,
        values,
        services,
        technologies,
        media_items,
        metrics,
        milestones,
        seo_values,
        change_summary="",
    ):
        for field, value in values.items():
            setattr(case_study, field, value)

        case_study.updated_by = request.auth
        case_study.save()

        seo, _ = CaseStudySeo.objects.get_or_create(
            case_study=case_study,
            defaults={
                "created_by": request.auth,
                "updated_by": request.auth,
            },
        )

        for field, value in seo_values.items():
            setattr(seo, field, value)

        seo.updated_by = request.auth
        seo.save()

        CaseStudyServiceLayer.replace_related(
            request=request,
            case_study=case_study,
            services=services,
            technologies=technologies,
            media_items=media_items,
            metrics=metrics,
            milestones=milestones,
        )

        CaseStudyServiceLayer.create_revision(
            case_study=case_study,
            actor=request.auth,
            change_summary=change_summary,
        )

        return case_study

    @staticmethod
    @transaction.atomic
    def publish(*, request, case_study):
        case_study.status = CaseStudyStatus.PUBLISHED
        case_study.published_at = timezone.now()
        case_study.scheduled_for = None
        case_study.updated_by = request.auth
        case_study.save()

        CaseStudyServiceLayer.create_revision(
            case_study=case_study,
            actor=request.auth,
            change_summary="Case study published.",
        )

        return case_study

    @staticmethod
    @transaction.atomic
    def schedule(
        *,
        request,
        case_study,
        scheduled_for,
    ):
        if scheduled_for <= timezone.now():
            raise ValueError(
                "Scheduled publication time must be in the future."
            )

        case_study.status = CaseStudyStatus.SCHEDULED
        case_study.scheduled_for = scheduled_for
        case_study.published_at = None
        case_study.updated_by = request.auth
        case_study.save()

        return case_study

    @staticmethod
    @transaction.atomic
    def process_scheduled():
        case_studies = list(
            CaseStudy.objects.filter(
                is_active=True,
                status=CaseStudyStatus.SCHEDULED,
                scheduled_for__lte=timezone.now(),
            )
        )

        for case_study in case_studies:
            case_study.status = (
                CaseStudyStatus.PUBLISHED
            )
            case_study.published_at = (
                case_study.scheduled_for
            )
            case_study.scheduled_for = None
            case_study.save()

        return len(case_studies)

    @staticmethod
    @transaction.atomic
    def soft_delete(*, request, case_study):
        case_study_id = str(case_study.pk)
        case_study.delete()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="case_studies",
            message="Case study soft deleted.",
            target_type="case_studies.CaseStudy",
            target_id=case_study_id,
            after={"is_deleted": True},
        )
