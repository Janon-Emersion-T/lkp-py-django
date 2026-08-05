from datetime import timedelta
from decimal import Decimal
from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .calculations import (
    calculate_item,
    calculate_quotation_totals,
)
from .models import (
    Quotation,
    QuotationEvent,
    QuotationItem,
    QuotationRecipient,
    QuotationStatus,
)


class QuotationService:
    @staticmethod
    def generate_number() -> str:
        year = timezone.localdate().year
        prefix = f"LKP-QT-{year}-"

        latest = (
            Quotation.all_objects.filter(
                quotation_number__startswith=prefix,
            )
            .order_by("-quotation_number")
            .values_list(
                "quotation_number",
                flat=True,
            )
            .first()
        )

        if latest:
            try:
                sequence = int(
                    latest.rsplit("-", 1)[1]
                ) + 1
            except ValueError:
                sequence = (
                    Quotation.all_objects.filter(
                        quotation_number__startswith=prefix,
                    ).count()
                    + 1
                )
        else:
            sequence = 1

        return f"{prefix}{sequence:05d}"

    @staticmethod
    def create_event(
        *,
        quotation: Quotation,
        event_type: str,
        description: str,
        actor=None,
        metadata: dict[str, Any] | None = None,
    ) -> QuotationEvent:
        return QuotationEvent.objects.create(
            quotation=quotation,
            event_type=event_type,
            description=description,
            metadata=metadata or {},
            created_by=actor,
            updated_by=actor,
        )

    @staticmethod
    def recalculate(
        quotation: Quotation,
    ) -> Quotation:
        for item in quotation.items.all():
            calculate_item(item)
            item.save(
                update_fields=[
                    "subtotal",
                    "tax_amount",
                    "total_amount",
                    "updated_at",
                ],
            )

        calculate_quotation_totals(quotation)

        quotation.save(
            update_fields=[
                "subtotal",
                "discount_amount",
                "tax_amount",
                "total_amount",
                "updated_at",
            ],
        )

        return quotation

    @staticmethod
    @transaction.atomic
    def create_quotation(
        *,
        request,
        values: dict[str, Any],
        items: list[dict[str, Any]],
        recipients: list[dict[str, Any]] | None = None,
    ) -> Quotation:
        values.setdefault(
            "quotation_number",
            QuotationService.generate_number(),
        )

        values.setdefault(
            "expiry_date",
            timezone.localdate() + timedelta(days=14),
        )

        quotation = Quotation.objects.create(
            **values,
            created_by=request.auth,
            updated_by=request.auth,
        )

        for index, item_values in enumerate(items):
            item = QuotationItem(
                quotation=quotation,
                sort_order=item_values.pop(
                    "sort_order",
                    index,
                ),
                created_by=request.auth,
                updated_by=request.auth,
                **item_values,
            )

            calculate_item(item)
            item.save()

        for recipient_values in recipients or []:
            QuotationRecipient.objects.create(
                quotation=quotation,
                created_by=request.auth,
                updated_by=request.auth,
                **recipient_values,
            )

        QuotationService.recalculate(quotation)

        QuotationService.create_event(
            quotation=quotation,
            event_type="created",
            description="Quotation created.",
            actor=request.auth,
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="quotation_created",
            module="quotations",
            description="Quotation created.",
            entity_type="quotations.Quotation",
            entity_id=str(quotation.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="quotations",
            message="Quotation created.",
            target_type="quotations.Quotation",
            target_id=str(quotation.pk),
            after={
                "quotation_number": (
                    quotation.quotation_number
                ),
                "client_id": str(
                    quotation.client_id
                ),
                "status": quotation.status,
                "currency": quotation.currency,
                "subtotal": str(
                    quotation.subtotal
                ),
                "total_amount": str(
                    quotation.total_amount
                ),
            },
        )

        return quotation

    @staticmethod
    @transaction.atomic
    def update_quotation(
        *,
        request,
        quotation: Quotation,
        values: dict[str, Any],
        items: list[dict[str, Any]],
        recipients: list[dict[str, Any]],
    ) -> Quotation:
        if quotation.status not in (
            QuotationStatus.DRAFT,
            QuotationStatus.SENT,
            QuotationStatus.VIEWED,
        ):
            raise ValueError(
                "This quotation can no longer be edited."
            )

        before = {
            "title": quotation.title,
            "status": quotation.status,
            "currency": quotation.currency,
            "total_amount": str(quotation.total_amount),
        }

        for field, value in values.items():
            setattr(quotation, field, value)

        quotation.updated_by = request.auth
        quotation.save()

        quotation.items.all().delete()
        quotation.recipients.all().delete()

        for index, item_values in enumerate(items):
            item = QuotationItem(
                quotation=quotation,
                sort_order=item_values.pop(
                    "sort_order",
                    index,
                ),
                created_by=request.auth,
                updated_by=request.auth,
                **item_values,
            )
            calculate_item(item)
            item.save()

        for recipient_values in recipients:
            QuotationRecipient.objects.create(
                quotation=quotation,
                created_by=request.auth,
                updated_by=request.auth,
                **recipient_values,
            )

        QuotationService.recalculate(quotation)

        QuotationService.create_event(
            quotation=quotation,
            event_type="updated",
            description="Quotation updated.",
            actor=request.auth,
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="quotations",
            message="Quotation updated.",
            target_type="quotations.Quotation",
            target_id=str(quotation.pk),
            before=before,
            after={
                "title": quotation.title,
                "status": quotation.status,
                "currency": quotation.currency,
                "total_amount": str(quotation.total_amount),
            },
        )

        return quotation

    @staticmethod
    @transaction.atomic
    def duplicate(
        *,
        request,
        quotation: Quotation,
    ) -> Quotation:
        duplicate = Quotation.objects.create(
            quotation_number=(
                QuotationService.generate_number()
            ),
            client=quotation.client,
            lead=quotation.lead,
            title=f"{quotation.title} — Copy",
            subject=quotation.subject,
            description=quotation.description,
            status=QuotationStatus.DRAFT,
            issue_date=timezone.localdate(),
            expiry_date=(
                timezone.localdate()
                + timedelta(days=14)
            ),
            currency=quotation.currency,
            discount_amount=(
                quotation.discount_amount
            ),
            tax_amount=Decimal("0.00"),
            terms=quotation.terms,
            notes=quotation.notes,
            duplicated_from=quotation,
            created_by=request.auth,
            updated_by=request.auth,
        )

        for item in quotation.items.all():
            copied_item = QuotationItem(
                quotation=duplicate,
                title=item.title,
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                discount_amount=(
                    item.discount_amount
                ),
                tax_rate=item.tax_rate,
                sort_order=item.sort_order,
                created_by=request.auth,
                updated_by=request.auth,
            )

            calculate_item(copied_item)
            copied_item.save()

        for recipient in quotation.recipients.all():
            QuotationRecipient.objects.create(
                quotation=duplicate,
                name=recipient.name,
                email=recipient.email,
                is_primary=recipient.is_primary,
                created_by=request.auth,
                updated_by=request.auth,
            )

        QuotationService.recalculate(duplicate)

        QuotationService.create_event(
            quotation=duplicate,
            event_type="duplicated",
            description=(
                "Quotation duplicated from "
                f"{quotation.quotation_number}."
            ),
            actor=request.auth,
            metadata={
                "source_quotation_id": str(
                    quotation.pk
                ),
            },
        )

        return duplicate

    @staticmethod
    @transaction.atomic
    def mark_sent(
        *,
        request,
        quotation: Quotation,
    ) -> Quotation:
        if quotation.status not in (
            QuotationStatus.DRAFT,
            QuotationStatus.VIEWED,
        ):
            raise ValueError(
                "Only draft or viewed quotations can be sent."
            )

        quotation.status = QuotationStatus.SENT
        quotation.sent_at = timezone.now()
        quotation.updated_by = request.auth
        quotation.save(
            update_fields=[
                "status",
                "sent_at",
                "updated_by",
                "updated_at",
            ],
        )

        QuotationService.create_event(
            quotation=quotation,
            event_type="sent",
            description="Quotation marked as sent.",
            actor=request.auth,
        )

        return quotation

    @staticmethod
    def accept(
        *,
        request,
        quotation: Quotation,
        accepted_by_name: str,
        accepted_by_email: str,
    ) -> Quotation:
        if quotation.status in (
            QuotationStatus.REJECTED,
            QuotationStatus.CANCELLED,
            QuotationStatus.EXPIRED,
        ):
            raise ValueError(
                "This quotation cannot be accepted."
            )

        if quotation.is_expired:
            quotation.status = QuotationStatus.EXPIRED
            quotation.updated_by = request.auth
            quotation.save(
                update_fields=[
                    "status",
                    "updated_by",
                    "updated_at",
                ],
            )

            QuotationService.create_event(
                quotation=quotation,
                event_type="expired",
                description=(
                    "Quotation expired before acceptance."
                ),
                actor=request.auth,
            )

            raise ValueError(
                "This quotation has expired."
            )

        with transaction.atomic():
            quotation.status = QuotationStatus.ACCEPTED
            quotation.accepted_at = timezone.now()
            quotation.accepted_by_name = (
                accepted_by_name.strip()
            )
            quotation.accepted_by_email = (
                accepted_by_email.strip().lower()
            )
            quotation.updated_by = request.auth

            quotation.save(
                update_fields=[
                    "status",
                    "accepted_at",
                    "accepted_by_name",
                    "accepted_by_email",
                    "updated_by",
                    "updated_at",
                ],
            )

            QuotationService.create_event(
                quotation=quotation,
                event_type="accepted",
                description="Quotation accepted.",
                actor=request.auth,
                metadata={
                    "accepted_by_name": (
                        quotation.accepted_by_name
                    ),
                    "accepted_by_email": (
                        quotation.accepted_by_email
                    ),
                },
            )

            log_activity(
                request=request,
                actor=request.auth,
                action="quotation_accepted",
                module="quotations",
                description="Quotation accepted.",
                entity_type="quotations.Quotation",
                entity_id=str(quotation.pk),
            )

            log_audit_event(
                request=request,
                actor=request.auth,
                event_type=AuditEventType.RECORD_UPDATED,
                module="quotations",
                message="Quotation accepted.",
                target_type="quotations.Quotation",
                target_id=str(quotation.pk),
                after={
                    "status": quotation.status,
                    "accepted_by_name": (
                        quotation.accepted_by_name
                    ),
                    "accepted_by_email": (
                        quotation.accepted_by_email
                    ),
                },
            )

            return quotation

    @staticmethod
    @transaction.atomic
    def reject(
        *,
        request,
        quotation: Quotation,
        reason: str = "",
    ) -> Quotation:
        if quotation.status == QuotationStatus.ACCEPTED:
            raise ValueError(
                "An accepted quotation cannot be rejected."
            )

        quotation.status = QuotationStatus.REJECTED
        quotation.updated_by = request.auth
        quotation.save(
            update_fields=[
                "status",
                "updated_by",
                "updated_at",
            ],
        )

        QuotationService.create_event(
            quotation=quotation,
            event_type="rejected",
            description="Quotation rejected.",
            actor=request.auth,
            metadata={
                "reason": reason,
            },
        )

        return quotation

    @staticmethod
    @transaction.atomic
    def mark_expired_quotations() -> int:
        quotations = list(
            Quotation.objects.filter(
                expiry_date__lt=timezone.localdate(),
                status__in=(
                    QuotationStatus.DRAFT,
                    QuotationStatus.SENT,
                    QuotationStatus.VIEWED,
                ),
            )
        )

        for quotation in quotations:
            quotation.status = QuotationStatus.EXPIRED
            quotation.save(
                update_fields=[
                    "status",
                    "updated_at",
                ],
            )

            QuotationService.create_event(
                quotation=quotation,
                event_type="expired",
                description="Quotation expired.",
            )

        return len(quotations)

    @staticmethod
    @transaction.atomic
    def soft_delete(
        *,
        request,
        quotation: Quotation,
    ) -> None:
        quotation_id = str(quotation.pk)
        quotation.delete()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="quotations",
            message="Quotation soft deleted.",
            target_type="quotations.Quotation",
            target_id=quotation_id,
            after={
                "is_deleted": True,
            },
        )
