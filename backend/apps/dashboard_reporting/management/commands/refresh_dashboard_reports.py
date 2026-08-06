from datetime import date

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.dashboard_reporting.models import (
    DashboardPeriodPreset,
)
from apps.dashboard_reporting.services import (
    DashboardSnapshotService,
)


class Command(BaseCommand):
    help = (
        "Generate fresh snapshots for all dashboard "
        "report types."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--period",
            default=DashboardPeriodPreset.THIS_MONTH,
            choices=[
                value
                for value, _label
                in DashboardPeriodPreset.choices
            ],
        )
        parser.add_argument("--date-from")
        parser.add_argument("--date-to")
        parser.add_argument(
            "--environment",
            default="production",
        )
        parser.add_argument(
            "--expiry-minutes",
            type=int,
            default=30,
        )

    def parse_date(self, value, option_name):
        if not value:
            return None

        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise CommandError(
                f"{option_name} must use YYYY-MM-DD."
            ) from exc

    def handle(self, *args, **options):
        date_from = self.parse_date(
            options["date_from"],
            "--date-from",
        )
        date_to = self.parse_date(
            options["date_to"],
            "--date-to",
        )

        try:
            snapshots = DashboardSnapshotService.refresh_all(
                period_preset=options["period"],
                date_from=date_from,
                date_to=date_to,
                environment=options["environment"],
                expiry_minutes=options["expiry_minutes"],
            )
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(
                "Dashboard report snapshots refreshed: "
                f"{len(snapshots)} generated."
            )
        )

        for snapshot in snapshots:
            self.stdout.write(
                "  "
                f"{snapshot.report_type}: "
                f"v{snapshot.version} "
                f"({snapshot.checksum})"
            )
