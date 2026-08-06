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
