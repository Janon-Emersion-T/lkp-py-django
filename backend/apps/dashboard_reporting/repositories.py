from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from .models import DashboardReportSnapshot


ALLOWED_ENVIRONMENTS = {
    "development",
    "staging",
    "production",
    "test",
}


def normalize_environment(environment):
    normalized = (environment or "production").strip().lower()

    if normalized not in ALLOWED_ENVIRONMENTS:
        allowed = ", ".join(sorted(ALLOWED_ENVIRONMENTS))
        raise ValueError(
            f"Invalid dashboard reporting environment. "
            f"Allowed values: {allowed}."
        )

    return normalized


class DashboardSnapshotRepository:
    @staticmethod
    def queryset():
        return DashboardReportSnapshot.objects.all()

    @classmethod
    def latest(
        cls,
        *,
        report_type,
        period_preset,
        date_from,
        date_to,
        environment,
        include_expired=False,
    ):
        queryset = cls.queryset().filter(
            report_type=report_type,
            period_preset=period_preset,
            date_from=date_from,
            date_to=date_to,
            environment=environment,
            is_active=True,
        )

        if not include_expired:
            now = timezone.now()
            queryset = queryset.filter(
                models_expiry_filter(now),
            )

        return queryset.order_by(
            "-version",
            "-generated_at",
        ).first()

    @classmethod
    def list_snapshots(
        cls,
        *,
        report_type=None,
        environment=None,
        active_only=False,
    ):
        queryset = cls.queryset()

        if report_type:
            queryset = queryset.filter(
                report_type=report_type,
            )

        if environment:
            queryset = queryset.filter(
                environment=environment,
            )

        if active_only:
            queryset = queryset.filter(is_active=True)

        return queryset.order_by(
            "report_type",
            "-version",
            "-generated_at",
        )

    @classmethod
    def next_version(
        cls,
        *,
        report_type,
        period_preset,
        date_from,
        date_to,
        environment,
    ):
        current = (
            cls.queryset()
            .filter(
                report_type=report_type,
                period_preset=period_preset,
                date_from=date_from,
                date_to=date_to,
                environment=environment,
            )
            .aggregate(maximum=Max("version"))
            .get("maximum")
        )

        return (current or 0) + 1

    @classmethod
    @transaction.atomic
    def create_snapshot(
        cls,
        *,
        report_type,
        period_preset,
        date_from,
        date_to,
        environment,
        payload,
        checksum,
        generated_at,
        expires_at,
        metadata=None,
        actor=None,
    ):
        cls.queryset().select_for_update().filter(
            report_type=report_type,
            period_preset=period_preset,
            date_from=date_from,
            date_to=date_to,
            environment=environment,
            is_active=True,
        ).update(
            is_active=False,
            updated_by=actor,
        )

        version = cls.next_version(
            report_type=report_type,
            period_preset=period_preset,
            date_from=date_from,
            date_to=date_to,
            environment=environment,
        )

        return cls.queryset().create(
            report_type=report_type,
            period_preset=period_preset,
            date_from=date_from,
            date_to=date_to,
            environment=environment,
            version=version,
            payload=payload,
            checksum=checksum,
            generated_at=generated_at,
            expires_at=expires_at,
            is_active=True,
            metadata=metadata or {},
            created_by=actor,
            updated_by=actor,
        )

    @classmethod
    def invalidate(
        cls,
        *,
        report_type=None,
        environment=None,
        actor=None,
    ):
        queryset = cls.queryset().filter(is_active=True)

        if report_type:
            queryset = queryset.filter(
                report_type=report_type,
            )

        if environment:
            queryset = queryset.filter(
                environment=environment,
            )

        return queryset.update(
            is_active=False,
            updated_by=actor,
        )


def models_expiry_filter(now):
    from django.db.models import Q

    return (
        Q(expires_at__isnull=True)
        | Q(expires_at__gt=now)
    )


class ExecutiveDashboardRepository:
    TERMINAL_LEAD_STATUSES = {
        "won",
        "lost",
        "spam",
    }

    OPEN_ENQUIRY_STATUSES = {
        "new",
        "assigned",
        "contacted",
        "qualified",
        "proposal_sent",
    }

    ACTIVE_PROJECT_STATUSES = {
        "planning",
        "development",
        "testing",
        "review",
    }

    OPEN_TASK_STATUSES = {
        "todo",
        "in_progress",
        "testing",
        "review",
    }

    OUTSTANDING_INVOICE_STATUSES = {
        "sent",
        "partially_paid",
        "overdue",
    }

    @staticmethod
    def _model(app_label, model_name):
        from django.apps import apps

        return apps.get_model(
            app_label,
            model_name,
        )

    @staticmethod
    def _currency_rows(queryset, amount_field):
        from django.db.models import DecimalField, Sum, Value
        from django.db.models.functions import Coalesce

        return list(
            queryset.values("currency")
            .annotate(
                amount=Coalesce(
                    Sum(amount_field),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                )
            )
            .order_by("currency")
        )

    @classmethod
    def client_metrics(cls, period):
        from django.db.models import Count, Q

        Client = cls._model(
            "clients",
            "Client",
        )

        return Client.objects.aggregate(
            total_clients=Count("id"),
            active_clients=Count(
                "id",
                filter=Q(status="active"),
            ),
            new_clients=Count(
                "id",
                filter=Q(
                    created_at__gte=period.datetime_from,
                    created_at__lt=period.datetime_to,
                ),
            ),
        )

    @classmethod
    def lead_metrics(cls, period, now):
        from django.db.models import Count, Q

        Lead = cls._model(
            "crm",
            "Lead",
        )

        metrics = Lead.objects.aggregate(
            total_leads=Count("id"),
            qualified_leads=Count(
                "id",
                filter=Q(
                    status__in={
                        "proposal_sent",
                        "negotiation",
                        "won",
                    }
                ),
            ),
            won_leads=Count(
                "id",
                filter=Q(status="won"),
            ),
            lost_leads=Count(
                "id",
                filter=Q(status="lost"),
            ),
            overdue_follow_ups=Count(
                "id",
                filter=Q(
                    next_follow_up_at__lt=now,
                )
                & ~Q(
                    status__in=cls.TERMINAL_LEAD_STATUSES,
                ),
            ),
            period_leads=Count(
                "id",
                filter=Q(
                    created_at__gte=period.datetime_from,
                    created_at__lt=period.datetime_to,
                ),
            ),
        )

        closed = (
            metrics["won_leads"]
            + metrics["lost_leads"]
        )

        metrics["lead_conversion_rate"] = (
            round(
                metrics["won_leads"]
                / closed
                * 100,
                2,
            )
            if closed
            else 0.0
        )

        return metrics

    @classmethod
    def quotation_metrics(cls, period):
        from django.db.models import Count, Q

        Quotation = cls._model(
            "quotations",
            "Quotation",
        )

        metrics = Quotation.objects.aggregate(
            total_quotations=Count("id"),
            accepted_quotations=Count(
                "id",
                filter=Q(status="accepted"),
            ),
            period_quotations=Count(
                "id",
                filter=Q(
                    issue_date__gte=period.date_from,
                    issue_date__lte=period.date_to,
                ),
            ),
        )

        metrics["quotation_value_by_currency"] = (
            cls._currency_rows(
                Quotation.objects.all(),
                "total_amount",
            )
        )

        metrics[
            "accepted_quotation_value_by_currency"
        ] = cls._currency_rows(
            Quotation.objects.filter(
                status="accepted",
            ),
            "total_amount",
        )

        return metrics

    @classmethod
    def project_metrics(cls, today, period):
        from django.db.models import Count, Q

        Project = cls._model(
            "projects",
            "Project",
        )

        return Project.objects.aggregate(
            active_projects=Count(
                "id",
                filter=Q(
                    status__in=cls.ACTIVE_PROJECT_STATUSES,
                ),
            ),
            completed_projects=Count(
                "id",
                filter=Q(status="completed"),
            ),
            overdue_projects=Count(
                "id",
                filter=Q(
                    deadline__lt=today,
                    status__in=cls.ACTIVE_PROJECT_STATUSES,
                ),
            ),
            completed_in_period=Count(
                "id",
                filter=Q(
                    completed_at__gte=period.datetime_from,
                    completed_at__lt=period.datetime_to,
                    status="completed",
                ),
            ),
        )

    @classmethod
    def task_metrics(cls, today, period):
        from django.db.models import Count, Q

        Task = cls._model(
            "tasks",
            "Task",
        )

        return Task.objects.aggregate(
            open_tasks=Count(
                "id",
                filter=Q(
                    status__in=cls.OPEN_TASK_STATUSES,
                ),
            ),
            overdue_tasks=Count(
                "id",
                filter=Q(
                    due_date__lt=today,
                    status__in=cls.OPEN_TASK_STATUSES,
                ),
            ),
            completed_tasks=Count(
                "id",
                filter=Q(status="completed"),
            ),
            completed_in_period=Count(
                "id",
                filter=Q(
                    completed_at__gte=period.datetime_from,
                    completed_at__lt=period.datetime_to,
                    status="completed",
                ),
            ),
        )

    @classmethod
    def finance_metrics(cls, today, period):
        from django.db.models import Count, Q

        Invoice = cls._model(
            "finance",
            "Invoice",
        )
        Payment = cls._model(
            "finance",
            "Payment",
        )
        Account = cls._model(
            "finance",
            "Account",
        )

        invoice_metrics = Invoice.objects.aggregate(
            outstanding_invoices=Count(
                "id",
                filter=Q(
                    status__in=(
                        cls.OUTSTANDING_INVOICE_STATUSES
                    )
                ),
            ),
            overdue_invoices=Count(
                "id",
                filter=(
                    Q(status="overdue")
                    | Q(
                        due_date__lt=today,
                        status__in={
                            "sent",
                            "partially_paid",
                        },
                    )
                ),
            ),
        )

        outstanding_values = cls._currency_rows(
            Invoice.objects.filter(
                status__in=(
                    cls.OUTSTANDING_INVOICE_STATUSES
                ),
            ),
            "balance_due",
        )

        overdue_values = cls._currency_rows(
            Invoice.objects.filter(
                Q(status="overdue")
                | Q(
                    due_date__lt=today,
                    status__in={
                        "sent",
                        "partially_paid",
                    },
                )
            ),
            "balance_due",
        )

        revenue_by_currency = cls._currency_rows(
            Payment.objects.filter(
                status="completed",
                payment_date__gte=period.date_from,
                payment_date__lte=period.date_to,
            ),
            "amount",
        )

        asset_balances = list(
            Account.objects.filter(
                account_type="asset",
                is_active=True,
            )
            .values(
                "id",
                "name",
                "currency",
                "current_balance",
            )
            .order_by(
                "currency",
                "name",
            )
        )

        return {
            **invoice_metrics,
            "outstanding_value_by_currency": (
                outstanding_values
            ),
            "overdue_value_by_currency": overdue_values,
            "revenue_by_currency": revenue_by_currency,
            "cash_and_bank_balances": asset_balances,
        }

    @classmethod
    def enquiry_metrics(cls, now, period):
        from django.db.models import Count, Q

        ContactEnquiry = cls._model(
            "enquiries",
            "ContactEnquiry",
        )
        QuoteEnquiry = cls._model(
            "enquiries",
            "QuoteEnquiry",
        )

        def aggregate(model):
            return model.objects.aggregate(
                open_count=Count(
                    "id",
                    filter=Q(
                        status__in=(
                            cls.OPEN_ENQUIRY_STATUSES
                        ),
                    ),
                ),
                overdue_follow_ups=Count(
                    "id",
                    filter=Q(
                        next_follow_up_at__lt=now,
                        status__in=(
                            cls.OPEN_ENQUIRY_STATUSES
                        ),
                    ),
                ),
                submitted_in_period=Count(
                    "id",
                    filter=Q(
                        submitted_at__gte=(
                            period.datetime_from
                        ),
                        submitted_at__lt=(
                            period.datetime_to
                        ),
                    ),
                ),
            )

        contact = aggregate(ContactEnquiry)
        quote = aggregate(QuoteEnquiry)

        return {
            "open_enquiries": (
                contact["open_count"]
                + quote["open_count"]
            ),
            "overdue_follow_ups": (
                contact["overdue_follow_ups"]
                + quote["overdue_follow_ups"]
            ),
            "submitted_in_period": (
                contact["submitted_in_period"]
                + quote["submitted_in_period"]
            ),
            "contact_enquiries": contact,
            "quote_enquiries": quote,
        }

    @classmethod
    def workforce_metrics(cls, now):
        from django.db.models import Count, Q, Sum, Value
        from django.db.models.functions import Coalesce

        TeamMember = cls._model(
            "team_management",
            "TeamMember",
        )
        JobListing = cls._model(
            "careers",
            "JobListing",
        )
        Subscriber = cls._model(
            "newsletter",
            "Subscriber",
        )

        people = TeamMember.objects.aggregate(
            active_team_members=Count(
                "id",
                filter=Q(
                    employment_status__in={
                        "active",
                        "on_leave",
                    },
                ),
            ),
        )

        jobs = JobListing.objects.filter(
            status="published",
            is_active=True,
        ).filter(
            Q(application_deadline__isnull=True)
            | Q(application_deadline__gte=now)
        ).aggregate(
            open_job_positions=Coalesce(
                Sum("number_of_openings"),
                Value(0),
            ),
            open_job_listings=Count("id"),
        )

        subscribers = Subscriber.objects.aggregate(
            newsletter_subscribers=Count(
                "id",
                filter=Q(status="active"),
            ),
        )

        return {
            **people,
            **jobs,
            **subscribers,
        }

    @classmethod
    def build(cls, period, now):
        today = timezone.localdate()

        client_metrics = cls.client_metrics(period)
        lead_metrics = cls.lead_metrics(
            period,
            now,
        )
        enquiry_metrics = cls.enquiry_metrics(
            now,
            period,
        )

        return {
            "clients": client_metrics,
            "crm": lead_metrics,
            "sales": cls.quotation_metrics(period),
            "projects": cls.project_metrics(
                today,
                period,
            ),
            "tasks": cls.task_metrics(
                today,
                period,
            ),
            "finance": cls.finance_metrics(
                today,
                period,
            ),
            "enquiries": enquiry_metrics,
            "workforce": cls.workforce_metrics(now),
            "summary": {
                "total_clients": (
                    client_metrics["total_clients"]
                ),
                "active_clients": (
                    client_metrics["active_clients"]
                ),
                "total_leads": (
                    lead_metrics["total_leads"]
                ),
                "qualified_leads": (
                    lead_metrics["qualified_leads"]
                ),
                "won_leads": lead_metrics["won_leads"],
                "lost_leads": (
                    lead_metrics["lost_leads"]
                ),
                "lead_conversion_rate": (
                    lead_metrics[
                        "lead_conversion_rate"
                    ]
                ),
                "open_enquiries": (
                    enquiry_metrics["open_enquiries"]
                ),
                "overdue_follow_ups": (
                    lead_metrics[
                        "overdue_follow_ups"
                    ]
                    + enquiry_metrics[
                        "overdue_follow_ups"
                    ]
                ),
            },
        }


class CrmReportingRepository:
    FUNNEL_STAGES = (
        "new",
        "contacted",
        "follow_up",
        "proposal_sent",
        "negotiation",
        "won",
        "lost",
    )

    TERMINAL_STATUSES = {
        "won",
        "lost",
        "spam",
    }

    @staticmethod
    def _lead_model():
        from django.apps import apps

        return apps.get_model("crm", "Lead")

    @classmethod
    def period_queryset(cls, period):
        Lead = cls._lead_model()

        return Lead.objects.filter(
            created_at__gte=period.datetime_from,
            created_at__lt=period.datetime_to,
        )

    @classmethod
    def summary(cls, period, now):
        from django.db.models import Count, Q

        Lead = cls._lead_model()
        period_queryset = cls.period_queryset(period)

        all_time = Lead.objects.aggregate(
            all_time_total_leads=Count("id"),
            all_time_won_leads=Count(
                "id",
                filter=Q(status="won"),
            ),
            all_time_lost_leads=Count(
                "id",
                filter=Q(status="lost"),
            ),
        )

        period_metrics = period_queryset.aggregate(
            total_leads=Count("id"),
            new_leads=Count(
                "id",
                filter=Q(status="new"),
            ),
            contacted_leads=Count(
                "id",
                filter=Q(status="contacted"),
            ),
            follow_up_leads=Count(
                "id",
                filter=Q(status="follow_up"),
            ),
            proposal_sent_leads=Count(
                "id",
                filter=Q(status="proposal_sent"),
            ),
            negotiation_leads=Count(
                "id",
                filter=Q(status="negotiation"),
            ),
            won_leads=Count(
                "id",
                filter=Q(status="won"),
            ),
            lost_leads=Count(
                "id",
                filter=Q(status="lost"),
            ),
            spam_leads=Count(
                "id",
                filter=Q(status="spam"),
            ),
            assigned_leads=Count(
                "id",
                filter=Q(assigned_to__isnull=False),
            ),
            unassigned_leads=Count(
                "id",
                filter=Q(assigned_to__isnull=True),
            ),
            overdue_follow_ups=Count(
                "id",
                filter=(
                    Q(next_follow_up_at__lt=now)
                    & ~Q(
                        status__in=cls.TERMINAL_STATUSES
                    )
                ),
            ),
        )

        closed_leads = (
            period_metrics["won_leads"]
            + period_metrics["lost_leads"]
        )

        period_metrics["closed_leads"] = closed_leads
        period_metrics["conversion_rate"] = (
            round(
                period_metrics["won_leads"]
                / closed_leads
                * 100,
                2,
            )
            if closed_leads
            else 0.0
        )

        period_metrics["win_rate_from_total"] = (
            round(
                period_metrics["won_leads"]
                / period_metrics["total_leads"]
                * 100,
                2,
            )
            if period_metrics["total_leads"]
            else 0.0
        )

        return {
            **all_time,
            **period_metrics,
        }

    @classmethod
    def leads_by_status(cls, period):
        from django.db.models import Count

        Lead = cls._lead_model()
        status_labels = dict(
            Lead._meta.get_field("status").choices
        )

        rows = list(
            cls.period_queryset(period)
            .values("status")
            .annotate(total=Count("id"))
            .order_by("status")
        )

        totals = {
            row["status"]: row["total"]
            for row in rows
        }

        return [
            {
                "status": value,
                "label": label,
                "total": totals.get(value, 0),
            }
            for value, label
            in Lead._meta.get_field("status").choices
        ]

    @classmethod
    def leads_by_source(cls, period):
        from django.db.models import Count

        Lead = cls._lead_model()

        rows = list(
            cls.period_queryset(period)
            .values("source")
            .annotate(total=Count("id"))
            .order_by("-total", "source")
        )

        source_labels = dict(
            Lead._meta.get_field("source").choices
        )

        return [
            {
                "source": row["source"],
                "label": source_labels.get(
                    row["source"],
                    row["source"],
                ),
                "total": row["total"],
            }
            for row in rows
        ]

    @classmethod
    def leads_by_owner(cls, period):
        from django.db.models import Count

        rows = list(
            cls.period_queryset(period)
            .values(
                "assigned_to_id",
                "assigned_to__username",
                "assigned_to__first_name",
                "assigned_to__last_name",
                "assigned_to__email",
            )
            .annotate(total=Count("id"))
            .order_by("-total", "assigned_to__username")
        )

        result = []

        for row in rows:
            first_name = (
                row["assigned_to__first_name"]
                or ""
            ).strip()
            last_name = (
                row["assigned_to__last_name"]
                or ""
            ).strip()
            full_name = (
                f"{first_name} {last_name}".strip()
            )

            if row["assigned_to_id"] is None:
                owner_name = "Unassigned"
            else:
                owner_name = (
                    full_name
                    or row["assigned_to__username"]
                    or row["assigned_to__email"]
                    or str(row["assigned_to_id"])
                )

            result.append(
                {
                    "owner_id": row["assigned_to_id"],
                    "owner_name": owner_name,
                    "username": (
                        row["assigned_to__username"]
                    ),
                    "email": row["assigned_to__email"],
                    "total": row["total"],
                }
            )

        return result

    @classmethod
    def conversion_funnel(cls, period):
        from django.db.models import Count

        Lead = cls._lead_model()

        rows = {
            row["status"]: row["total"]
            for row in (
                cls.period_queryset(period)
                .values("status")
                .annotate(total=Count("id"))
            )
        }

        total = sum(rows.values())

        funnel = []

        for position, status in enumerate(
            cls.FUNNEL_STAGES,
            start=1,
        ):
            count = rows.get(status, 0)

            funnel.append(
                {
                    "position": position,
                    "status": status,
                    "label": dict(
                        Lead._meta.get_field(
                            "status"
                        ).choices
                    ).get(status, status),
                    "total": count,
                    "percentage_of_total": (
                        round(count / total * 100, 2)
                        if total
                        else 0.0
                    ),
                }
            )

        return funnel

    @classmethod
    def monthly_lead_trend(cls, period):
        from django.db.models import Count
        from django.db.models.functions import TruncMonth

        rows = list(
            cls.period_queryset(period)
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )

        return [
            {
                "month": row["month"].date(),
                "total": row["total"],
            }
            for row in rows
        ]

    @classmethod
    def won_lost_trend(cls, period):
        from django.db.models import Count, Q
        from django.db.models.functions import TruncMonth

        rows = list(
            cls.period_queryset(period)
            .filter(status__in={"won", "lost"})
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(
                won=Count(
                    "id",
                    filter=Q(status="won"),
                ),
                lost=Count(
                    "id",
                    filter=Q(status="lost"),
                ),
            )
            .order_by("month")
        )

        return [
            {
                "month": row["month"].date(),
                "won": row["won"],
                "lost": row["lost"],
                "closed": (
                    row["won"] + row["lost"]
                ),
                "conversion_rate": (
                    round(
                        row["won"]
                        / (
                            row["won"]
                            + row["lost"]
                        )
                        * 100,
                        2,
                    )
                    if (
                        row["won"]
                        + row["lost"]
                    )
                    else 0.0
                ),
            }
            for row in rows
        ]

    @classmethod
    def estimated_value_by_currency(cls, period):
        from django.db.models import DecimalField, Sum, Value
        from django.db.models.functions import Coalesce

        return list(
            cls.period_queryset(period)
            .exclude(estimated_value__isnull=True)
            .values("currency")
            .annotate(
                estimated_value=Coalesce(
                    Sum("estimated_value"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                )
            )
            .order_by("currency")
        )

    @classmethod
    def build(cls, period, now):
        return {
            "summary": cls.summary(period, now),
            "leads_by_status": (
                cls.leads_by_status(period)
            ),
            "leads_by_source": (
                cls.leads_by_source(period)
            ),
            "leads_by_owner": (
                cls.leads_by_owner(period)
            ),
            "conversion_funnel": (
                cls.conversion_funnel(period)
            ),
            "monthly_lead_trend": (
                cls.monthly_lead_trend(period)
            ),
            "won_lost_trend": (
                cls.won_lost_trend(period)
            ),
            "estimated_value_by_currency": (
                cls.estimated_value_by_currency(
                    period
                )
            ),
            "metadata": {
                "trend_date_basis": "lead_created_at",
                "conversion_definition": (
                    "won divided by won plus lost"
                ),
            },
        }


class SalesReportingRepository:
    CLOSED_STATUSES = {
        "accepted",
        "rejected",
    }

    OPEN_STATUSES = {
        "draft",
        "sent",
        "viewed",
    }

    @staticmethod
    def _quotation_model():
        from django.apps import apps

        return apps.get_model(
            "quotations",
            "Quotation",
        )

    @classmethod
    def period_queryset(cls, period):
        Quotation = cls._quotation_model()

        return Quotation.objects.filter(
            issue_date__gte=period.date_from,
            issue_date__lte=period.date_to,
        )

    @classmethod
    def summary(cls, period, today):
        from django.db.models import Count, Q

        Quotation = cls._quotation_model()
        period_queryset = cls.period_queryset(period)

        all_time = Quotation.objects.aggregate(
            all_time_total_quotations=Count("id"),
            all_time_accepted_quotations=Count(
                "id",
                filter=Q(status="accepted"),
            ),
            all_time_rejected_quotations=Count(
                "id",
                filter=Q(status="rejected"),
            ),
        )

        period_metrics = period_queryset.aggregate(
            total_quotations=Count("id"),
            draft_quotations=Count(
                "id",
                filter=Q(status="draft"),
            ),
            sent_quotations=Count(
                "id",
                filter=Q(status="sent"),
            ),
            viewed_quotations=Count(
                "id",
                filter=Q(status="viewed"),
            ),
            accepted_quotations=Count(
                "id",
                filter=Q(status="accepted"),
            ),
            rejected_quotations=Count(
                "id",
                filter=Q(status="rejected"),
            ),
            expired_quotations=Count(
                "id",
                filter=Q(status="expired"),
            ),
            cancelled_quotations=Count(
                "id",
                filter=Q(status="cancelled"),
            ),
            naturally_expired_open_quotations=Count(
                "id",
                filter=(
                    Q(
                        expiry_date__lt=today,
                        status__in=cls.OPEN_STATUSES,
                    )
                ),
            ),
            quotations_with_leads=Count(
                "id",
                filter=Q(lead__isnull=False),
            ),
            quotations_without_leads=Count(
                "id",
                filter=Q(lead__isnull=True),
            ),
        )

        closed = (
            period_metrics["accepted_quotations"]
            + period_metrics["rejected_quotations"]
        )

        decided = (
            closed
            + period_metrics["expired_quotations"]
        )

        total = period_metrics["total_quotations"]

        period_metrics["closed_quotations"] = closed
        period_metrics["decided_quotations"] = decided

        period_metrics["quotation_conversion_rate"] = (
            round(
                period_metrics["accepted_quotations"]
                / closed
                * 100,
                2,
            )
            if closed
            else 0.0
        )

        period_metrics[
            "acceptance_rate_from_total"
        ] = (
            round(
                period_metrics["accepted_quotations"]
                / total
                * 100,
                2,
            )
            if total
            else 0.0
        )

        period_metrics["rejection_rate"] = (
            round(
                period_metrics["rejected_quotations"]
                / closed
                * 100,
                2,
            )
            if closed
            else 0.0
        )

        return {
            **all_time,
            **period_metrics,
        }

    @classmethod
    def quotations_by_status(cls, period):
        from django.db.models import Count

        Quotation = cls._quotation_model()

        rows = {
            row["status"]: row["total"]
            for row in (
                cls.period_queryset(period)
                .values("status")
                .annotate(total=Count("id"))
            )
        }

        return [
            {
                "status": value,
                "label": label,
                "total": rows.get(value, 0),
            }
            for value, label in (
                Quotation._meta.get_field(
                    "status"
                ).choices
            )
        ]

    @classmethod
    def value_by_currency(cls, period):
        from django.db.models import (
            Count,
            DecimalField,
            Q,
            Sum,
            Value,
        )
        from django.db.models.functions import Coalesce

        return list(
            cls.period_queryset(period)
            .values("currency")
            .annotate(
                quotation_count=Count("id"),
                total_value=Coalesce(
                    Sum("total_amount"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
                accepted_value=Coalesce(
                    Sum(
                        "total_amount",
                        filter=Q(status="accepted"),
                    ),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
                rejected_value=Coalesce(
                    Sum(
                        "total_amount",
                        filter=Q(status="rejected"),
                    ),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
                open_value=Coalesce(
                    Sum(
                        "total_amount",
                        filter=Q(
                            status__in=cls.OPEN_STATUSES,
                        ),
                    ),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by("currency")
        )

    @classmethod
    def monthly_quotation_trend(cls, period):
        from django.db.models import (
            Count,
            DecimalField,
            Q,
            Sum,
            Value,
        )
        from django.db.models.functions import (
            Coalesce,
            TruncMonth,
        )

        rows = list(
            cls.period_queryset(period)
            .annotate(
                month=TruncMonth("issue_date")
            )
            .values("month", "currency")
            .annotate(
                total_quotations=Count("id"),
                accepted_quotations=Count(
                    "id",
                    filter=Q(status="accepted"),
                ),
                rejected_quotations=Count(
                    "id",
                    filter=Q(status="rejected"),
                ),
                expired_quotations=Count(
                    "id",
                    filter=Q(status="expired"),
                ),
                total_value=Coalesce(
                    Sum("total_amount"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
                accepted_value=Coalesce(
                    Sum(
                        "total_amount",
                        filter=Q(status="accepted"),
                    ),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by("month", "currency")
        )

        return [
            {
                "month": row["month"],
                "currency": row["currency"],
                "total_quotations": (
                    row["total_quotations"]
                ),
                "accepted_quotations": (
                    row["accepted_quotations"]
                ),
                "rejected_quotations": (
                    row["rejected_quotations"]
                ),
                "expired_quotations": (
                    row["expired_quotations"]
                ),
                "total_value": row["total_value"],
                "accepted_value": (
                    row["accepted_value"]
                ),
                "conversion_rate": (
                    round(
                        row["accepted_quotations"]
                        / (
                            row["accepted_quotations"]
                            + row[
                                "rejected_quotations"
                            ]
                        )
                        * 100,
                        2,
                    )
                    if (
                        row["accepted_quotations"]
                        + row[
                            "rejected_quotations"
                        ]
                    )
                    else 0.0
                ),
            }
            for row in rows
        ]

    @classmethod
    def acceptance_trend(cls, period):
        from django.db.models import (
            Count,
            DecimalField,
            Sum,
            Value,
        )
        from django.db.models.functions import (
            Coalesce,
            TruncMonth,
        )

        rows = list(
            cls._quotation_model()
            .objects.filter(
                status="accepted",
                accepted_at__gte=period.datetime_from,
                accepted_at__lt=period.datetime_to,
            )
            .annotate(
                month=TruncMonth("accepted_at")
            )
            .values("month", "currency")
            .annotate(
                accepted_quotations=Count("id"),
                accepted_value=Coalesce(
                    Sum("total_amount"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by("month", "currency")
        )

        return rows

    @classmethod
    def expiry_ageing(cls, today):
        from datetime import timedelta

        from django.db.models import Count, Q

        Quotation = cls._quotation_model()

        queryset = Quotation.objects.filter(
            status__in=cls.OPEN_STATUSES,
            expiry_date__isnull=False,
        )

        return queryset.aggregate(
            expires_today=Count(
                "id",
                filter=Q(expiry_date=today),
            ),
            expires_next_7_days=Count(
                "id",
                filter=Q(
                    expiry_date__gt=today,
                    expiry_date__lte=(
                        today
                        + timedelta(days=7)
                    ),
                ),
            ),
            expires_next_30_days=Count(
                "id",
                filter=Q(
                    expiry_date__gt=(
                        today
                        + timedelta(days=7)
                    ),
                    expiry_date__lte=(
                        today
                        + timedelta(days=30)
                    ),
                ),
            ),
            already_expired=Count(
                "id",
                filter=Q(expiry_date__lt=today),
            ),
        )

    @classmethod
    def client_distribution(cls, period):
        from django.db.models import (
            Count,
            DecimalField,
            Sum,
            Value,
        )
        from django.db.models.functions import Coalesce

        rows = list(
            cls.period_queryset(period)
            .values(
                "client_id",
                "client__client_code",
                "client__company_name",
            )
            .annotate(
                quotation_count=Count("id"),
                currencies=Count(
                    "currency",
                    distinct=True,
                ),
                total_value=Coalesce(
                    Sum("total_amount"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by(
                "-quotation_count",
                "client__company_name",
            )[:25]
        )

        return [
            {
                "client_id": row["client_id"],
                "client_code": (
                    row["client__client_code"]
                ),
                "client_name": (
                    row["client__company_name"]
                ),
                "quotation_count": (
                    row["quotation_count"]
                ),
                "currency_count": row["currencies"],
                "total_value": row["total_value"],
            }
            for row in rows
        ]

    @classmethod
    def build(cls, period, now):
        today = timezone.localdate()

        return {
            "summary": cls.summary(
                period,
                today,
            ),
            "quotations_by_status": (
                cls.quotations_by_status(period)
            ),
            "value_by_currency": (
                cls.value_by_currency(period)
            ),
            "monthly_quotation_trend": (
                cls.monthly_quotation_trend(period)
            ),
            "acceptance_trend": (
                cls.acceptance_trend(period)
            ),
            "expiry_ageing": cls.expiry_ageing(
                today
            ),
            "top_clients": (
                cls.client_distribution(period)
            ),
            "metadata": {
                "period_date_basis": "issue_date",
                "acceptance_date_basis": (
                    "accepted_at"
                ),
                "conversion_definition": (
                    "accepted divided by accepted "
                    "plus rejected"
                ),
            },
        }


class ProjectReportingRepository:
    ACTIVE_STATUSES = {
        "planning",
        "development",
        "testing",
        "review",
    }

    TERMINAL_STATUSES = {
        "completed",
        "cancelled",
    }

    @staticmethod
    def _project_model():
        from django.apps import apps

        return apps.get_model(
            "projects",
            "Project",
        )

    @classmethod
    def period_queryset(cls, period):
        Project = cls._project_model()

        return Project.objects.filter(
            created_at__gte=period.datetime_from,
            created_at__lt=period.datetime_to,
        )

    @classmethod
    def summary(cls, period, today):
        from django.db.models import (
            Avg,
            Count,
            Q,
        )

        Project = cls._project_model()

        all_time = Project.objects.aggregate(
            total_projects=Count("id"),
            active_projects=Count(
                "id",
                filter=Q(
                    status__in=cls.ACTIVE_STATUSES,
                ),
            ),
            completed_projects=Count(
                "id",
                filter=Q(status="completed"),
            ),
            cancelled_projects=Count(
                "id",
                filter=Q(status="cancelled"),
            ),
            overdue_projects=Count(
                "id",
                filter=Q(
                    deadline__lt=today,
                    status__in=cls.ACTIVE_STATUSES,
                ),
            ),
            projects_without_manager=Count(
                "id",
                filter=Q(
                    project_manager__isnull=True,
                    status__in=cls.ACTIVE_STATUSES,
                ),
            ),
            projects_without_deadline=Count(
                "id",
                filter=Q(
                    deadline__isnull=True,
                    status__in=cls.ACTIVE_STATUSES,
                ),
            ),
            average_progress=Avg(
                "progress",
                filter=Q(
                    status__in=cls.ACTIVE_STATUSES,
                ),
            ),
        )

        period_metrics = cls.period_queryset(
            period
        ).aggregate(
            new_projects=Count("id"),
            new_active_projects=Count(
                "id",
                filter=Q(
                    status__in=cls.ACTIVE_STATUSES,
                ),
            ),
        )

        completed_in_period = Project.objects.filter(
            status="completed",
            completed_at__gte=period.datetime_from,
            completed_at__lt=period.datetime_to,
        ).count()

        all_time["average_progress"] = round(
            float(all_time["average_progress"] or 0),
            2,
        )

        return {
            **all_time,
            **period_metrics,
            "completed_in_period": (
                completed_in_period
            ),
        }

    @classmethod
    def projects_by_status(cls):
        from django.db.models import Count

        Project = cls._project_model()

        totals = {
            row["status"]: row["total"]
            for row in (
                Project.objects
                .values("status")
                .annotate(total=Count("id"))
            )
        }

        return [
            {
                "status": value,
                "label": label,
                "total": totals.get(value, 0),
            }
            for value, label in (
                Project._meta.get_field(
                    "status"
                ).choices
            )
        ]

    @classmethod
    def projects_by_priority(cls):
        from django.db.models import Count

        Project = cls._project_model()

        totals = {
            row["priority"]: row["total"]
            for row in (
                Project.objects
                .values("priority")
                .annotate(total=Count("id"))
            )
        }

        return [
            {
                "priority": value,
                "label": label,
                "total": totals.get(value, 0),
            }
            for value, label in (
                Project._meta.get_field(
                    "priority"
                ).choices
            )
        ]

    @classmethod
    def projects_by_manager(cls):
        from django.db.models import (
            Avg,
            Count,
            Q,
        )

        rows = list(
            cls._project_model()
            .objects.values(
                "project_manager_id",
                "project_manager__username",
                "project_manager__first_name",
                "project_manager__last_name",
                "project_manager__email",
            )
            .annotate(
                total_projects=Count("id"),
                active_projects=Count(
                    "id",
                    filter=Q(
                        status__in=(
                            cls.ACTIVE_STATUSES
                        ),
                    ),
                ),
                completed_projects=Count(
                    "id",
                    filter=Q(status="completed"),
                ),
                overdue_projects=Count(
                    "id",
                    filter=Q(
                        status__in=(
                            cls.ACTIVE_STATUSES
                        ),
                        deadline__lt=(
                            timezone.localdate()
                        ),
                    ),
                ),
                average_progress=Avg(
                    "progress",
                    filter=Q(
                        status__in=(
                            cls.ACTIVE_STATUSES
                        ),
                    ),
                ),
            )
            .order_by(
                "-active_projects",
                "-total_projects",
                "project_manager__username",
            )
        )

        result = []

        for row in rows:
            first_name = (
                row["project_manager__first_name"]
                or ""
            ).strip()
            last_name = (
                row["project_manager__last_name"]
                or ""
            ).strip()

            full_name = (
                f"{first_name} {last_name}".strip()
            )

            if row["project_manager_id"] is None:
                manager_name = "Unassigned"
            else:
                manager_name = (
                    full_name
                    or row[
                        "project_manager__username"
                    ]
                    or row[
                        "project_manager__email"
                    ]
                    or str(
                        row["project_manager_id"]
                    )
                )

            result.append(
                {
                    "manager_id": (
                        row["project_manager_id"]
                    ),
                    "manager_name": manager_name,
                    "username": row[
                        "project_manager__username"
                    ],
                    "email": row[
                        "project_manager__email"
                    ],
                    "total_projects": (
                        row["total_projects"]
                    ),
                    "active_projects": (
                        row["active_projects"]
                    ),
                    "completed_projects": (
                        row["completed_projects"]
                    ),
                    "overdue_projects": (
                        row["overdue_projects"]
                    ),
                    "average_progress": round(
                        float(
                            row["average_progress"]
                            or 0
                        ),
                        2,
                    ),
                }
            )

        return result

    @classmethod
    def project_health(cls, today):
        from datetime import timedelta

        from django.db.models import (
            Case,
            CharField,
            Count,
            Q,
            Value,
            When,
        )

        Project = cls._project_model()

        warning_date = today + timedelta(days=14)

        queryset = Project.objects.annotate(
            health=Case(
                When(
                    status="completed",
                    then=Value("completed"),
                ),
                When(
                    status="cancelled",
                    then=Value("cancelled"),
                ),
                When(
                    deadline__lt=today,
                    status__in=cls.ACTIVE_STATUSES,
                    then=Value("overdue"),
                ),
                When(
                    deadline__lte=warning_date,
                    deadline__gte=today,
                    progress__lt=75,
                    status__in=cls.ACTIVE_STATUSES,
                    then=Value("at_risk"),
                ),
                When(
                    progress__lt=25,
                    status__in={
                        "development",
                        "testing",
                        "review",
                    },
                    then=Value("at_risk"),
                ),
                When(
                    status__in=cls.ACTIVE_STATUSES,
                    then=Value("healthy"),
                ),
                default=Value("unknown"),
                output_field=CharField(),
            )
        )

        totals = {
            row["health"]: row["total"]
            for row in (
                queryset.values("health")
                .annotate(total=Count("id"))
            )
        }

        health_order = (
            "healthy",
            "at_risk",
            "overdue",
            "completed",
            "cancelled",
            "unknown",
        )

        return [
            {
                "health": health,
                "total": totals.get(health, 0),
            }
            for health in health_order
        ]

    @classmethod
    def overdue_projects(cls, today):
        from django.db.models import F

        rows = list(
            cls._project_model()
            .objects.filter(
                status__in=cls.ACTIVE_STATUSES,
                deadline__lt=today,
            )
            .select_related(
                "client",
                "project_manager",
            )
            .annotate(
                days_overdue=today - F("deadline")
            )
            .values(
                "id",
                "project_code",
                "title",
                "status",
                "priority",
                "progress",
                "deadline",
                "currency",
                "budget",
                "client_id",
                "client__client_code",
                "client__company_name",
                "project_manager_id",
                "project_manager__username",
                "project_manager__first_name",
                "project_manager__last_name",
                "days_overdue",
            )
            .order_by(
                "deadline",
                "-priority",
                "title",
            )
        )

        result = []

        for row in rows:
            manager_name = "Unassigned"

            if row["project_manager_id"]:
                full_name = (
                    f"{row['project_manager__first_name'] or ''} "
                    f"{row['project_manager__last_name'] or ''}"
                ).strip()

                manager_name = (
                    full_name
                    or row[
                        "project_manager__username"
                    ]
                    or str(
                        row["project_manager_id"]
                    )
                )

            days_overdue = row["days_overdue"]

            result.append(
                {
                    "project_id": row["id"],
                    "project_code": (
                        row["project_code"]
                    ),
                    "title": row["title"],
                    "status": row["status"],
                    "priority": row["priority"],
                    "progress": row["progress"],
                    "deadline": row["deadline"],
                    "days_overdue": (
                        days_overdue.days
                        if days_overdue
                        else 0
                    ),
                    "currency": row["currency"],
                    "budget": row["budget"],
                    "client_id": row["client_id"],
                    "client_code": (
                        row["client__client_code"]
                    ),
                    "client_name": (
                        row["client__company_name"]
                    ),
                    "manager_id": (
                        row["project_manager_id"]
                    ),
                    "manager_name": manager_name,
                }
            )

        return result

    @classmethod
    def budget_by_currency(cls):
        from django.db.models import (
            Count,
            DecimalField,
            Q,
            Sum,
            Value,
        )
        from django.db.models.functions import Coalesce

        return list(
            cls._project_model()
            .objects.values("currency")
            .annotate(
                project_count=Count("id"),
                total_budget=Coalesce(
                    Sum("budget"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
                active_budget=Coalesce(
                    Sum(
                        "budget",
                        filter=Q(
                            status__in=(
                                cls.ACTIVE_STATUSES
                            ),
                        ),
                    ),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
                completed_budget=Coalesce(
                    Sum(
                        "budget",
                        filter=Q(status="completed"),
                    ),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
                overdue_budget=Coalesce(
                    Sum(
                        "budget",
                        filter=Q(
                            status__in=(
                                cls.ACTIVE_STATUSES
                            ),
                            deadline__lt=(
                                timezone.localdate()
                            ),
                        ),
                    ),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by("currency")
        )

    @classmethod
    def completion_trend(cls, period):
        from django.db.models import Count
        from django.db.models.functions import TruncMonth

        rows = list(
            cls._project_model()
            .objects.filter(
                status="completed",
                completed_at__gte=period.datetime_from,
                completed_at__lt=period.datetime_to,
            )
            .annotate(
                month=TruncMonth("completed_at")
            )
            .values("month")
            .annotate(
                completed_projects=Count("id")
            )
            .order_by("month")
        )

        return [
            {
                "month": row["month"].date(),
                "completed_projects": (
                    row["completed_projects"]
                ),
            }
            for row in rows
        ]

    @classmethod
    def creation_trend(cls, period):
        from django.db.models import Count
        from django.db.models.functions import TruncMonth

        rows = list(
            cls.period_queryset(period)
            .annotate(
                month=TruncMonth("created_at")
            )
            .values("month")
            .annotate(
                new_projects=Count("id")
            )
            .order_by("month")
        )

        return [
            {
                "month": row["month"].date(),
                "new_projects": row["new_projects"],
            }
            for row in rows
        ]

    @classmethod
    def progress_distribution(cls):
        from django.db.models import (
            Case,
            CharField,
            Count,
            Value,
            When,
        )

        queryset = (
            cls._project_model()
            .objects.filter(
                status__in=cls.ACTIVE_STATUSES,
            )
            .annotate(
                progress_band=Case(
                    When(
                        progress__lt=25,
                        then=Value("0_24"),
                    ),
                    When(
                        progress__lt=50,
                        then=Value("25_49"),
                    ),
                    When(
                        progress__lt=75,
                        then=Value("50_74"),
                    ),
                    When(
                        progress__lt=100,
                        then=Value("75_99"),
                    ),
                    default=Value("100"),
                    output_field=CharField(),
                )
            )
        )

        totals = {
            row["progress_band"]: row["total"]
            for row in (
                queryset.values("progress_band")
                .annotate(total=Count("id"))
            )
        }

        labels = (
            ("0_24", "0–24%"),
            ("25_49", "25–49%"),
            ("50_74", "50–74%"),
            ("75_99", "75–99%"),
            ("100", "100%"),
        )

        return [
            {
                "band": band,
                "label": label,
                "total": totals.get(band, 0),
            }
            for band, label in labels
        ]

    @classmethod
    def build(cls, period, now):
        today = timezone.localdate()

        return {
            "summary": cls.summary(
                period,
                today,
            ),
            "projects_by_status": (
                cls.projects_by_status()
            ),
            "projects_by_priority": (
                cls.projects_by_priority()
            ),
            "projects_by_manager": (
                cls.projects_by_manager()
            ),
            "project_health": (
                cls.project_health(today)
            ),
            "overdue_projects": (
                cls.overdue_projects(today)
            ),
            "budget_by_currency": (
                cls.budget_by_currency()
            ),
            "completion_trend": (
                cls.completion_trend(period)
            ),
            "creation_trend": (
                cls.creation_trend(period)
            ),
            "progress_distribution": (
                cls.progress_distribution()
            ),
            "metadata": {
                "creation_period_basis": (
                    "project_created_at"
                ),
                "completion_period_basis": (
                    "project_completed_at"
                ),
                "health_definition": {
                    "overdue": (
                        "active project with deadline "
                        "before today"
                    ),
                    "at_risk": (
                        "deadline within 14 days and "
                        "progress below 75%, or advanced "
                        "status with progress below 25%"
                    ),
                    "healthy": (
                        "active project not classified "
                        "as overdue or at risk"
                    ),
                },
            },
        }


class TaskReportingRepository:
    OPEN_STATUSES = {
        "todo",
        "in_progress",
        "testing",
        "review",
    }

    TERMINAL_STATUSES = {
        "completed",
        "cancelled",
    }

    @staticmethod
    def _task_model():
        from django.apps import apps

        return apps.get_model(
            "tasks",
            "Task",
        )

    @staticmethod
    def _task_assignee_model():
        from django.apps import apps

        return apps.get_model(
            "tasks",
            "TaskAssignee",
        )

    @classmethod
    def period_queryset(cls, period):
        Task = cls._task_model()

        return Task.objects.filter(
            created_at__gte=period.datetime_from,
            created_at__lt=period.datetime_to,
        )

    @classmethod
    def summary(cls, period, today):
        from django.db.models import Count, Q

        Task = cls._task_model()

        all_time = Task.objects.aggregate(
            total_tasks=Count("id"),
            open_tasks=Count(
                "id",
                filter=Q(
                    status__in=cls.OPEN_STATUSES,
                ),
            ),
            completed_tasks=Count(
                "id",
                filter=Q(status="completed"),
            ),
            cancelled_tasks=Count(
                "id",
                filter=Q(status="cancelled"),
            ),
            overdue_tasks=Count(
                "id",
                filter=Q(
                    status__in=cls.OPEN_STATUSES,
                    due_date__lt=today,
                ),
            ),
            tasks_without_due_date=Count(
                "id",
                filter=Q(
                    status__in=cls.OPEN_STATUSES,
                    due_date__isnull=True,
                ),
            ),
            high_priority_open_tasks=Count(
                "id",
                filter=Q(
                    status__in=cls.OPEN_STATUSES,
                    priority__in={
                        "high",
                        "urgent",
                    },
                ),
            ),
        )

        period_metrics = cls.period_queryset(
            period
        ).aggregate(
            new_tasks=Count("id"),
            new_open_tasks=Count(
                "id",
                filter=Q(
                    status__in=cls.OPEN_STATUSES,
                ),
            ),
        )

        completed_in_period = (
            Task.objects.filter(
                status="completed",
                completed_at__gte=(
                    period.datetime_from
                ),
                completed_at__lt=(
                    period.datetime_to
                ),
            ).count()
        )

        period_metrics[
            "completed_in_period"
        ] = completed_in_period

        created_count = period_metrics["new_tasks"]

        period_metrics[
            "period_completion_rate"
        ] = (
            round(
                completed_in_period
                / created_count
                * 100,
                2,
            )
            if created_count
            else 0.0
        )

        return {
            **all_time,
            **period_metrics,
        }

    @classmethod
    def tasks_by_status(cls):
        from django.db.models import Count

        Task = cls._task_model()

        totals = {
            row["status"]: row["total"]
            for row in (
                Task.objects
                .values("status")
                .annotate(total=Count("id"))
            )
        }

        return [
            {
                "status": value,
                "label": label,
                "total": totals.get(value, 0),
            }
            for value, label in (
                Task._meta.get_field(
                    "status"
                ).choices
            )
        ]

    @classmethod
    def tasks_by_priority(cls):
        from django.db.models import Count

        Task = cls._task_model()

        totals = {
            row["priority"]: row["total"]
            for row in (
                Task.objects
                .values("priority")
                .annotate(total=Count("id"))
            )
        }

        return [
            {
                "priority": value,
                "label": label,
                "total": totals.get(value, 0),
            }
            for value, label in (
                Task._meta.get_field(
                    "priority"
                ).choices
            )
        ]

    @classmethod
    def workload_by_assignee(cls, today):
        from collections import defaultdict

        from django.db.models import Count, Q

        Task = cls._task_model()
        TaskAssignee = cls._task_assignee_model()

        metrics = defaultdict(
            lambda: {
                "task_ids": set(),
                "open_task_ids": set(),
                "completed_task_ids": set(),
                "overdue_task_ids": set(),
                "urgent_task_ids": set(),
                "username": None,
                "first_name": "",
                "last_name": "",
                "email": None,
            }
        )

        primary_task_rows = Task.objects.filter(
            assignee__isnull=False,
        ).values(
            "id",
            "assignee_id",
            "assignee__username",
            "assignee__first_name",
            "assignee__last_name",
            "assignee__email",
            "status",
            "priority",
            "due_date",
        )

        for task in primary_task_rows:
            user_id = task["assignee_id"]
            item = metrics[user_id]

            item["username"] = (
                task["assignee__username"]
            )
            item["first_name"] = (
                task["assignee__first_name"] or ""
            )
            item["last_name"] = (
                task["assignee__last_name"] or ""
            )
            item["email"] = task["assignee__email"]

            task_id = task["id"]
            item["task_ids"].add(task_id)

            if task["status"] in cls.OPEN_STATUSES:
                item["open_task_ids"].add(task_id)

                if (
                    task["due_date"] is not None
                    and task["due_date"] < today
                ):
                    item["overdue_task_ids"].add(
                        task_id
                    )

                if task["priority"] == "urgent":
                    item["urgent_task_ids"].add(
                        task_id
                    )

            if task["status"] == "completed":
                item["completed_task_ids"].add(
                    task_id
                )

        additional_rows = (
            TaskAssignee.objects
            .select_related("task", "user")
            .values(
                "task_id",
                "user_id",
                "user__username",
                "user__first_name",
                "user__last_name",
                "user__email",
                "task__status",
                "task__priority",
                "task__due_date",
            )
        )

        for assignment in additional_rows:
            user_id = assignment["user_id"]
            item = metrics[user_id]

            item["username"] = (
                assignment["user__username"]
            )
            item["first_name"] = (
                assignment["user__first_name"] or ""
            )
            item["last_name"] = (
                assignment["user__last_name"] or ""
            )
            item["email"] = assignment["user__email"]

            task_id = assignment["task_id"]
            item["task_ids"].add(task_id)

            status = assignment["task__status"]

            if status in cls.OPEN_STATUSES:
                item["open_task_ids"].add(task_id)

                due_date = assignment[
                    "task__due_date"
                ]

                if (
                    due_date is not None
                    and due_date < today
                ):
                    item["overdue_task_ids"].add(
                        task_id
                    )

                if (
                    assignment["task__priority"]
                    == "urgent"
                ):
                    item["urgent_task_ids"].add(
                        task_id
                    )

            if status == "completed":
                item["completed_task_ids"].add(
                    task_id
                )

        result = []

        for user_id, item in metrics.items():
            full_name = (
                f"{item['first_name']} "
                f"{item['last_name']}"
            ).strip()

            total = len(item["task_ids"])
            completed = len(
                item["completed_task_ids"]
            )

            result.append(
                {
                    "user_id": user_id,
                    "user_name": (
                        full_name
                        or item["username"]
                        or item["email"]
                        or str(user_id)
                    ),
                    "username": item["username"],
                    "email": item["email"],
                    "total_tasks": total,
                    "open_tasks": len(
                        item["open_task_ids"]
                    ),
                    "completed_tasks": completed,
                    "overdue_tasks": len(
                        item["overdue_task_ids"]
                    ),
                    "urgent_tasks": len(
                        item["urgent_task_ids"]
                    ),
                    "completion_rate": (
                        round(
                            completed
                            / total
                            * 100,
                            2,
                        )
                        if total
                        else 0.0
                    ),
                }
            )

        return sorted(
            result,
            key=lambda row: (
                -row["open_tasks"],
                -row["overdue_tasks"],
                row["user_name"].lower(),
            ),
        )

    @classmethod
    def unassigned_workload(cls, today):
        from django.db.models import Count, Q

        Task = cls._task_model()

        queryset = Task.objects.filter(
            assignee__isnull=True,
            additional_assignees__isnull=True,
        )

        return queryset.aggregate(
            total_unassigned_tasks=Count(
                "id",
                distinct=True,
            ),
            open_unassigned_tasks=Count(
                "id",
                filter=Q(
                    status__in=cls.OPEN_STATUSES,
                ),
                distinct=True,
            ),
            overdue_unassigned_tasks=Count(
                "id",
                filter=Q(
                    status__in=cls.OPEN_STATUSES,
                    due_date__lt=today,
                ),
                distinct=True,
            ),
            urgent_unassigned_tasks=Count(
                "id",
                filter=Q(
                    status__in=cls.OPEN_STATUSES,
                    priority="urgent",
                ),
                distinct=True,
            ),
        )

    @classmethod
    def overdue_tasks(cls, today):
        from django.db.models import F

        Task = cls._task_model()
        TaskAssignee = cls._task_assignee_model()

        rows = list(
            Task.objects.filter(
                status__in=cls.OPEN_STATUSES,
                due_date__lt=today,
            )
            .select_related(
                "project",
                "assignee",
            )
            .annotate(
                days_overdue=today - F("due_date")
            )
            .values(
                "id",
                "title",
                "status",
                "priority",
                "due_date",
                "project_id",
                "project__project_code",
                "project__title",
                "assignee_id",
                "assignee__username",
                "assignee__first_name",
                "assignee__last_name",
                "assignee__email",
                "days_overdue",
            )
            .order_by(
                "due_date",
                "-priority",
                "title",
            )
        )

        task_ids = [
            row["id"]
            for row in rows
        ]

        assignees_by_task = {
            task_id: {}
            for task_id in task_ids
        }

        for row in rows:
            user_id = row["assignee_id"]

            if user_id is None:
                continue

            full_name = (
                f"{row['assignee__first_name'] or ''} "
                f"{row['assignee__last_name'] or ''}"
            ).strip()

            assignees_by_task[row["id"]][user_id] = {
                "user_id": user_id,
                "user_name": (
                    full_name
                    or row["assignee__username"]
                    or row["assignee__email"]
                    or str(user_id)
                ),
                "assignment_type": "primary",
            }

        additional_rows = (
            TaskAssignee.objects
            .filter(task_id__in=task_ids)
            .values(
                "task_id",
                "user_id",
                "user__username",
                "user__first_name",
                "user__last_name",
                "user__email",
            )
            .order_by(
                "task_id",
                "user__username",
            )
        )

        for assignment in additional_rows:
            full_name = (
                f"{assignment['user__first_name'] or ''} "
                f"{assignment['user__last_name'] or ''}"
            ).strip()

            task_id = assignment["task_id"]
            user_id = assignment["user_id"]

            existing = assignees_by_task[
                task_id
            ].get(user_id)

            if existing is not None:
                existing[
                    "assignment_type"
                ] = "primary_and_additional"
                continue

            assignees_by_task[task_id][user_id] = {
                "user_id": user_id,
                "user_name": (
                    full_name
                    or assignment["user__username"]
                    or assignment["user__email"]
                    or str(user_id)
                ),
                "assignment_type": "additional",
            }

        result = []

        for row in rows:
            duration = row["days_overdue"]

            assignees = sorted(
                assignees_by_task[
                    row["id"]
                ].values(),
                key=lambda item: (
                    item["user_name"].lower()
                ),
            )

            result.append(
                {
                    "task_id": row["id"],
                    "title": row["title"],
                    "status": row["status"],
                    "priority": row["priority"],
                    "due_date": row["due_date"],
                    "days_overdue": (
                        duration.days
                        if duration
                        else 0
                    ),
                    "project_id": (
                        row["project_id"]
                    ),
                    "project_code": (
                        row["project__project_code"]
                    ),
                    "project_title": (
                        row["project__title"]
                    ),
                    "assignees": assignees,
                }
            )

        return result

    @classmethod
    def tasks_by_project(cls):
        from django.db.models import Count, Q

        rows = list(
            cls._task_model()
            .objects.values(
                "project_id",
                "project__project_code",
                "project__title",
            )
            .annotate(
                total_tasks=Count("id"),
                open_tasks=Count(
                    "id",
                    filter=Q(
                        status__in=(
                            cls.OPEN_STATUSES
                        ),
                    ),
                ),
                completed_tasks=Count(
                    "id",
                    filter=Q(status="completed"),
                ),
                overdue_tasks=Count(
                    "id",
                    filter=Q(
                        status__in=(
                            cls.OPEN_STATUSES
                        ),
                        due_date__lt=(
                            timezone.localdate()
                        ),
                    ),
                ),
            )
            .order_by(
                "-open_tasks",
                "-total_tasks",
                "project__title",
            )
        )

        result = []

        for row in rows:
            total = row["total_tasks"]
            completed = row["completed_tasks"]

            result.append(
                {
                    "project_id": (
                        row["project_id"]
                    ),
                    "project_code": (
                        row["project__project_code"]
                    ),
                    "project_title": (
                        row["project__title"]
                    ),
                    "total_tasks": total,
                    "open_tasks": row["open_tasks"],
                    "completed_tasks": completed,
                    "overdue_tasks": (
                        row["overdue_tasks"]
                    ),
                    "completion_rate": (
                        round(
                            completed / total * 100,
                            2,
                        )
                        if total
                        else 0.0
                    ),
                }
            )

        return result

    @classmethod
    def completion_trend(cls, period):
        from django.db.models import Count
        from django.db.models.functions import (
            TruncMonth,
        )

        rows = list(
            cls._task_model()
            .objects.filter(
                status="completed",
                completed_at__gte=(
                    period.datetime_from
                ),
                completed_at__lt=(
                    period.datetime_to
                ),
            )
            .annotate(
                month=TruncMonth("completed_at")
            )
            .values("month")
            .annotate(
                completed_tasks=Count("id")
            )
            .order_by("month")
        )

        return [
            {
                "month": row["month"].date(),
                "completed_tasks": (
                    row["completed_tasks"]
                ),
            }
            for row in rows
        ]

    @classmethod
    def creation_trend(cls, period):
        from django.db.models import Count
        from django.db.models.functions import (
            TruncMonth,
        )

        rows = list(
            cls.period_queryset(period)
            .annotate(
                month=TruncMonth("created_at")
            )
            .values("month")
            .annotate(
                new_tasks=Count("id")
            )
            .order_by("month")
        )

        return [
            {
                "month": row["month"].date(),
                "new_tasks": row["new_tasks"],
            }
            for row in rows
        ]

    @classmethod
    def due_date_ageing(cls, today):
        from datetime import timedelta

        from django.db.models import Count, Q

        Task = cls._task_model()

        queryset = Task.objects.filter(
            status__in=cls.OPEN_STATUSES,
            due_date__isnull=False,
        )

        return queryset.aggregate(
            overdue=Count(
                "id",
                filter=Q(due_date__lt=today),
            ),
            due_today=Count(
                "id",
                filter=Q(due_date=today),
            ),
            due_next_7_days=Count(
                "id",
                filter=Q(
                    due_date__gt=today,
                    due_date__lte=(
                        today
                        + timedelta(days=7)
                    ),
                ),
            ),
            due_next_30_days=Count(
                "id",
                filter=Q(
                    due_date__gt=(
                        today
                        + timedelta(days=7)
                    ),
                    due_date__lte=(
                        today
                        + timedelta(days=30)
                    ),
                ),
            ),
            due_later=Count(
                "id",
                filter=Q(
                    due_date__gt=(
                        today
                        + timedelta(days=30)
                    ),
                ),
            ),
        )

    @classmethod
    def build(cls, period, now):
        today = timezone.localdate()

        return {
            "summary": cls.summary(
                period,
                today,
            ),
            "tasks_by_status": (
                cls.tasks_by_status()
            ),
            "tasks_by_priority": (
                cls.tasks_by_priority()
            ),
            "workload_by_assignee": (
                cls.workload_by_assignee(today)
            ),
            "unassigned_workload": (
                cls.unassigned_workload(today)
            ),
            "overdue_tasks": (
                cls.overdue_tasks(today)
            ),
            "tasks_by_project": (
                cls.tasks_by_project()
            ),
            "completion_trend": (
                cls.completion_trend(period)
            ),
            "creation_trend": (
                cls.creation_trend(period)
            ),
            "due_date_ageing": (
                cls.due_date_ageing(today)
            ),
            "metadata": {
                "creation_period_basis": (
                    "task_created_at"
                ),
                "completion_period_basis": (
                    "task_completed_at"
                ),
                "overdue_definition": (
                    "open task with due date "
                    "before today"
                ),
            },
        }


class FinanceReportingRepository:
    RECEIVABLE_STATUSES = {
        "sent",
        "partially_paid",
        "overdue",
    }

    OPEN_INVOICE_STATUSES = {
        "draft",
        "sent",
        "partially_paid",
        "overdue",
    }

    REALIZED_PAYMENT_STATUS = "completed"
    REALIZED_EXPENSE_STATUS = "paid"

    @staticmethod
    def _model(model_name):
        from django.apps import apps

        return apps.get_model(
            "finance",
            model_name,
        )

    @classmethod
    def _currency_totals(
        cls,
        queryset,
        amount_field,
        result_name,
    ):
        from django.db.models import (
            Count,
            DecimalField,
            Sum,
            Value,
        )
        from django.db.models.functions import Coalesce

        rows = list(
            queryset.values("currency")
            .annotate(
                count=Count("id"),
                value=Coalesce(
                    Sum(amount_field),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by("currency")
        )

        return [
            {
                "currency": row["currency"],
                "count": row["count"],
                result_name: row["value"],
            }
            for row in rows
        ]

    @staticmethod
    def _currency_map(rows, value_key):
        return {
            row["currency"]: row[value_key]
            for row in rows
        }

    @classmethod
    def revenue_by_currency(cls, period):
        Payment = cls._model("Payment")

        queryset = Payment.objects.filter(
            status=cls.REALIZED_PAYMENT_STATUS,
            payment_date__gte=period.date_from,
            payment_date__lte=period.date_to,
        )

        return cls._currency_totals(
            queryset,
            "amount",
            "revenue",
        )

    @classmethod
    def expenses_by_currency(cls, period):
        Expense = cls._model("Expense")

        queryset = Expense.objects.filter(
            status=cls.REALIZED_EXPENSE_STATUS,
            expense_date__gte=period.date_from,
            expense_date__lte=period.date_to,
        )

        return cls._currency_totals(
            queryset,
            "amount",
            "expenses",
        )

    @classmethod
    def profit_by_currency(cls, period):
        revenues = cls.revenue_by_currency(period)
        expenses = cls.expenses_by_currency(period)

        revenue_map = cls._currency_map(
            revenues,
            "revenue",
        )
        expense_map = cls._currency_map(
            expenses,
            "expenses",
        )

        currencies = sorted(
            set(revenue_map)
            | set(expense_map)
        )

        result = []

        for currency in currencies:
            revenue = revenue_map.get(currency, 0)
            expense = expense_map.get(currency, 0)
            profit = revenue - expense

            result.append(
                {
                    "currency": currency,
                    "revenue": revenue,
                    "expenses": expense,
                    "profit": profit,
                    "profit_margin": (
                        round(
                            float(
                                profit
                                / revenue
                                * 100
                            ),
                            2,
                        )
                        if revenue
                        else 0.0
                    ),
                }
            )

        return result

    @classmethod
    def invoice_summary(cls, today):
        from django.db.models import Count, Q

        Invoice = cls._model("Invoice")

        metrics = Invoice.objects.aggregate(
            total_invoices=Count("id"),
            draft_invoices=Count(
                "id",
                filter=Q(status="draft"),
            ),
            sent_invoices=Count(
                "id",
                filter=Q(status="sent"),
            ),
            partially_paid_invoices=Count(
                "id",
                filter=Q(
                    status="partially_paid"
                ),
            ),
            paid_invoices=Count(
                "id",
                filter=Q(status="paid"),
            ),
            overdue_status_invoices=Count(
                "id",
                filter=Q(status="overdue"),
            ),
            cancelled_invoices=Count(
                "id",
                filter=Q(status="cancelled"),
            ),
            overdue_invoices=Count(
                "id",
                filter=(
                    Q(status="overdue")
                    | Q(
                        due_date__lt=today,
                        status__in={
                            "sent",
                            "partially_paid",
                        },
                    )
                ),
            ),
            invoices_without_due_date=Count(
                "id",
                filter=Q(
                    due_date__isnull=True,
                    status__in=(
                        cls.OPEN_INVOICE_STATUSES
                    ),
                ),
            ),
        )

        receivable_rows = cls._currency_totals(
            Invoice.objects.filter(
                status__in=cls.RECEIVABLE_STATUSES,
            ),
            "balance_due",
            "accounts_receivable",
        )

        overdue_rows = cls._currency_totals(
            Invoice.objects.filter(
                Q(status="overdue")
                | Q(
                    due_date__lt=today,
                    status__in={
                        "sent",
                        "partially_paid",
                    },
                )
            ),
            "balance_due",
            "overdue_receivable",
        )

        return {
            **metrics,
            "accounts_receivable_by_currency": (
                receivable_rows
            ),
            "overdue_receivable_by_currency": (
                overdue_rows
            ),
        }

    @classmethod
    def invoice_value_by_currency(cls):
        from django.db.models import (
            Count,
            DecimalField,
            Q,
            Sum,
            Value,
        )
        from django.db.models.functions import Coalesce

        Invoice = cls._model("Invoice")

        return list(
            Invoice.objects.values("currency")
            .annotate(
                invoice_count=Count("id"),
                invoiced_value=Coalesce(
                    Sum("total_amount"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
                paid_value=Coalesce(
                    Sum("paid_amount"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
                outstanding_value=Coalesce(
                    Sum(
                        "balance_due",
                        filter=Q(
                            status__in=(
                                cls.RECEIVABLE_STATUSES
                            ),
                        ),
                    ),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by("currency")
        )

    @classmethod
    def payment_summary(cls, period):
        from django.db.models import Count, Q

        Payment = cls._model("Payment")

        queryset = Payment.objects.filter(
            payment_date__gte=period.date_from,
            payment_date__lte=period.date_to,
        )

        metrics = queryset.aggregate(
            total_payments=Count("id"),
            completed_payments=Count(
                "id",
                filter=Q(status="completed"),
            ),
            pending_payments=Count(
                "id",
                filter=Q(status="pending"),
            ),
            failed_payments=Count(
                "id",
                filter=Q(status="failed"),
            ),
            refunded_payments=Count(
                "id",
                filter=Q(status="refunded"),
            ),
            voided_payments=Count(
                "id",
                filter=Q(status="voided"),
            ),
        )

        metrics["payments_by_currency"] = (
            cls._currency_totals(
                queryset.filter(status="completed"),
                "amount",
                "amount",
            )
        )

        return metrics

    @classmethod
    def payments_by_method(cls, period):
        from django.db.models import (
            Count,
            DecimalField,
            Sum,
            Value,
        )
        from django.db.models.functions import Coalesce

        Payment = cls._model("Payment")

        labels = dict(
            Payment._meta.get_field(
                "method"
            ).choices
        )

        rows = list(
            Payment.objects.filter(
                status="completed",
                payment_date__gte=period.date_from,
                payment_date__lte=period.date_to,
            )
            .values("method", "currency")
            .annotate(
                payment_count=Count("id"),
                amount=Coalesce(
                    Sum("amount"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by(
                "currency",
                "-amount",
                "method",
            )
        )

        return [
            {
                "method": row["method"],
                "label": labels.get(
                    row["method"],
                    row["method"],
                ),
                "currency": row["currency"],
                "payment_count": (
                    row["payment_count"]
                ),
                "amount": row["amount"],
            }
            for row in rows
        ]

    @classmethod
    def expenses_by_category(cls, period):
        from django.db.models import (
            Count,
            DecimalField,
            Sum,
            Value,
        )
        from django.db.models.functions import Coalesce

        Expense = cls._model("Expense")

        labels = dict(
            Expense._meta.get_field(
                "category"
            ).choices
        )

        rows = list(
            Expense.objects.filter(
                status="paid",
                expense_date__gte=period.date_from,
                expense_date__lte=period.date_to,
            )
            .values("category", "currency")
            .annotate(
                expense_count=Count("id"),
                amount=Coalesce(
                    Sum("amount"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by(
                "currency",
                "-amount",
                "category",
            )
        )

        return [
            {
                "category": row["category"],
                "label": labels.get(
                    row["category"],
                    row["category"],
                ),
                "currency": row["currency"],
                "expense_count": (
                    row["expense_count"]
                ),
                "amount": row["amount"],
            }
            for row in rows
        ]

    @classmethod
    def account_balances(cls):
        Account = cls._model("Account")

        return list(
            Account.objects.filter(
                is_active=True,
            )
            .values(
                "id",
                "account_code",
                "name",
                "account_type",
                "currency",
                "opening_balance",
                "current_balance",
                "is_system",
            )
            .order_by(
                "account_type",
                "currency",
                "account_code",
            )
        )

    @classmethod
    def balances_by_type_and_currency(cls):
        from django.db.models import (
            Count,
            DecimalField,
            Sum,
            Value,
        )
        from django.db.models.functions import Coalesce

        Account = cls._model("Account")

        return list(
            Account.objects.filter(
                is_active=True,
            )
            .values(
                "account_type",
                "currency",
            )
            .annotate(
                account_count=Count("id"),
                balance=Coalesce(
                    Sum("current_balance"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by(
                "account_type",
                "currency",
            )
        )

    @classmethod
    def monthly_finance_trend(cls, period):
        from django.db.models import (
            Count,
            DecimalField,
            Sum,
            Value,
        )
        from django.db.models.functions import (
            Coalesce,
            TruncMonth,
        )

        Payment = cls._model("Payment")
        Expense = cls._model("Expense")

        revenue_rows = list(
            Payment.objects.filter(
                status="completed",
                payment_date__gte=period.date_from,
                payment_date__lte=period.date_to,
            )
            .annotate(
                month=TruncMonth("payment_date")
            )
            .values("month", "currency")
            .annotate(
                payment_count=Count("id"),
                revenue=Coalesce(
                    Sum("amount"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by("month", "currency")
        )

        expense_rows = list(
            Expense.objects.filter(
                status="paid",
                expense_date__gte=period.date_from,
                expense_date__lte=period.date_to,
            )
            .annotate(
                month=TruncMonth("expense_date")
            )
            .values("month", "currency")
            .annotate(
                expense_count=Count("id"),
                expenses=Coalesce(
                    Sum("amount"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by("month", "currency")
        )

        combined = {}

        for row in revenue_rows:
            month = row["month"]
            key = (
                month.isoformat(),
                row["currency"],
            )

            combined[key] = {
                "month": month,
                "currency": row["currency"],
                "payment_count": (
                    row["payment_count"]
                ),
                "expense_count": 0,
                "revenue": row["revenue"],
                "expenses": 0,
            }

        for row in expense_rows:
            month = row["month"]
            key = (
                month.isoformat(),
                row["currency"],
            )

            item = combined.setdefault(
                key,
                {
                    "month": month,
                    "currency": row["currency"],
                    "payment_count": 0,
                    "expense_count": 0,
                    "revenue": 0,
                    "expenses": 0,
                },
            )

            item["expense_count"] = (
                row["expense_count"]
            )
            item["expenses"] = row["expenses"]

        result = []

        for key in sorted(combined):
            item = combined[key]
            revenue = item["revenue"]
            expenses = item["expenses"]
            profit = revenue - expenses

            result.append(
                {
                    **item,
                    "profit": profit,
                    "profit_margin": (
                        round(
                            float(
                                profit
                                / revenue
                                * 100
                            ),
                            2,
                        )
                        if revenue
                        else 0.0
                    ),
                }
            )

        return result

    @classmethod
    def invoice_ageing(cls, today):
        from datetime import timedelta

        from django.db.models import (
            Count,
            DecimalField,
            Q,
            Sum,
            Value,
        )
        from django.db.models.functions import Coalesce

        Invoice = cls._model("Invoice")

        queryset = Invoice.objects.filter(
            status__in=cls.RECEIVABLE_STATUSES,
        )

        buckets = (
            (
                "not_due",
                Q(
                    due_date__isnull=True,
                )
                | Q(due_date__gte=today),
            ),
            (
                "overdue_1_30",
                Q(
                    due_date__lt=today,
                    due_date__gte=(
                        today - timedelta(days=30)
                    ),
                ),
            ),
            (
                "overdue_31_60",
                Q(
                    due_date__lt=(
                        today - timedelta(days=30)
                    ),
                    due_date__gte=(
                        today - timedelta(days=60)
                    ),
                ),
            ),
            (
                "overdue_61_90",
                Q(
                    due_date__lt=(
                        today - timedelta(days=60)
                    ),
                    due_date__gte=(
                        today - timedelta(days=90)
                    ),
                ),
            ),
            (
                "overdue_90_plus",
                Q(
                    due_date__lt=(
                        today - timedelta(days=90)
                    ),
                ),
            ),
        )

        result = []

        currencies = list(
            queryset.values_list(
                "currency",
                flat=True,
            )
            .distinct()
            .order_by("currency")
        )

        for currency in currencies:
            currency_queryset = queryset.filter(
                currency=currency,
            )

            for bucket, condition in buckets:
                metrics = currency_queryset.filter(
                    condition
                ).aggregate(
                    invoice_count=Count("id"),
                    balance=Coalesce(
                        Sum("balance_due"),
                        Value(0),
                        output_field=DecimalField(
                            max_digits=18,
                            decimal_places=2,
                        ),
                    ),
                )

                result.append(
                    {
                        "currency": currency,
                        "bucket": bucket,
                        **metrics,
                    }
                )

        return result

    @classmethod
    def transaction_activity(cls, period):
        from django.db.models import (
            Count,
            DecimalField,
            Sum,
            Value,
        )
        from django.db.models.functions import Coalesce

        Transaction = cls._model("Transaction")

        return list(
            Transaction.objects.filter(
                transaction_date__gte=(
                    period.date_from
                ),
                transaction_date__lte=period.date_to,
            )
            .values("transaction_type")
            .annotate(
                transaction_count=Count("id"),
                total_amount=Coalesce(
                    Sum("total_amount"),
                    Value(0),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                ),
            )
            .order_by("transaction_type")
        )

    @classmethod
    def build(cls, period, now):
        today = timezone.localdate()

        revenue = cls.revenue_by_currency(period)
        expenses = cls.expenses_by_currency(period)

        return {
            "summary": {
                "revenue_by_currency": revenue,
                "expenses_by_currency": expenses,
                "profit_by_currency": (
                    cls.profit_by_currency(period)
                ),
                **cls.invoice_summary(today),
                **cls.payment_summary(period),
            },
            "invoice_value_by_currency": (
                cls.invoice_value_by_currency()
            ),
            "payments_by_method": (
                cls.payments_by_method(period)
            ),
            "expenses_by_category": (
                cls.expenses_by_category(period)
            ),
            "account_balances": (
                cls.account_balances()
            ),
            "balances_by_type_and_currency": (
                cls.balances_by_type_and_currency()
            ),
            "monthly_finance_trend": (
                cls.monthly_finance_trend(period)
            ),
            "invoice_ageing": (
                cls.invoice_ageing(today)
            ),
            "transaction_activity": (
                cls.transaction_activity(period)
            ),
            "metadata": {
                "revenue_definition": (
                    "completed payments within period"
                ),
                "expense_definition": (
                    "paid expenses within period"
                ),
                "profit_definition": (
                    "realized revenue minus realized "
                    "expenses, calculated per currency"
                ),
                "receivable_definition": (
                    "invoice balance_due for sent, "
                    "partially_paid and overdue invoices"
                ),
                "currency_policy": (
                    "currencies are never combined "
                    "without conversion"
                ),
            },
        }


class ContentMarketingReportingRepository:
    ENQUIRY_OPEN_STATUSES = {
        "new",
        "assigned",
        "contacted",
        "qualified",
        "proposal_sent",
    }

    @staticmethod
    def _model(app_label, model_name):
        from django.apps import apps

        return apps.get_model(
            app_label,
            model_name,
        )

    @classmethod
    def content_summary(cls, period):
        from django.db.models import (
            Avg,
            Count,
            Q,
            Sum,
        )

        InsightArticle = cls._model(
            "insights",
            "InsightArticle",
        )
        CaseStudy = cls._model(
            "case_studies",
            "CaseStudy",
        )
        Testimonial = cls._model(
            "testimonials",
            "Testimonial",
        )

        insights = InsightArticle.objects.aggregate(
            total=Count("id"),
            published=Count(
                "id",
                filter=Q(status="published"),
            ),
            draft=Count(
                "id",
                filter=Q(status="draft"),
            ),
            review=Count(
                "id",
                filter=Q(status="review"),
            ),
            scheduled=Count(
                "id",
                filter=Q(status="scheduled"),
            ),
            archived=Count(
                "id",
                filter=Q(status="archived"),
            ),
            featured=Count(
                "id",
                filter=Q(is_featured=True),
            ),
            total_views=Sum("view_count"),
            published_in_period=Count(
                "id",
                filter=Q(
                    status="published",
                    published_at__gte=(
                        period.datetime_from
                    ),
                    published_at__lt=(
                        period.datetime_to
                    ),
                ),
            ),
        )

        case_studies = CaseStudy.objects.aggregate(
            total=Count("id"),
            published=Count(
                "id",
                filter=Q(status="published"),
            ),
            draft=Count(
                "id",
                filter=Q(status="draft"),
            ),
            review=Count(
                "id",
                filter=Q(status="review"),
            ),
            scheduled=Count(
                "id",
                filter=Q(status="scheduled"),
            ),
            archived=Count(
                "id",
                filter=Q(status="archived"),
            ),
            featured=Count(
                "id",
                filter=Q(is_featured=True),
            ),
            total_views=Sum("view_count"),
            published_in_period=Count(
                "id",
                filter=Q(
                    status="published",
                    published_at__gte=(
                        period.datetime_from
                    ),
                    published_at__lt=(
                        period.datetime_to
                    ),
                ),
            ),
        )

        testimonials = Testimonial.objects.aggregate(
            total=Count("id"),
            published=Count(
                "id",
                filter=Q(status="published"),
            ),
            draft=Count(
                "id",
                filter=Q(status="draft"),
            ),
            review=Count(
                "id",
                filter=Q(status="review"),
            ),
            scheduled=Count(
                "id",
                filter=Q(status="scheduled"),
            ),
            archived=Count(
                "id",
                filter=Q(status="archived"),
            ),
            featured=Count(
                "id",
                filter=Q(is_featured=True),
            ),
            verified=Count(
                "id",
                filter=Q(is_verified=True),
            ),
            average_rating=Avg("rating"),
            published_in_period=Count(
                "id",
                filter=Q(
                    status="published",
                    published_at__gte=(
                        period.datetime_from
                    ),
                    published_at__lt=(
                        period.datetime_to
                    ),
                ),
            ),
        )

        for section in (
            insights,
            case_studies,
            testimonials,
        ):
            for key, value in tuple(section.items()):
                if value is None:
                    section[key] = 0

        testimonials["average_rating"] = round(
            float(
                testimonials[
                    "average_rating"
                ] or 0
            ),
            2,
        )

        return {
            "insights": insights,
            "case_studies": case_studies,
            "testimonials": testimonials,
        }

    @classmethod
    def content_publication_trend(cls, period):
        from collections import defaultdict

        from django.db.models import Count
        from django.db.models.functions import (
            TruncMonth,
        )

        models = (
            (
                "insights",
                "InsightArticle",
                "insights",
            ),
            (
                "case_studies",
                "CaseStudy",
                "case_studies",
            ),
            (
                "testimonials",
                "Testimonial",
                "testimonials",
            ),
        )

        totals = defaultdict(
            lambda: {
                "insights": 0,
                "case_studies": 0,
                "testimonials": 0,
            }
        )

        for app_label, model_name, key in models:
            model = cls._model(
                app_label,
                model_name,
            )

            rows = (
                model.objects.filter(
                    status="published",
                    published_at__gte=(
                        period.datetime_from
                    ),
                    published_at__lt=(
                        period.datetime_to
                    ),
                )
                .annotate(
                    month=TruncMonth(
                        "published_at"
                    )
                )
                .values("month")
                .annotate(total=Count("id"))
                .order_by("month")
            )

            for row in rows:
                totals[row["month"]][key] += (
                    row["total"]
                )

        return [
            {
                "month": month.date(),
                **totals[month],
                "total_published": sum(
                    totals[month].values()
                ),
            }
            for month in sorted(totals)
        ]

    @classmethod
    def testimonial_sources(cls):
        from django.db.models import (
            Avg,
            Count,
        )

        Testimonial = cls._model(
            "testimonials",
            "Testimonial",
        )

        labels = dict(
            Testimonial._meta.get_field(
                "source"
            ).choices
        )

        rows = list(
            Testimonial.objects.values("source")
            .annotate(
                total=Count("id"),
                average_rating=Avg("rating"),
            )
            .order_by("-total", "source")
        )

        return [
            {
                "source": row["source"],
                "label": labels.get(
                    row["source"],
                    row["source"],
                ),
                "total": row["total"],
                "average_rating": round(
                    float(
                        row["average_rating"]
                        or 0
                    ),
                    2,
                ),
            }
            for row in rows
        ]

    @classmethod
    def subscribers_summary(cls, period):
        from django.db.models import Count, Q

        Subscriber = cls._model(
            "newsletter",
            "Subscriber",
        )

        return Subscriber.objects.aggregate(
            total_subscribers=Count("id"),
            active_subscribers=Count(
                "id",
                filter=Q(status="active"),
            ),
            pending_subscribers=Count(
                "id",
                filter=Q(status="pending"),
            ),
            unsubscribed_subscribers=Count(
                "id",
                filter=Q(status="unsubscribed"),
            ),
            bounced_subscribers=Count(
                "id",
                filter=Q(status="bounced"),
            ),
            complained_subscribers=Count(
                "id",
                filter=Q(status="complained"),
            ),
            suppressed_subscribers=Count(
                "id",
                filter=Q(status="suppressed"),
            ),
            new_subscribers=Count(
                "id",
                filter=Q(
                    created_at__gte=(
                        period.datetime_from
                    ),
                    created_at__lt=(
                        period.datetime_to
                    ),
                ),
            ),
            subscribed_in_period=Count(
                "id",
                filter=Q(
                    subscribed_at__gte=(
                        period.datetime_from
                    ),
                    subscribed_at__lt=(
                        period.datetime_to
                    ),
                ),
            ),
            confirmed_in_period=Count(
                "id",
                filter=Q(
                    confirmed_at__gte=(
                        period.datetime_from
                    ),
                    confirmed_at__lt=(
                        period.datetime_to
                    ),
                ),
            ),
            unsubscribed_in_period=Count(
                "id",
                filter=Q(
                    unsubscribed_at__gte=(
                        period.datetime_from
                    ),
                    unsubscribed_at__lt=(
                        period.datetime_to
                    ),
                ),
            ),
        )

    @classmethod
    def subscribers_by_source(cls):
        from django.db.models import Count

        Subscriber = cls._model(
            "newsletter",
            "Subscriber",
        )

        labels = dict(
            Subscriber._meta.get_field(
                "source"
            ).choices
        )

        rows = list(
            Subscriber.objects.values("source")
            .annotate(total=Count("id"))
            .order_by("-total", "source")
        )

        return [
            {
                "source": row["source"],
                "label": labels.get(
                    row["source"],
                    row["source"],
                ),
                "total": row["total"],
            }
            for row in rows
        ]

    @classmethod
    def subscriber_trend(cls, period):
        from django.db.models import Count
        from django.db.models.functions import (
            TruncMonth,
        )

        Subscriber = cls._model(
            "newsletter",
            "Subscriber",
        )

        rows = list(
            Subscriber.objects.filter(
                created_at__gte=(
                    period.datetime_from
                ),
                created_at__lt=(
                    period.datetime_to
                ),
            )
            .annotate(
                month=TruncMonth("created_at")
            )
            .values("month")
            .annotate(
                new_subscribers=Count("id")
            )
            .order_by("month")
        )

        return [
            {
                "month": row["month"].date(),
                "new_subscribers": (
                    row["new_subscribers"]
                ),
            }
            for row in rows
        ]

    @classmethod
    def campaign_summary(cls, period):
        from django.db.models import (
            Count,
            Q,
            Sum,
        )

        Campaign = cls._model(
            "newsletter",
            "NewsletterCampaign",
        )

        metrics = Campaign.objects.aggregate(
            total_campaigns=Count("id"),
            draft_campaigns=Count(
                "id",
                filter=Q(status="draft"),
            ),
            review_campaigns=Count(
                "id",
                filter=Q(status="review"),
            ),
            scheduled_campaigns=Count(
                "id",
                filter=Q(status="scheduled"),
            ),
            queued_campaigns=Count(
                "id",
                filter=Q(status="queued"),
            ),
            sending_campaigns=Count(
                "id",
                filter=Q(status="sending"),
            ),
            sent_campaigns=Count(
                "id",
                filter=Q(status="sent"),
            ),
            paused_campaigns=Count(
                "id",
                filter=Q(status="paused"),
            ),
            cancelled_campaigns=Count(
                "id",
                filter=Q(status="cancelled"),
            ),
            failed_campaigns=Count(
                "id",
                filter=Q(status="failed"),
            ),
            archived_campaigns=Count(
                "id",
                filter=Q(status="archived"),
            ),
            recipient_count=Sum(
                "recipient_count"
            ),
            sent_count=Sum("sent_count"),
            delivered_count=Sum(
                "delivered_count"
            ),
            opened_count=Sum(
                "opened_count"
            ),
            clicked_count=Sum(
                "clicked_count"
            ),
            bounced_count=Sum(
                "bounced_count"
            ),
            failed_count=Sum("failed_count"),
            complained_count=Sum(
                "complained_count"
            ),
            unsubscribed_count=Sum(
                "unsubscribed_count"
            ),
            campaigns_sent_in_period=Count(
                "id",
                filter=Q(
                    sent_at__gte=(
                        period.datetime_from
                    ),
                    sent_at__lt=(
                        period.datetime_to
                    ),
                ),
            ),
        )

        for key, value in tuple(
            metrics.items()
        ):
            if value is None:
                metrics[key] = 0

        delivered = metrics["delivered_count"]

        metrics["open_rate"] = (
            round(
                metrics["opened_count"]
                / delivered
                * 100,
                2,
            )
            if delivered
            else 0.0
        )

        metrics["click_rate"] = (
            round(
                metrics["clicked_count"]
                / delivered
                * 100,
                2,
            )
            if delivered
            else 0.0
        )

        metrics["bounce_rate"] = (
            round(
                metrics["bounced_count"]
                / metrics["sent_count"]
                * 100,
                2,
            )
            if metrics["sent_count"]
            else 0.0
        )

        return metrics

    @classmethod
    def campaign_trend(cls, period):
        from django.db.models import (
            Count,
            Sum,
        )
        from django.db.models.functions import (
            TruncMonth,
        )

        Campaign = cls._model(
            "newsletter",
            "NewsletterCampaign",
        )

        rows = list(
            Campaign.objects.filter(
                sent_at__gte=(
                    period.datetime_from
                ),
                sent_at__lt=(
                    period.datetime_to
                ),
            )
            .annotate(
                month=TruncMonth("sent_at")
            )
            .values("month")
            .annotate(
                campaigns=Count("id"),
                sent_count=Sum("sent_count"),
                delivered_count=Sum(
                    "delivered_count"
                ),
                opened_count=Sum(
                    "opened_count"
                ),
                clicked_count=Sum(
                    "clicked_count"
                ),
                bounced_count=Sum(
                    "bounced_count"
                ),
            )
            .order_by("month")
        )

        result = []

        for row in rows:
            for key, value in tuple(
                row.items()
            ):
                if value is None:
                    row[key] = 0

            delivered = row["delivered_count"]
            sent = row["sent_count"]

            result.append(
                {
                    **row,
                    "month": row["month"].date(),
                    "open_rate": (
                        round(
                            row["opened_count"]
                            / delivered
                            * 100,
                            2,
                        )
                        if delivered
                        else 0.0
                    ),
                    "click_rate": (
                        round(
                            row["clicked_count"]
                            / delivered
                            * 100,
                            2,
                        )
                        if delivered
                        else 0.0
                    ),
                    "bounce_rate": (
                        round(
                            row["bounced_count"]
                            / sent
                            * 100,
                            2,
                        )
                        if sent
                        else 0.0
                    ),
                }
            )

        return result

    @classmethod
    def _enquiry_models(cls):
        return (
            cls._model(
                "enquiries",
                "ContactEnquiry",
            ),
            cls._model(
                "enquiries",
                "QuoteEnquiry",
            ),
        )

    @classmethod
    def enquiry_summary(cls, period):
        from django.db.models import (
            Count,
            Q,
        )

        combined = {
            "total_enquiries": 0,
            "open_enquiries": 0,
            "won_enquiries": 0,
            "lost_enquiries": 0,
            "spam_enquiries": 0,
            "archived_enquiries": 0,
            "enquiries_in_period": 0,
            "overdue_follow_ups": 0,
            "by_type": {},
        }

        now = timezone.now()

        for model in cls._enquiry_models():
            metrics = model.objects.aggregate(
                total=Count("id"),
                open=Count(
                    "id",
                    filter=Q(
                        status__in=(
                            cls.ENQUIRY_OPEN_STATUSES
                        ),
                    ),
                ),
                won=Count(
                    "id",
                    filter=Q(status="won"),
                ),
                lost=Count(
                    "id",
                    filter=Q(status="lost"),
                ),
                spam=Count(
                    "id",
                    filter=Q(status="spam"),
                ),
                archived=Count(
                    "id",
                    filter=Q(status="archived"),
                ),
                in_period=Count(
                    "id",
                    filter=Q(
                        submitted_at__gte=(
                            period.datetime_from
                        ),
                        submitted_at__lt=(
                            period.datetime_to
                        ),
                    ),
                ),
                overdue_follow_ups=Count(
                    "id",
                    filter=Q(
                        status__in=(
                            cls.ENQUIRY_OPEN_STATUSES
                        ),
                        next_follow_up_at__lt=now,
                    ),
                ),
            )

            model_key = model._meta.model_name
            combined["by_type"][
                model_key
            ] = metrics

            combined[
                "total_enquiries"
            ] += metrics["total"]
            combined[
                "open_enquiries"
            ] += metrics["open"]
            combined[
                "won_enquiries"
            ] += metrics["won"]
            combined[
                "lost_enquiries"
            ] += metrics["lost"]
            combined[
                "spam_enquiries"
            ] += metrics["spam"]
            combined[
                "archived_enquiries"
            ] += metrics["archived"]
            combined[
                "enquiries_in_period"
            ] += metrics["in_period"]
            combined[
                "overdue_follow_ups"
            ] += metrics[
                "overdue_follow_ups"
            ]

        closed = (
            combined["won_enquiries"]
            + combined["lost_enquiries"]
        )

        combined["closed_enquiries"] = closed
        combined["conversion_rate"] = (
            round(
                combined["won_enquiries"]
                / closed
                * 100,
                2,
            )
            if closed
            else 0.0
        )

        return combined

    @classmethod
    def enquiries_by_source(cls, period):
        from collections import defaultdict

        from django.db.models import Count, Q

        totals = defaultdict(
            lambda: {
                "total": 0,
                "won": 0,
                "lost": 0,
            }
        )
        labels = {}

        for model in cls._enquiry_models():
            labels.update(
                dict(
                    model._meta.get_field(
                        "source"
                    ).choices
                )
            )

            rows = (
                model.objects.filter(
                    submitted_at__gte=(
                        period.datetime_from
                    ),
                    submitted_at__lt=(
                        period.datetime_to
                    ),
                )
                .values("source")
                .annotate(
                    total=Count("id"),
                    won=Count(
                        "id",
                        filter=Q(status="won"),
                    ),
                    lost=Count(
                        "id",
                        filter=Q(status="lost"),
                    ),
                )
            )

            for row in rows:
                item = totals[row["source"]]
                item["total"] += row["total"]
                item["won"] += row["won"]
                item["lost"] += row["lost"]

        result = []

        for source, item in totals.items():
            closed = (
                item["won"] + item["lost"]
            )

            result.append(
                {
                    "source": source,
                    "label": labels.get(
                        source,
                        source,
                    ),
                    **item,
                    "conversion_rate": (
                        round(
                            item["won"]
                            / closed
                            * 100,
                            2,
                        )
                        if closed
                        else 0.0
                    ),
                }
            )

        return sorted(
            result,
            key=lambda row: (
                -row["total"],
                row["source"],
            ),
        )

    @classmethod
    def enquiry_trend(cls, period):
        from collections import defaultdict

        from django.db.models import Count, Q
        from django.db.models.functions import (
            TruncMonth,
        )

        totals = defaultdict(
            lambda: {
                "total": 0,
                "won": 0,
                "lost": 0,
            }
        )

        for model in cls._enquiry_models():
            rows = (
                model.objects.filter(
                    submitted_at__gte=(
                        period.datetime_from
                    ),
                    submitted_at__lt=(
                        period.datetime_to
                    ),
                )
                .annotate(
                    month=TruncMonth(
                        "submitted_at"
                    )
                )
                .values("month")
                .annotate(
                    total=Count("id"),
                    won=Count(
                        "id",
                        filter=Q(status="won"),
                    ),
                    lost=Count(
                        "id",
                        filter=Q(status="lost"),
                    ),
                )
            )

            for row in rows:
                item = totals[row["month"]]
                item["total"] += row["total"]
                item["won"] += row["won"]
                item["lost"] += row["lost"]

        return [
            {
                "month": month.date(),
                **totals[month],
                "conversion_rate": (
                    round(
                        totals[month]["won"]
                        / (
                            totals[month]["won"]
                            + totals[month]["lost"]
                        )
                        * 100,
                        2,
                    )
                    if (
                        totals[month]["won"]
                        + totals[month]["lost"]
                    )
                    else 0.0
                ),
            }
            for month in sorted(totals)
        ]

    @classmethod
    def build(cls, period, now):
        return {
            "summary": {
                "content": cls.content_summary(
                    period
                ),
                "subscribers": (
                    cls.subscribers_summary(
                        period
                    )
                ),
                "campaigns": (
                    cls.campaign_summary(period)
                ),
                "enquiries": (
                    cls.enquiry_summary(period)
                ),
            },
            "content_publication_trend": (
                cls.content_publication_trend(
                    period
                )
            ),
            "testimonial_sources": (
                cls.testimonial_sources()
            ),
            "subscribers_by_source": (
                cls.subscribers_by_source()
            ),
            "subscriber_trend": (
                cls.subscriber_trend(period)
            ),
            "campaign_trend": (
                cls.campaign_trend(period)
            ),
            "enquiries_by_source": (
                cls.enquiries_by_source(period)
            ),
            "enquiry_trend": (
                cls.enquiry_trend(period)
            ),
            "metadata": {
                "insight_model": (
                    "insights.InsightArticle"
                ),
                "content_date_basis": (
                    "published_at"
                ),
                "subscriber_date_basis": (
                    "created_at"
                ),
                "campaign_date_basis": (
                    "sent_at"
                ),
                "enquiry_date_basis": (
                    "submitted_at"
                ),
                "enquiry_conversion_definition": (
                    "won divided by won plus lost"
                ),
            },
        }


class TeamReportingRepository:
    CURRENT_EMPLOYMENT_STATUSES = {
        "active",
        "on_leave",
    }

    @staticmethod
    def _model(model_name):
        from django.apps import apps

        return apps.get_model(
            "team_management",
            model_name,
        )

    @classmethod
    def period_queryset(cls, period):
        TeamMember = cls._model("TeamMember")

        return TeamMember.objects.filter(
            created_at__gte=period.datetime_from,
            created_at__lt=period.datetime_to,
        )

    @classmethod
    def summary(cls, period):
        from django.db.models import Count, Q

        Team = cls._model("Team")
        TeamMember = cls._model("TeamMember")
        TeamMembership = cls._model(
            "TeamMembership"
        )

        member_metrics = TeamMember.objects.aggregate(
            total_members=Count("id"),
            active_members=Count(
                "id",
                filter=Q(
                    employment_status="active",
                ),
            ),
            members_on_leave=Count(
                "id",
                filter=Q(
                    employment_status="on_leave",
                ),
            ),
            current_members=Count(
                "id",
                filter=Q(
                    employment_status__in=(
                        cls.CURRENT_EMPLOYMENT_STATUSES
                    ),
                ),
            ),
            inactive_members=Count(
                "id",
                filter=~Q(
                    employment_status__in=(
                        cls.CURRENT_EMPLOYMENT_STATUSES
                    ),
                ),
            ),
            leadership_members=Count(
                "id",
                filter=Q(is_leadership=True),
            ),
            public_members=Count(
                "id",
                filter=Q(is_public=True),
            ),
            members_without_managers=Count(
                "id",
                filter=Q(
                    employment_status__in=(
                        cls.CURRENT_EMPLOYMENT_STATUSES
                    ),
                    reports_to__isnull=True,
                ),
            ),
            members_without_user_accounts=Count(
                "id",
                filter=Q(
                    employment_status__in=(
                        cls.CURRENT_EMPLOYMENT_STATUSES
                    ),
                    user__isnull=True,
                ),
            ),
        )

        membership_metrics = (
            TeamMembership.objects.aggregate(
                active_memberships=Count(
                    "id",
                    filter=Q(is_active=True),
                ),
                active_primary_memberships=Count(
                    "id",
                    filter=Q(
                        is_active=True,
                        is_primary=True,
                    ),
                ),
            )
        )

        members_without_primary_teams = (
            TeamMember.objects.filter(
                employment_status__in=(
                    cls.CURRENT_EMPLOYMENT_STATUSES
                ),
            )
            .exclude(
                team_memberships__is_active=True,
                team_memberships__is_primary=True,
            )
            .distinct()
            .count()
        )

        team_metrics = Team.objects.aggregate(
            total_teams=Count("id"),
            active_teams=Count(
                "id",
                filter=Q(is_active=True),
            ),
            public_teams=Count(
                "id",
                filter=Q(is_public=True),
            ),
            teams_without_managers=Count(
                "id",
                filter=Q(
                    is_active=True,
                    manager__isnull=True,
                ),
            ),
            root_teams=Count(
                "id",
                filter=Q(parent__isnull=True),
            ),
        )

        period_metrics = cls.period_queryset(
            period
        ).aggregate(
            new_members=Count("id"),
            new_active_members=Count(
                "id",
                filter=Q(
                    employment_status="active",
                ),
            ),
        )

        joined_in_period = (
            TeamMember.objects.filter(
                joined_at__gte=period.date_from,
                joined_at__lte=period.date_to,
            ).count()
        )

        ended_in_period = (
            TeamMember.objects.filter(
                employment_ended_at__gte=(
                    period.date_from
                ),
                employment_ended_at__lte=(
                    period.date_to
                ),
            ).count()
        )

        return {
            **member_metrics,
            **membership_metrics,
            **team_metrics,
            **period_metrics,
            "members_without_primary_teams": (
                members_without_primary_teams
            ),
            "joined_in_period": joined_in_period,
            "employment_ended_in_period": (
                ended_in_period
            ),
        }

    @classmethod
    def members_by_employment_status(cls):
        from django.db.models import Count

        TeamMember = cls._model("TeamMember")

        totals = {
            row["employment_status"]: row["total"]
            for row in (
                TeamMember.objects
                .values("employment_status")
                .annotate(total=Count("id"))
            )
        }

        return [
            {
                "employment_status": value,
                "label": label,
                "total": totals.get(value, 0),
            }
            for value, label in (
                TeamMember._meta.get_field(
                    "employment_status"
                ).choices
            )
        ]

    @classmethod
    def members_by_engagement_type(cls):
        from django.db.models import Count

        TeamMember = cls._model("TeamMember")

        totals = {
            row["engagement_type"]: row["total"]
            for row in (
                TeamMember.objects
                .filter(
                    employment_status__in=(
                        cls.CURRENT_EMPLOYMENT_STATUSES
                    ),
                )
                .values("engagement_type")
                .annotate(total=Count("id"))
            )
        }

        return [
            {
                "engagement_type": value,
                "label": label,
                "total": totals.get(value, 0),
            }
            for value, label in (
                TeamMember._meta.get_field(
                    "engagement_type"
                ).choices
            )
        ]

    @classmethod
    def members_by_work_location(cls):
        from django.db.models import Count

        TeamMember = cls._model("TeamMember")

        totals = {
            row["work_location_type"]: (
                row["total"]
            )
            for row in (
                TeamMember.objects
                .filter(
                    employment_status__in=(
                        cls.CURRENT_EMPLOYMENT_STATUSES
                    ),
                )
                .values("work_location_type")
                .annotate(total=Count("id"))
            )
        }

        return [
            {
                "work_location_type": value,
                "label": label,
                "total": totals.get(value, 0),
            }
            for value, label in (
                TeamMember._meta.get_field(
                    "work_location_type"
                ).choices
            )
        ]

    @classmethod
    def members_by_country(cls):
        from django.db.models import Count

        TeamMember = cls._model("TeamMember")

        rows = list(
            TeamMember.objects.filter(
                employment_status__in=(
                    cls.CURRENT_EMPLOYMENT_STATUSES
                ),
            )
            .values("country")
            .annotate(total=Count("id"))
            .order_by("-total", "country")
        )

        return [
            {
                "country": (
                    row["country"]
                    or "Not specified"
                ),
                "total": row["total"],
            }
            for row in rows
        ]

    @classmethod
    def members_by_team(cls):
        from django.db.models import (
            Count,
            Q,
        )

        Team = cls._model("Team")

        rows = list(
            Team.objects.annotate(
                total_members=Count(
                    "memberships__member",
                    distinct=True,
                ),
                active_members=Count(
                    "memberships__member",
                    filter=Q(
                        memberships__is_active=True,
                        memberships__member__employment_status__in=(
                            cls.CURRENT_EMPLOYMENT_STATUSES
                        ),
                    ),
                    distinct=True,
                ),
                primary_members=Count(
                    "memberships__member",
                    filter=Q(
                        memberships__is_active=True,
                        memberships__is_primary=True,
                        memberships__member__employment_status__in=(
                            cls.CURRENT_EMPLOYMENT_STATUSES
                        ),
                    ),
                    distinct=True,
                ),
            )
            .values(
                "id",
                "name",
                "slug",
                "team_type",
                "is_active",
                "manager_id",
                "manager__employee_code",
                "manager__first_name",
                "manager__last_name",
                "manager__preferred_name",
                "total_members",
                "active_members",
                "primary_members",
            )
            .order_by(
                "-active_members",
                "name",
            )
        )

        result = []

        for row in rows:
            manager_name = None

            if row["manager_id"] is not None:
                full_name = (
                    f"{row['manager__first_name'] or ''} "
                    f"{row['manager__last_name'] or ''}"
                ).strip()

                manager_name = (
                    row["manager__preferred_name"]
                    or full_name
                    or row["manager__employee_code"]
                )

            result.append(
                {
                    "team_id": row["id"],
                    "team_name": row["name"],
                    "slug": row["slug"],
                    "team_type": row["team_type"],
                    "is_active": row["is_active"],
                    "manager_id": row["manager_id"],
                    "manager_name": manager_name,
                    "total_members": (
                        row["total_members"]
                    ),
                    "active_members": (
                        row["active_members"]
                    ),
                    "primary_members": (
                        row["primary_members"]
                    ),
                }
            )

        return result

    @classmethod
    def management_span(cls):
        from django.db.models import Count, Q

        TeamMember = cls._model("TeamMember")

        rows = list(
            TeamMember.objects.filter(
                direct_reports__employment_status__in=(
                    cls.CURRENT_EMPLOYMENT_STATUSES
                ),
            )
            .annotate(
                direct_report_count=Count(
                    "direct_reports",
                    filter=Q(
                        direct_reports__employment_status__in=(
                            cls.CURRENT_EMPLOYMENT_STATUSES
                        ),
                    ),
                    distinct=True,
                )
            )
            .values(
                "id",
                "employee_code",
                "first_name",
                "last_name",
                "preferred_name",
                "job_title",
                "employment_status",
                "direct_report_count",
            )
            .order_by(
                "-direct_report_count",
                "first_name",
            )
        )

        return [
            {
                "member_id": row["id"],
                "employee_code": (
                    row["employee_code"]
                ),
                "member_name": (
                    row["preferred_name"]
                    or (
                        f"{row['first_name']} "
                        f"{row['last_name']}"
                    ).strip()
                ),
                "job_title": row["job_title"],
                "employment_status": (
                    row["employment_status"]
                ),
                "direct_report_count": (
                    row["direct_report_count"]
                ),
            }
            for row in rows
        ]

    @classmethod
    def members_without_primary_team(cls):
        TeamMember = cls._model("TeamMember")

        rows = list(
            TeamMember.objects.filter(
                employment_status__in=(
                    cls.CURRENT_EMPLOYMENT_STATUSES
                ),
            )
            .exclude(
                team_memberships__is_active=True,
                team_memberships__is_primary=True,
            )
            .values(
                "id",
                "employee_code",
                "first_name",
                "last_name",
                "preferred_name",
                "job_title",
                "employment_status",
            )
            .distinct()
            .order_by(
                "first_name",
                "last_name",
            )
        )

        return [
            {
                "member_id": row["id"],
                "employee_code": (
                    row["employee_code"]
                ),
                "member_name": (
                    row["preferred_name"]
                    or (
                        f"{row['first_name']} "
                        f"{row['last_name']}"
                    ).strip()
                ),
                "job_title": row["job_title"],
                "employment_status": (
                    row["employment_status"]
                ),
            }
            for row in rows
        ]

    @classmethod
    def members_without_manager(cls):
        TeamMember = cls._model("TeamMember")

        rows = list(
            TeamMember.objects.filter(
                employment_status__in=(
                    cls.CURRENT_EMPLOYMENT_STATUSES
                ),
                reports_to__isnull=True,
            )
            .values(
                "id",
                "employee_code",
                "first_name",
                "last_name",
                "preferred_name",
                "job_title",
                "employment_status",
                "is_leadership",
            )
            .order_by(
                "-is_leadership",
                "first_name",
                "last_name",
            )
        )

        return [
            {
                "member_id": row["id"],
                "employee_code": (
                    row["employee_code"]
                ),
                "member_name": (
                    row["preferred_name"]
                    or (
                        f"{row['first_name']} "
                        f"{row['last_name']}"
                    ).strip()
                ),
                "job_title": row["job_title"],
                "employment_status": (
                    row["employment_status"]
                ),
                "is_leadership": (
                    row["is_leadership"]
                ),
            }
            for row in rows
        ]

    @classmethod
    def team_type_distribution(cls):
        from django.db.models import Count

        Team = cls._model("Team")

        totals = {
            row["team_type"]: row["total"]
            for row in (
                Team.objects
                .values("team_type")
                .annotate(total=Count("id"))
            )
        }

        return [
            {
                "team_type": value,
                "label": label,
                "total": totals.get(value, 0),
            }
            for value, label in (
                Team._meta.get_field(
                    "team_type"
                ).choices
            )
        ]

    @classmethod
    def joiner_trend(cls, period):
        from django.db.models import Count
        from django.db.models.functions import (
            TruncMonth,
        )

        TeamMember = cls._model("TeamMember")

        rows = list(
            TeamMember.objects.filter(
                joined_at__gte=period.date_from,
                joined_at__lte=period.date_to,
            )
            .annotate(
                month=TruncMonth("joined_at")
            )
            .values("month")
            .annotate(joined_members=Count("id"))
            .order_by("month")
        )

        return [
            {
                "month": row["month"],
                "joined_members": (
                    row["joined_members"]
                ),
            }
            for row in rows
        ]

    @classmethod
    def build(cls, period, now):
        return {
            "summary": cls.summary(period),
            "members_by_team": (
                cls.members_by_team()
            ),
            "members_by_employment_status": (
                cls.members_by_employment_status()
            ),
            "members_by_engagement_type": (
                cls.members_by_engagement_type()
            ),
            "members_by_work_location": (
                cls.members_by_work_location()
            ),
            "members_by_country": (
                cls.members_by_country()
            ),
            "team_type_distribution": (
                cls.team_type_distribution()
            ),
            "management_span": (
                cls.management_span()
            ),
            "members_without_primary_team": (
                cls.members_without_primary_team()
            ),
            "members_without_manager": (
                cls.members_without_manager()
            ),
            "joiner_trend": (
                cls.joiner_trend(period)
            ),
            "metadata": {
                "current_member_definition": (
                    "employment status active "
                    "or on_leave"
                ),
                "primary_team_definition": (
                    "active TeamMembership with "
                    "is_primary true"
                ),
                "manager_definition": (
                    "TeamMember.reports_to"
                ),
                "team_manager_definition": (
                    "Team.manager"
                ),
            },
        }
