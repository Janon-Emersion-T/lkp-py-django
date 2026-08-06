from datetime import date, timedelta
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils import timezone

from apps.api.api import api

from .models import (
    DashboardPeriodPreset,
    DashboardReportSnapshot,
    DashboardReportType,
)
from .repositories import (
    DashboardSnapshotRepository,
    normalize_environment,
)
from .services import (
    DashboardPeriodService,
    DashboardReportFoundationService,
    DashboardSnapshotService,
)


class DashboardPeriodServiceTests(TestCase):
    def setUp(self):
        self.reference_date = date(2026, 8, 6)

    def test_today_period(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.TODAY,
            reference_date=self.reference_date,
        )

        self.assertEqual(
            period.date_from,
            self.reference_date,
        )
        self.assertEqual(
            period.date_to,
            self.reference_date,
        )

    def test_this_week_period_starts_on_monday(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_WEEK,
            reference_date=self.reference_date,
        )

        self.assertEqual(
            period.date_from,
            date(2026, 8, 3),
        )
        self.assertEqual(
            period.date_to,
            date(2026, 8, 6),
        )

    def test_this_month_period(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=self.reference_date,
        )

        self.assertEqual(
            period.date_from,
            date(2026, 8, 1),
        )
        self.assertEqual(
            period.date_to,
            date(2026, 8, 6),
        )

    def test_this_quarter_period(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_QUARTER,
            reference_date=self.reference_date,
        )

        self.assertEqual(
            period.date_from,
            date(2026, 7, 1),
        )
        self.assertEqual(
            period.date_to,
            date(2026, 8, 6),
        )

    def test_this_year_period(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_YEAR,
            reference_date=self.reference_date,
        )

        self.assertEqual(
            period.date_from,
            date(2026, 1, 1),
        )
        self.assertEqual(
            period.date_to,
            date(2026, 8, 6),
        )

    def test_last_7_days_period_is_inclusive(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.LAST_7_DAYS,
            reference_date=self.reference_date,
        )

        self.assertEqual(
            period.date_from,
            date(2026, 7, 31),
        )
        self.assertEqual(
            period.date_to,
            date(2026, 8, 6),
        )

    def test_last_30_days_period_is_inclusive(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.LAST_30_DAYS,
            reference_date=self.reference_date,
        )

        self.assertEqual(
            period.date_from,
            date(2026, 7, 8),
        )
        self.assertEqual(
            period.date_to,
            date(2026, 8, 6),
        )

    def test_last_90_days_period_is_inclusive(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.LAST_90_DAYS,
            reference_date=self.reference_date,
        )

        self.assertEqual(
            period.date_from,
            date(2026, 5, 9),
        )
        self.assertEqual(
            period.date_to,
            date(2026, 8, 6),
        )

    def test_custom_period_requires_both_dates(self):
        with self.assertRaisesMessage(
            ValueError,
            "date_from and date_to are required",
        ):
            DashboardPeriodService.resolve(
                preset=DashboardPeriodPreset.CUSTOM,
                date_from=date(2026, 8, 1),
            )

    def test_custom_period_rejects_reversed_dates(self):
        with self.assertRaisesMessage(
            ValueError,
            "date_to cannot be before date_from",
        ):
            DashboardPeriodService.resolve(
                preset=DashboardPeriodPreset.CUSTOM,
                date_from=date(2026, 8, 6),
                date_to=date(2026, 8, 1),
            )

    def test_non_custom_period_rejects_explicit_dates(self):
        with self.assertRaisesMessage(
            ValueError,
            "may only be supplied with the custom period",
        ):
            DashboardPeriodService.resolve(
                preset=DashboardPeriodPreset.THIS_MONTH,
                date_from=date(2026, 8, 1),
            )

    def test_datetime_range_uses_exclusive_end(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.TODAY,
            reference_date=self.reference_date,
        )

        self.assertEqual(
            period.datetime_to.date(),
            self.reference_date + timedelta(days=1),
        )


class DashboardEnvironmentTests(TestCase):
    def test_environment_is_normalized(self):
        self.assertEqual(
            normalize_environment(" Production "),
            "production",
        )

    def test_invalid_environment_is_rejected(self):
        with self.assertRaisesMessage(
            ValueError,
            "Invalid dashboard reporting environment",
        ):
            normalize_environment("unknown")


class DashboardReportFoundationServiceTests(TestCase):
    def test_foundation_context_contains_period_metadata(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = (
            DashboardReportFoundationService
            .build_report_context(
                report_type=DashboardReportType.EXECUTIVE,
                period=period,
                environment="test",
            )
        )

        self.assertEqual(
            report["report_type"],
            DashboardReportType.EXECUTIVE,
        )
        self.assertEqual(
            report["environment"],
            "test",
        )
        self.assertEqual(
            report["period"]["date_from"],
            "2026-08-01",
        )
        self.assertIn("summary", report["data"])
        self.assertIn("clients", report["data"])
        self.assertIn("crm", report["data"])
        self.assertIn("finance", report["data"])
        self.assertFalse(
            report["metadata"]["foundation"]
        )
        self.assertEqual(
            report["metadata"]["aggregation_status"],
            "complete",
        )


class DashboardSnapshotServiceTests(TestCase):
    def test_snapshot_checksum_is_deterministic(self):
        first = DashboardSnapshotService.checksum(
            {"b": 2, "a": 1}
        )
        second = DashboardSnapshotService.checksum(
            {"a": 1, "b": 2}
        )

        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)

    def test_generate_creates_versioned_snapshot(self):
        first = DashboardSnapshotService.generate(
            report_type=DashboardReportType.EXECUTIVE,
            period_preset=DashboardPeriodPreset.THIS_MONTH,
            environment="test",
        )

        second = DashboardSnapshotService.generate(
            report_type=DashboardReportType.EXECUTIVE,
            period_preset=DashboardPeriodPreset.THIS_MONTH,
            environment="test",
        )

        first.refresh_from_db()
        second.refresh_from_db()

        self.assertEqual(first.version, 1)
        self.assertEqual(second.version, 2)
        self.assertFalse(first.is_active)
        self.assertTrue(second.is_active)
        self.assertEqual(len(second.checksum), 64)
        self.assertGreater(
            second.expires_at,
            second.generated_at,
        )

    def test_latest_ignores_expired_snapshot(self):
        snapshot = DashboardSnapshotService.generate(
            report_type=DashboardReportType.CRM,
            period_preset=DashboardPeriodPreset.TODAY,
            environment="test",
        )

        DashboardReportSnapshot.objects.filter(
            id=snapshot.id
        ).update(
            expires_at=timezone.now()
            - timedelta(minutes=1)
        )

        latest = DashboardSnapshotRepository.latest(
            report_type=DashboardReportType.CRM,
            period_preset=DashboardPeriodPreset.TODAY,
            date_from=timezone.localdate(),
            date_to=timezone.localdate(),
            environment="test",
        )

        self.assertIsNone(latest)

    def test_invalidate_deactivates_matching_snapshots(self):
        DashboardSnapshotService.generate(
            report_type=DashboardReportType.TEAM,
            period_preset=DashboardPeriodPreset.THIS_MONTH,
            environment="test",
        )

        count = DashboardSnapshotRepository.invalidate(
            report_type=DashboardReportType.TEAM,
            environment="test",
        )

        self.assertEqual(count, 1)
        self.assertFalse(
            DashboardReportSnapshot.objects.get().is_active
        )

    def test_refresh_all_generates_every_report_type(self):
        snapshots = DashboardSnapshotService.refresh_all(
            period_preset=DashboardPeriodPreset.THIS_MONTH,
            environment="test",
        )

        self.assertEqual(
            len(snapshots),
            len(DashboardReportType.choices),
        )

        self.assertEqual(
            DashboardReportSnapshot.objects.count(),
            len(DashboardReportType.choices),
        )

    def test_expiry_minutes_must_be_positive(self):
        with self.assertRaisesMessage(
            ValueError,
            "expiry_minutes must be at least 1",
        ):
            DashboardSnapshotService.generate(
                report_type=DashboardReportType.FINANCE,
                period_preset=DashboardPeriodPreset.THIS_MONTH,
                environment="test",
                expiry_minutes=0,
            )


class DashboardReportingCommandTests(TestCase):
    def test_refresh_command_generates_snapshots(self):
        call_command(
            "refresh_dashboard_reports",
            period=DashboardPeriodPreset.TODAY,
            environment="test",
            expiry_minutes=15,
        )

        self.assertEqual(
            DashboardReportSnapshot.objects.count(),
            len(DashboardReportType.choices),
        )

    def test_refresh_command_rejects_invalid_date(self):
        with self.assertRaises(CommandError):
            call_command(
                "refresh_dashboard_reports",
                period=DashboardPeriodPreset.CUSTOM,
                date_from="invalid",
                date_to="2026-08-06",
                environment="test",
            )


class DashboardReportingOpenApiTests(TestCase):
    def test_dashboard_reporting_routes_are_registered(self):
        schema = api.get_openapi_schema()
        paths = schema["paths"]

        expected_paths = {
            "/api/v1/dashboard-reporting/health",
            "/api/v1/dashboard-reporting/period",
            "/api/v1/dashboard-reporting/executive",
            "/api/v1/dashboard-reporting/crm",
            "/api/v1/dashboard-reporting/sales",
            "/api/v1/dashboard-reporting/projects",
            "/api/v1/dashboard-reporting/tasks",
            "/api/v1/dashboard-reporting/finance",
            (
                "/api/v1/dashboard-reporting/"
                "foundation/{report_type}"
            ),
            "/api/v1/dashboard-reporting/snapshots",
            (
                "/api/v1/dashboard-reporting/"
                "snapshots/generate"
            ),
            (
                "/api/v1/dashboard-reporting/"
                "snapshots/refresh-all"
            ),
            (
                "/api/v1/dashboard-reporting/"
                "snapshots/invalidate"
            ),
        }

        self.assertTrue(
            expected_paths.issubset(paths.keys()),
            expected_paths - paths.keys(),
        )

    def test_dashboard_reporting_routes_are_protected(self):
        schema = api.get_openapi_schema()
        paths = schema["paths"]

        for path, methods in paths.items():
            if not path.startswith(
                "/api/v1/dashboard-reporting/"
            ):
                continue

            for method, operation in methods.items():
                if method.lower() not in {
                    "get",
                    "post",
                    "put",
                    "patch",
                    "delete",
                }:
                    continue

                self.assertTrue(
                    operation.get("security"),
                    f"{method.upper()} {path} is not protected.",
                )


class ExecutiveDashboardRepositoryTests(TestCase):
    def test_empty_database_returns_zeroed_dashboard(self):
        from apps.dashboard_reporting.repositories import (
            ExecutiveDashboardRepository,
        )

        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = ExecutiveDashboardRepository.build(
            period,
            timezone.now(),
        )

        self.assertEqual(
            report["summary"]["total_clients"],
            0,
        )
        self.assertEqual(
            report["summary"]["active_clients"],
            0,
        )
        self.assertEqual(
            report["summary"]["total_leads"],
            0,
        )
        self.assertEqual(
            report["summary"]["lead_conversion_rate"],
            0.0,
        )
        self.assertEqual(
            report["projects"]["active_projects"],
            0,
        )
        self.assertEqual(
            report["tasks"]["open_tasks"],
            0,
        )
        self.assertEqual(
            report["finance"]["revenue_by_currency"],
            [],
        )
        self.assertEqual(
            report["finance"]["cash_and_bank_balances"],
            [],
        )

    def test_executive_foundation_report_uses_aggregation(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = (
            DashboardReportFoundationService
            .build_report_context(
                report_type=(
                    DashboardReportType.EXECUTIVE
                ),
                period=period,
                environment="test",
            )
        )

        self.assertFalse(
            report["metadata"]["foundation"]
        )
        self.assertEqual(
            report["metadata"]["aggregation_status"],
            "complete",
        )
        self.assertIn("summary", report["data"])
        self.assertIn("finance", report["data"])

    def test_unimplemented_reports_remain_foundations(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = (
            DashboardReportFoundationService
            .build_report_context(
                report_type=(
                    DashboardReportType.CONTENT_MARKETING
                ),
                period=period,
                environment="test",
            )
        )

        self.assertTrue(
            report["metadata"]["foundation"]
        )
        self.assertEqual(
            report["metadata"]["aggregation_status"],
            "foundation_ready",
        )
        self.assertEqual(report["data"], {})

    def test_executive_snapshot_contains_real_data_shape(self):
        snapshot = DashboardSnapshotService.generate(
            report_type=DashboardReportType.EXECUTIVE,
            period_preset=DashboardPeriodPreset.THIS_MONTH,
            environment="test",
        )

        self.assertIn(
            "summary",
            snapshot.payload["data"],
        )
        self.assertIn(
            "clients",
            snapshot.payload["data"],
        )
        self.assertIn(
            "finance",
            snapshot.payload["data"],
        )
        self.assertEqual(
            snapshot.payload["metadata"][
                "aggregation_status"
            ],
            "complete",
        )


class ExecutiveDashboardOpenApiTests(TestCase):
    def test_executive_route_is_registered_and_protected(self):
        schema = api.get_openapi_schema()
        path = (
            "/api/v1/dashboard-reporting/executive"
        )

        self.assertIn(path, schema["paths"])
        self.assertIn("get", schema["paths"][path])
        self.assertTrue(
            schema["paths"][path]["get"].get(
                "security"
            )
        )


class CrmReportingRepositoryTests(TestCase):
    def test_empty_database_returns_complete_crm_shape(self):
        from apps.dashboard_reporting.repositories import (
            CrmReportingRepository,
        )

        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = CrmReportingRepository.build(
            period,
            timezone.now(),
        )

        expected_sections = {
            "summary",
            "leads_by_status",
            "leads_by_source",
            "leads_by_owner",
            "conversion_funnel",
            "monthly_lead_trend",
            "won_lost_trend",
            "estimated_value_by_currency",
            "metadata",
        }

        self.assertEqual(
            set(report),
            expected_sections,
        )
        self.assertEqual(
            report["summary"]["total_leads"],
            0,
        )
        self.assertEqual(
            report["summary"]["conversion_rate"],
            0.0,
        )
        self.assertEqual(
            report["leads_by_source"],
            [],
        )
        self.assertEqual(
            report["leads_by_owner"],
            [],
        )
        self.assertEqual(
            report["monthly_lead_trend"],
            [],
        )
        self.assertEqual(
            report["won_lost_trend"],
            [],
        )

    def test_status_distribution_contains_all_statuses(self):
        from apps.dashboard_reporting.repositories import (
            CrmReportingRepository,
        )
        from apps.crm.models import Lead

        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        rows = CrmReportingRepository.leads_by_status(
            period
        )

        expected_statuses = {
            value
            for value, _label
            in Lead._meta.get_field(
                "status"
            ).choices
        }

        actual_statuses = {
            row["status"]
            for row in rows
        }

        self.assertEqual(
            actual_statuses,
            expected_statuses,
        )
        self.assertTrue(
            all(row["total"] == 0 for row in rows)
        )

    def test_conversion_funnel_is_ordered(self):
        from apps.dashboard_reporting.repositories import (
            CrmReportingRepository,
        )

        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        funnel = (
            CrmReportingRepository
            .conversion_funnel(period)
        )

        self.assertEqual(
            [
                row["status"]
                for row in funnel
            ],
            list(
                CrmReportingRepository
                .FUNNEL_STAGES
            ),
        )

        self.assertEqual(
            [
                row["position"]
                for row in funnel
            ],
            list(
                range(
                    1,
                    len(funnel) + 1,
                )
            ),
        )

    def test_crm_service_report_is_complete(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = (
            DashboardReportFoundationService
            .build_report_context(
                report_type=DashboardReportType.CRM,
                period=period,
                environment="test",
            )
        )

        self.assertFalse(
            report["metadata"]["foundation"]
        )
        self.assertEqual(
            report["metadata"][
                "aggregation_status"
            ],
            "complete",
        )
        self.assertIn(
            "conversion_funnel",
            report["data"],
        )
        self.assertIn(
            "monthly_lead_trend",
            report["data"],
        )

    def test_crm_snapshot_contains_aggregations(self):
        snapshot = DashboardSnapshotService.generate(
            report_type=DashboardReportType.CRM,
            period_preset=DashboardPeriodPreset.THIS_MONTH,
            environment="test",
        )

        data = snapshot.payload["data"]

        self.assertIn("summary", data)
        self.assertIn("leads_by_status", data)
        self.assertIn("leads_by_source", data)
        self.assertIn("leads_by_owner", data)
        self.assertIn("conversion_funnel", data)
        self.assertIn("monthly_lead_trend", data)
        self.assertIn("won_lost_trend", data)


class CrmReportingOpenApiTests(TestCase):
    def test_crm_route_is_registered_and_protected(self):
        schema = api.get_openapi_schema()
        path = "/api/v1/dashboard-reporting/crm"

        self.assertIn(path, schema["paths"])
        self.assertIn(
            "get",
            schema["paths"][path],
        )
        self.assertTrue(
            schema["paths"][path]["get"].get(
                "security"
            )
        )


class SalesReportingRepositoryTests(TestCase):
    def test_empty_database_returns_complete_sales_shape(self):
        from apps.dashboard_reporting.repositories import (
            SalesReportingRepository,
        )

        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = SalesReportingRepository.build(
            period,
            timezone.now(),
        )

        required = {
            "summary",
            "quotations_by_status",
            "value_by_currency",
            "monthly_quotation_trend",
            "acceptance_trend",
            "expiry_ageing",
            "top_clients",
            "metadata",
        }

        self.assertEqual(set(report), required)

        self.assertEqual(
            report["summary"]["total_quotations"],
            0,
        )
        self.assertEqual(
            report["summary"][
                "quotation_conversion_rate"
            ],
            0.0,
        )
        self.assertEqual(
            report["value_by_currency"],
            [],
        )
        self.assertEqual(
            report["monthly_quotation_trend"],
            [],
        )
        self.assertEqual(
            report["acceptance_trend"],
            [],
        )
        self.assertEqual(
            report["top_clients"],
            [],
        )

    def test_status_distribution_contains_all_statuses(self):
        from apps.dashboard_reporting.repositories import (
            SalesReportingRepository,
        )
        from apps.quotations.models import Quotation

        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        rows = (
            SalesReportingRepository
            .quotations_by_status(period)
        )

        expected = {
            value
            for value, _label in (
                Quotation._meta.get_field(
                    "status"
                ).choices
            )
        }

        actual = {
            row["status"]
            for row in rows
        }

        self.assertEqual(actual, expected)

        self.assertTrue(
            all(
                row["total"] == 0
                for row in rows
            )
        )

    def test_sales_service_report_is_complete(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = (
            DashboardReportFoundationService
            .build_report_context(
                report_type=DashboardReportType.SALES,
                period=period,
                environment="test",
            )
        )

        self.assertFalse(
            report["metadata"]["foundation"]
        )
        self.assertEqual(
            report["metadata"][
                "aggregation_status"
            ],
            "complete",
        )
        self.assertIn(
            "quotations_by_status",
            report["data"],
        )
        self.assertIn(
            "value_by_currency",
            report["data"],
        )

    def test_sales_snapshot_contains_aggregations(self):
        snapshot = DashboardSnapshotService.generate(
            report_type=DashboardReportType.SALES,
            period_preset=DashboardPeriodPreset.THIS_MONTH,
            environment="test",
        )

        data = snapshot.payload["data"]

        self.assertIn("summary", data)
        self.assertIn(
            "quotations_by_status",
            data,
        )
        self.assertIn(
            "value_by_currency",
            data,
        )
        self.assertIn(
            "monthly_quotation_trend",
            data,
        )
        self.assertIn(
            "acceptance_trend",
            data,
        )
        self.assertIn(
            "expiry_ageing",
            data,
        )


class SalesReportingOpenApiTests(TestCase):
    def test_sales_route_is_registered_and_protected(self):
        schema = api.get_openapi_schema()
        path = (
            "/api/v1/dashboard-reporting/sales"
        )

        self.assertIn(path, schema["paths"])
        self.assertIn(
            "get",
            schema["paths"][path],
        )
        self.assertTrue(
            schema["paths"][path]["get"].get(
                "security"
            )
        )


class ProjectReportingRepositoryTests(TestCase):
    def test_empty_database_returns_complete_project_shape(self):
        from apps.dashboard_reporting.repositories import (
            ProjectReportingRepository,
        )

        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = ProjectReportingRepository.build(
            period,
            timezone.now(),
        )

        required = {
            "summary",
            "projects_by_status",
            "projects_by_priority",
            "projects_by_manager",
            "project_health",
            "overdue_projects",
            "budget_by_currency",
            "completion_trend",
            "creation_trend",
            "progress_distribution",
            "metadata",
        }

        self.assertEqual(set(report), required)
        self.assertEqual(
            report["summary"]["total_projects"],
            0,
        )
        self.assertEqual(
            report["summary"]["active_projects"],
            0,
        )
        self.assertEqual(
            report["summary"]["average_progress"],
            0.0,
        )
        self.assertEqual(
            report["projects_by_manager"],
            [],
        )
        self.assertEqual(
            report["overdue_projects"],
            [],
        )
        self.assertEqual(
            report["budget_by_currency"],
            [],
        )
        self.assertEqual(
            report["completion_trend"],
            [],
        )

    def test_status_distribution_contains_all_statuses(self):
        from apps.dashboard_reporting.repositories import (
            ProjectReportingRepository,
        )
        from apps.projects.models import Project

        rows = (
            ProjectReportingRepository
            .projects_by_status()
        )

        expected = {
            value
            for value, _label in (
                Project._meta.get_field(
                    "status"
                ).choices
            )
        }

        actual = {
            row["status"]
            for row in rows
        }

        self.assertEqual(actual, expected)
        self.assertTrue(
            all(
                row["total"] == 0
                for row in rows
            )
        )

    def test_project_health_contains_all_bands(self):
        from apps.dashboard_reporting.repositories import (
            ProjectReportingRepository,
        )

        rows = (
            ProjectReportingRepository
            .project_health(date(2026, 8, 6))
        )

        self.assertEqual(
            [row["health"] for row in rows],
            [
                "healthy",
                "at_risk",
                "overdue",
                "completed",
                "cancelled",
                "unknown",
            ],
        )

    def test_project_service_report_is_complete(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = (
            DashboardReportFoundationService
            .build_report_context(
                report_type=(
                    DashboardReportType.PROJECTS
                ),
                period=period,
                environment="test",
            )
        )

        self.assertFalse(
            report["metadata"]["foundation"]
        )
        self.assertEqual(
            report["metadata"][
                "aggregation_status"
            ],
            "complete",
        )
        self.assertIn(
            "project_health",
            report["data"],
        )
        self.assertIn(
            "overdue_projects",
            report["data"],
        )
        self.assertIn(
            "budget_by_currency",
            report["data"],
        )

    def test_project_snapshot_contains_aggregations(self):
        snapshot = DashboardSnapshotService.generate(
            report_type=DashboardReportType.PROJECTS,
            period_preset=DashboardPeriodPreset.THIS_MONTH,
            environment="test",
        )

        data = snapshot.payload["data"]

        self.assertIn("summary", data)
        self.assertIn(
            "projects_by_status",
            data,
        )
        self.assertIn(
            "projects_by_manager",
            data,
        )
        self.assertIn(
            "project_health",
            data,
        )
        self.assertIn(
            "overdue_projects",
            data,
        )
        self.assertIn(
            "completion_trend",
            data,
        )


class ProjectReportingOpenApiTests(TestCase):
    def test_projects_route_is_registered_and_protected(self):
        schema = api.get_openapi_schema()
        path = (
            "/api/v1/dashboard-reporting/projects"
        )

        self.assertIn(path, schema["paths"])
        self.assertIn(
            "get",
            schema["paths"][path],
        )
        self.assertTrue(
            schema["paths"][path]["get"].get(
                "security"
            )
        )


class TaskReportingRepositoryTests(TestCase):
    def test_empty_database_returns_complete_task_shape(self):
        from apps.dashboard_reporting.repositories import (
            TaskReportingRepository,
        )

        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = TaskReportingRepository.build(
            period,
            timezone.now(),
        )

        required = {
            "summary",
            "tasks_by_status",
            "tasks_by_priority",
            "workload_by_assignee",
            "unassigned_workload",
            "overdue_tasks",
            "tasks_by_project",
            "completion_trend",
            "creation_trend",
            "due_date_ageing",
            "metadata",
        }

        self.assertEqual(set(report), required)
        self.assertEqual(
            report["summary"]["total_tasks"],
            0,
        )
        self.assertEqual(
            report["summary"]["open_tasks"],
            0,
        )
        self.assertEqual(
            report["workload_by_assignee"],
            [],
        )
        self.assertEqual(
            report["overdue_tasks"],
            [],
        )

    def test_status_distribution_contains_all_statuses(self):
        from apps.dashboard_reporting.repositories import (
            TaskReportingRepository,
        )
        from apps.tasks.models import Task

        rows = TaskReportingRepository.tasks_by_status()

        expected = {
            value
            for value, _label in (
                Task._meta.get_field("status").choices
            )
        }

        actual = {
            row["status"]
            for row in rows
        }

        self.assertEqual(actual, expected)

    def test_priority_distribution_contains_all_priorities(self):
        from apps.dashboard_reporting.repositories import (
            TaskReportingRepository,
        )
        from apps.tasks.models import Task

        rows = (
            TaskReportingRepository.tasks_by_priority()
        )

        expected = {
            value
            for value, _label in (
                Task._meta.get_field("priority").choices
            )
        }

        actual = {
            row["priority"]
            for row in rows
        }

        self.assertEqual(actual, expected)

    def test_task_service_report_is_complete(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = (
            DashboardReportFoundationService
            .build_report_context(
                report_type=DashboardReportType.TASKS,
                period=period,
                environment="test",
            )
        )

        self.assertFalse(
            report["metadata"]["foundation"]
        )
        self.assertEqual(
            report["metadata"]["aggregation_status"],
            "complete",
        )
        self.assertIn(
            "workload_by_assignee",
            report["data"],
        )
        self.assertIn(
            "unassigned_workload",
            report["data"],
        )

    def test_task_snapshot_contains_aggregations(self):
        snapshot = DashboardSnapshotService.generate(
            report_type=DashboardReportType.TASKS,
            period_preset=DashboardPeriodPreset.THIS_MONTH,
            environment="test",
        )

        data = snapshot.payload["data"]

        self.assertIn("summary", data)
        self.assertIn("tasks_by_status", data)
        self.assertIn("tasks_by_priority", data)
        self.assertIn(
            "workload_by_assignee",
            data,
        )
        self.assertIn(
            "unassigned_workload",
            data,
        )
        self.assertIn("overdue_tasks", data)


class TaskReportingOpenApiTests(TestCase):
    def test_tasks_route_is_registered_and_protected(self):
        schema = api.get_openapi_schema()
        path = (
            "/api/v1/dashboard-reporting/tasks"
        )

        self.assertIn(path, schema["paths"])
        self.assertIn(
            "get",
            schema["paths"][path],
        )
        self.assertTrue(
            schema["paths"][path]["get"].get(
                "security"
            )
        )


class FinanceReportingRepositoryTests(TestCase):
    def test_empty_database_returns_complete_finance_shape(self):
        from apps.dashboard_reporting.repositories import (
            FinanceReportingRepository,
        )

        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = FinanceReportingRepository.build(
            period,
            timezone.now(),
        )

        required = {
            "summary",
            "invoice_value_by_currency",
            "payments_by_method",
            "expenses_by_category",
            "account_balances",
            "balances_by_type_and_currency",
            "monthly_finance_trend",
            "invoice_ageing",
            "transaction_activity",
            "metadata",
        }

        self.assertEqual(set(report), required)

        summary = report["summary"]

        self.assertEqual(
            summary["revenue_by_currency"],
            [],
        )
        self.assertEqual(
            summary["expenses_by_currency"],
            [],
        )
        self.assertEqual(
            summary["profit_by_currency"],
            [],
        )
        self.assertEqual(
            summary["total_invoices"],
            0,
        )
        self.assertEqual(
            summary["total_payments"],
            0,
        )
        self.assertEqual(
            report["account_balances"],
            [],
        )
        self.assertEqual(
            report["monthly_finance_trend"],
            [],
        )

    def test_profit_is_kept_separate_by_currency(self):
        from apps.dashboard_reporting.repositories import (
            FinanceReportingRepository,
        )

        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        self.assertEqual(
            FinanceReportingRepository
            .profit_by_currency(period),
            [],
        )

    def test_finance_service_report_is_complete(self):
        period = DashboardPeriodService.resolve(
            preset=DashboardPeriodPreset.THIS_MONTH,
            reference_date=date(2026, 8, 6),
        )

        report = (
            DashboardReportFoundationService
            .build_report_context(
                report_type=(
                    DashboardReportType.FINANCE
                ),
                period=period,
                environment="test",
            )
        )

        self.assertFalse(
            report["metadata"]["foundation"]
        )
        self.assertEqual(
            report["metadata"][
                "aggregation_status"
            ],
            "complete",
        )
        self.assertIn(
            "monthly_finance_trend",
            report["data"],
        )
        self.assertIn(
            "invoice_ageing",
            report["data"],
        )
        self.assertIn(
            "account_balances",
            report["data"],
        )

    def test_finance_snapshot_contains_aggregations(self):
        snapshot = DashboardSnapshotService.generate(
            report_type=DashboardReportType.FINANCE,
            period_preset=DashboardPeriodPreset.THIS_MONTH,
            environment="test",
        )

        data = snapshot.payload["data"]

        self.assertIn("summary", data)
        self.assertIn(
            "invoice_value_by_currency",
            data,
        )
        self.assertIn(
            "payments_by_method",
            data,
        )
        self.assertIn(
            "expenses_by_category",
            data,
        )
        self.assertIn(
            "account_balances",
            data,
        )
        self.assertIn(
            "monthly_finance_trend",
            data,
        )
        self.assertIn(
            "invoice_ageing",
            data,
        )


class FinanceReportingOpenApiTests(TestCase):
    def test_finance_route_is_registered_and_protected(self):
        schema = api.get_openapi_schema()
        path = (
            "/api/v1/dashboard-reporting/finance"
        )

        self.assertIn(path, schema["paths"])
        self.assertIn(
            "get",
            schema["paths"][path],
        )
        self.assertTrue(
            schema["paths"][path]["get"].get(
                "security"
            )
        )
