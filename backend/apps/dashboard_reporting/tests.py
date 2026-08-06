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
        self.assertEqual(report["data"], {})
        self.assertTrue(
            report["metadata"]["foundation"]
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
