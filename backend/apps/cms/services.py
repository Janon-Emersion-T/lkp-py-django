from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    ContentStatus,
    Page,
    PageRevision,
    PageSeo,
    PublishingEvent,
    PublishingEventType,
    Redirect,
)


class CmsService:
    @staticmethod
    def create_publishing_event(
        *,
        page: Page,
        event_type: str,
        description: str,
        actor=None,
        metadata: dict[str, Any] | None = None,
    ) -> PublishingEvent:
        return PublishingEvent.objects.create(
            page=page,
            event_type=event_type,
            description=description,
            metadata=metadata or {},
            created_by=actor,
            updated_by=actor,
        )

    @staticmethod
    def create_revision(
        *,
        page: Page,
        actor,
        change_summary: str = "",
    ) -> PageRevision:
        latest = (
            PageRevision.all_objects.filter(page=page)
            .order_by("-revision_number")
            .values_list("revision_number", flat=True)
            .first()
        )

        revision_number = (latest or 0) + 1

        revision = PageRevision.objects.create(
            page=page,
            revision_number=revision_number,
            title=page.title,
            excerpt=page.excerpt,
            content=page.content,
            status=page.status,
            change_summary=change_summary,
            created_by=actor,
            updated_by=actor,
        )

        page.current_revision_number = revision_number
        page.save(
            update_fields=[
                "current_revision_number",
                "updated_at",
            ],
        )

        return revision

    @staticmethod
    @transaction.atomic
    def create_page(
        *,
        request,
        values: dict[str, Any],
        seo_values: dict[str, Any] | None = None,
    ) -> Page:
        page = Page.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        PageSeo.objects.create(
            page=page,
            created_by=request.auth,
            updated_by=request.auth,
            **(seo_values or {}),
        )

        CmsService.create_revision(
            page=page,
            actor=request.auth,
            change_summary="Initial page revision.",
        )

        CmsService.create_publishing_event(
            page=page,
            event_type=PublishingEventType.CREATED,
            description="Page created.",
            actor=request.auth,
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="cms_page_created",
            module="cms",
            description="CMS page created.",
            entity_type="cms.Page",
            entity_id=str(page.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="cms",
            message="CMS page created.",
            target_type="cms.Page",
            target_id=str(page.pk),
            after={
                "title": page.title,
                "slug": page.slug,
                "page_type": page.page_type,
                "status": page.status,
            },
        )

        return page

    @staticmethod
    @transaction.atomic
    def update_page(
        *,
        request,
        page: Page,
        values: dict[str, Any],
        seo_values: dict[str, Any] | None = None,
        change_summary: str = "",
    ) -> Page:
        before = {
            "title": page.title,
            "slug": page.slug,
            "status": page.status,
            "current_revision_number": (
                page.current_revision_number
            ),
        }

        for field, value in values.items():
            setattr(page, field, value)

        page.updated_by = request.auth
        page.save()

        if seo_values is not None:
            seo, _ = PageSeo.objects.get_or_create(
                page=page,
                defaults={
                    "created_by": request.auth,
                    "updated_by": request.auth,
                },
            )

            for field, value in seo_values.items():
                setattr(seo, field, value)

            seo.updated_by = request.auth
            seo.save()

        revision = CmsService.create_revision(
            page=page,
            actor=request.auth,
            change_summary=change_summary,
        )

        CmsService.create_publishing_event(
            page=page,
            event_type=PublishingEventType.UPDATED,
            description="Page updated.",
            actor=request.auth,
            metadata={
                "revision_number": revision.revision_number,
            },
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="cms",
            message="CMS page updated.",
            target_type="cms.Page",
            target_id=str(page.pk),
            before=before,
            after={
                "title": page.title,
                "slug": page.slug,
                "status": page.status,
                "current_revision_number": (
                    page.current_revision_number
                ),
            },
        )

        return page

    @staticmethod
    @transaction.atomic
    def publish_page(
        *,
        request,
        page: Page,
    ) -> Page:
        page.status = ContentStatus.PUBLISHED
        page.published_at = timezone.now()
        page.scheduled_for = None
        page.updated_by = request.auth
        page.save(
            update_fields=[
                "status",
                "published_at",
                "scheduled_for",
                "updated_by",
                "updated_at",
            ],
        )

        CmsService.create_revision(
            page=page,
            actor=request.auth,
            change_summary="Page published.",
        )

        CmsService.create_publishing_event(
            page=page,
            event_type=PublishingEventType.PUBLISHED,
            description="Page published.",
            actor=request.auth,
        )

        return page

    @staticmethod
    @transaction.atomic
    def schedule_page(
        *,
        request,
        page: Page,
        scheduled_for,
    ) -> Page:
        if scheduled_for <= timezone.now():
            raise ValueError(
                "Scheduled publication time must be in the future."
            )

        page.status = ContentStatus.SCHEDULED
        page.scheduled_for = scheduled_for
        page.published_at = None
        page.updated_by = request.auth
        page.save(
            update_fields=[
                "status",
                "scheduled_for",
                "published_at",
                "updated_by",
                "updated_at",
            ],
        )

        CmsService.create_publishing_event(
            page=page,
            event_type=PublishingEventType.SCHEDULED,
            description="Page publication scheduled.",
            actor=request.auth,
            metadata={
                "scheduled_for": scheduled_for.isoformat(),
            },
        )

        return page

    @staticmethod
    @transaction.atomic
    def process_scheduled_pages() -> int:
        pages = list(
            Page.objects.filter(
                status=ContentStatus.SCHEDULED,
                scheduled_for__lte=timezone.now(),
            )
        )

        for page in pages:
            page.status = ContentStatus.PUBLISHED
            page.published_at = page.scheduled_for
            page.scheduled_for = None
            page.save(
                update_fields=[
                    "status",
                    "published_at",
                    "scheduled_for",
                    "updated_at",
                ],
            )

            CmsService.create_publishing_event(
                page=page,
                event_type=PublishingEventType.PUBLISHED,
                description=(
                    "Scheduled page automatically published."
                ),
            )

        return len(pages)

    @staticmethod
    @transaction.atomic
    def restore_revision(
        *,
        request,
        page: Page,
        revision: PageRevision,
    ) -> Page:
        if revision.page_id != page.pk:
            raise ValueError(
                "Revision does not belong to this page."
            )

        page.title = revision.title
        page.excerpt = revision.excerpt
        page.content = revision.content
        page.status = revision.status
        page.updated_by = request.auth
        page.save()

        restored_revision = CmsService.create_revision(
            page=page,
            actor=request.auth,
            change_summary=(
                f"Restored revision "
                f"{revision.revision_number}."
            ),
        )

        CmsService.create_publishing_event(
            page=page,
            event_type=PublishingEventType.RESTORED,
            description="Page revision restored.",
            actor=request.auth,
            metadata={
                "source_revision": revision.revision_number,
                "new_revision": (
                    restored_revision.revision_number
                ),
            },
        )

        return page

    @staticmethod
    @transaction.atomic
    def create_redirect(
        *,
        request,
        values: dict[str, Any],
    ) -> Redirect:
        redirect = Redirect.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="cms",
            message="CMS redirect created.",
            target_type="cms.Redirect",
            target_id=str(redirect.pk),
            after={
                "source_path": redirect.source_path,
                "destination_url": redirect.destination_url,
                "redirect_type": redirect.redirect_type,
            },
        )

        return redirect

    @staticmethod
    @transaction.atomic
    def soft_delete_page(
        *,
        request,
        page: Page,
    ) -> None:
        page_id = str(page.pk)
        page.delete()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="cms",
            message="CMS page soft deleted.",
            target_type="cms.Page",
            target_id=page_id,
            after={
                "is_deleted": True,
            },
        )
