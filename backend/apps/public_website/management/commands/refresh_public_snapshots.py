from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.public_website.repositories import (
    normalize_environment,
)
from apps.public_website.services import (
    PublicSnapshotService,
)


class Command(BaseCommand):
    help = (
        "Regenerate all public website API snapshots."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--environment",
            default="production",
        )

        parser.add_argument(
            "--ttl-minutes",
            type=int,
            default=30,
        )

    def handle(self, *args, **options):
        environment = options["environment"]
        ttl_minutes = options["ttl_minutes"]

        try:
            environment = normalize_environment(
                environment
            )
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        if ttl_minutes < 1:
            raise CommandError(
                "Snapshot TTL must be at least "
                "one minute."
            )

        snapshots = PublicSnapshotService.refresh_all(
            request=None,
            environment=environment,
            ttl_minutes=ttl_minutes,
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Public website snapshots refreshed: "
                f"{len(snapshots)} generated for "
                f"{environment}."
            )
        )

        for snapshot in snapshots:
            self.stdout.write(
                f"  {snapshot.snapshot_type}: "
                f"v{snapshot.version} "
                f"({snapshot.checksum})"
            )
