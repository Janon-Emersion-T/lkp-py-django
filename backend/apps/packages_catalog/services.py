from decimal import Decimal
from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    Package,
    PackageAddon,
    PackageFaq,
    PackageFeature,
    PackageRevision,
    PackageSeo,
    PackageStatus,
    PackageTargetAudience,
)


class PackageCatalogService:
    @staticmethod
    def snapshot(package: Package) -> dict[str, Any]:
        try:
            seo = package.seo
        except PackageSeo.DoesNotExist:
            seo = None

        return {
            "name": package.name,
            "slug": package.slug,
            "category": package.category,
            "service_id": (
                str(package.service_id)
                if package.service_id
                else None
            ),
            "short_description": package.short_description,
            "description": package.description,
            "pricing_type": package.pricing_type,
            "price": str(package.price),
            "compare_at_price": (
                str(package.compare_at_price)
                if package.compare_at_price is not None
                else None
            ),
            "currency": package.currency,
            "billing_cycle": package.billing_cycle,
            "delivery_time": package.delivery_time,
            "revisions_included": (
                package.revisions_included
            ),
            "support_period_days": (
                package.support_period_days
            ),
            "status": package.status,
            "is_featured": package.is_featured,
            "is_popular": package.is_popular,
            "is_active": package.is_active,
            "sort_order": package.sort_order,
            "badge_text": package.badge_text,
            "cta_label": package.cta_label,
            "cta_url": package.cta_url,
            "features": [
                {
                    "title": item.title,
                    "description": item.description,
                    "is_included": item.is_included,
                    "value": item.value,
                    "icon": item.icon,
                    "sort_order": item.sort_order,
                }
                for item in package.features.all()
            ],
            "addons": [
                {
                    "name": item.name,
                    "description": item.description,
                    "price": str(item.price),
                    "currency": item.currency,
                    "billing_cycle": item.billing_cycle,
                    "is_active": item.is_active,
                    "sort_order": item.sort_order,
                }
                for item in package.addons.all()
            ],
            "target_audiences": [
                {
                    "title": item.title,
                    "description": item.description,
                    "sort_order": item.sort_order,
                }
                for item in package.target_audiences.all()
            ],
            "faqs": [
                {
                    "question": item.question,
                    "answer": item.answer,
                    "sort_order": item.sort_order,
                }
                for item in package.faqs.all()
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
                    "structured_data": seo.structured_data,
                }
                if seo
                else {}
            ),
        }

    @staticmethod
    def create_revision(
        *,
        package: Package,
        actor,
        change_summary: str = "",
    ) -> PackageRevision:
        latest = (
            PackageRevision.all_objects.filter(
                package=package,
            )
            .order_by("-revision_number")
            .values_list("revision_number", flat=True)
            .first()
        )

        revision_number = (latest or 0) + 1

        revision = PackageRevision.objects.create(
            package=package,
            revision_number=revision_number,
            snapshot=PackageCatalogService.snapshot(
                package
            ),
            change_summary=change_summary,
            created_by=actor,
            updated_by=actor,
        )

        package.current_revision_number = (
            revision_number
        )
        package.save(
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
        package: Package,
        features: list[dict[str, Any]],
        addons: list[dict[str, Any]],
        target_audiences: list[dict[str, Any]],
        faqs: list[dict[str, Any]],
    ) -> None:
        package.features.all().delete()
        package.addons.all().delete()
        package.target_audiences.all().delete()
        package.faqs.all().delete()

        for index, values in enumerate(features):
            PackageFeature.objects.create(
                package=package,
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

        for index, values in enumerate(addons):
            PackageAddon.objects.create(
                package=package,
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

        for index, values in enumerate(
            target_audiences
        ):
            PackageTargetAudience.objects.create(
                package=package,
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
            PackageFaq.objects.create(
                package=package,
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
    def create_package(
        *,
        request,
        values: dict[str, Any],
        features: list[dict[str, Any]],
        addons: list[dict[str, Any]],
        target_audiences: list[dict[str, Any]],
        faqs: list[dict[str, Any]],
        seo_values: dict[str, Any],
    ) -> Package:
        values["currency"] = values.get(
            "currency",
            "LKR",
        ).upper()

        values["price"] = Decimal(
            str(values.get("price", "0.00"))
        )

        package = Package.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        PackageSeo.objects.create(
            package=package,
            created_by=request.auth,
            updated_by=request.auth,
            **seo_values,
        )

        PackageCatalogService.replace_related_content(
            request=request,
            package=package,
            features=features,
            addons=addons,
            target_audiences=target_audiences,
            faqs=faqs,
        )

        PackageCatalogService.create_revision(
            package=package,
            actor=request.auth,
            change_summary="Initial package revision.",
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="package_created",
            module="packages_catalog",
            description="Package created.",
            entity_type="packages_catalog.Package",
            entity_id=str(package.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="packages_catalog",
            message="Package created.",
            target_type="packages_catalog.Package",
            target_id=str(package.pk),
            after={
                "name": package.name,
                "slug": package.slug,
                "category": package.category,
                "status": package.status,
                "price": str(package.price),
                "currency": package.currency,
            },
        )

        return package

    @staticmethod
    @transaction.atomic
    def update_package(
        *,
        request,
        package: Package,
        values: dict[str, Any],
        features: list[dict[str, Any]],
        addons: list[dict[str, Any]],
        target_audiences: list[dict[str, Any]],
        faqs: list[dict[str, Any]],
        seo_values: dict[str, Any],
        change_summary: str = "",
    ) -> Package:
        before = {
            "name": package.name,
            "slug": package.slug,
            "status": package.status,
            "price": str(package.price),
            "current_revision_number": (
                package.current_revision_number
            ),
        }

        for field, value in values.items():
            setattr(package, field, value)

        package.currency = package.currency.upper()
        package.updated_by = request.auth
        package.save()

        seo, _ = PackageSeo.objects.get_or_create(
            package=package,
            defaults={
                "created_by": request.auth,
                "updated_by": request.auth,
            },
        )

        for field, value in seo_values.items():
            setattr(seo, field, value)

        seo.updated_by = request.auth
        seo.save()

        PackageCatalogService.replace_related_content(
            request=request,
            package=package,
            features=features,
            addons=addons,
            target_audiences=target_audiences,
            faqs=faqs,
        )

        PackageCatalogService.create_revision(
            package=package,
            actor=request.auth,
            change_summary=change_summary,
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="packages_catalog",
            message="Package updated.",
            target_type="packages_catalog.Package",
            target_id=str(package.pk),
            before=before,
            after={
                "name": package.name,
                "slug": package.slug,
                "status": package.status,
                "price": str(package.price),
                "current_revision_number": (
                    package.current_revision_number
                ),
            },
        )

        return package

    @staticmethod
    @transaction.atomic
    def publish_package(
        *,
        request,
        package: Package,
    ) -> Package:
        package.status = PackageStatus.PUBLISHED
        package.published_at = timezone.now()
        package.scheduled_for = None
        package.updated_by = request.auth
        package.save(
            update_fields=[
                "status",
                "published_at",
                "scheduled_for",
                "updated_by",
                "updated_at",
            ],
        )

        PackageCatalogService.create_revision(
            package=package,
            actor=request.auth,
            change_summary="Package published.",
        )

        return package

    @staticmethod
    @transaction.atomic
    def schedule_package(
        *,
        request,
        package: Package,
        scheduled_for,
    ) -> Package:
        if scheduled_for <= timezone.now():
            raise ValueError(
                "Scheduled publication time must be in the future."
            )

        package.status = PackageStatus.SCHEDULED
        package.scheduled_for = scheduled_for
        package.published_at = None
        package.updated_by = request.auth
        package.save(
            update_fields=[
                "status",
                "scheduled_for",
                "published_at",
                "updated_by",
                "updated_at",
            ],
        )

        return package

    @staticmethod
    @transaction.atomic
    def process_scheduled_packages() -> int:
        packages = list(
            Package.objects.filter(
                is_active=True,
                status=PackageStatus.SCHEDULED,
                scheduled_for__lte=timezone.now(),
            )
        )

        for package in packages:
            package.status = PackageStatus.PUBLISHED
            package.published_at = package.scheduled_for
            package.scheduled_for = None
            package.save(
                update_fields=[
                    "status",
                    "published_at",
                    "scheduled_for",
                    "updated_at",
                ],
            )

        return len(packages)

    @staticmethod
    @transaction.atomic
    def soft_delete_package(
        *,
        request,
        package: Package,
    ) -> None:
        package_id = str(package.pk)
        package.delete()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="packages_catalog",
            message="Package soft deleted.",
            target_type="packages_catalog.Package",
            target_id=package_id,
            after={"is_deleted": True},
        )
