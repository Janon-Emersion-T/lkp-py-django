from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import User
from apps.navigation.models import (
    MenuItemLinkType,
    MenuItemVisibility,
    NavigationLocation,
    NavigationMenu,
    NavigationMenuItem,
)
from apps.website_settings.models import (
    SettingEnvironment,
    WebsiteSetting,
    WebsiteSettingGroup,
)

from .models import (
    PublicSnapshotType,
    PublicWebsiteSnapshot,
)
from .repositories import (
    PublicSnapshotRepository,
    normalize_environment,
)
from .services import (
    PublicSnapshotService,
    PublicWebsiteService,
)


class RequestStub:
    def __init__(self, user):
        self.auth = user
        self.user = user
        self.META = {}
        self.headers = {}


class PublicWebsiteFixtureMixin:
    def create_public_configuration(self):
        group = WebsiteSettingGroup.objects.create(
            name="Public General",
            slug="public-general",
        )

        WebsiteSetting.objects.create(
            group=group,
            key="public-site-name",
            label="Public site name",
            value="LKProfessionals",
            environment=SettingEnvironment.GLOBAL,
            is_public=True,
        )

        menu = NavigationMenu.objects.create(
            name="Public Main",
            slug="public-main",
            location=(
                NavigationLocation.HEADER_PRIMARY
            ),
            is_active=True,
            is_public=True,
        )

        NavigationMenuItem.objects.create(
            menu=menu,
            label="Home",
            link_type=MenuItemLinkType.INTERNAL,
            url="/",
            visibility=(
                MenuItemVisibility.EVERYONE
            ),
            is_active=True,
        )

        return group, menu


class PublicWebsiteModelTests(TestCase):
    def test_snapshot_string(self):
        snapshot = PublicWebsiteSnapshot.objects.create(
            snapshot_type=(
                PublicSnapshotType.BOOTSTRAP
            ),
            environment="production",
            version=1,
        )

        self.assertEqual(
            str(snapshot),
            "bootstrap:production:v1",
        )

    def test_snapshot_expiry(self):
        snapshot = PublicWebsiteSnapshot.objects.create(
            snapshot_type=(
                PublicSnapshotType.BOOTSTRAP
            ),
            environment="production",
            expires_at=(
                timezone.now()
                - timedelta(minutes=1)
            ),
        )

        self.assertTrue(snapshot.is_expired)


class PublicWebsiteRepositoryTests(TestCase):
    def test_environment_validation(self):
        self.assertEqual(
            normalize_environment("production"),
            "production",
        )

        with self.assertRaises(ValueError):
            normalize_environment("invalid")

    def test_latest_snapshot_excludes_expired(self):
        PublicWebsiteSnapshot.objects.create(
            snapshot_type=(
                PublicSnapshotType.BOOTSTRAP
            ),
            environment="production",
            version=1,
            expires_at=(
                timezone.now()
                - timedelta(minutes=1)
            ),
        )

        active = PublicWebsiteSnapshot.objects.create(
            snapshot_type=(
                PublicSnapshotType.BOOTSTRAP
            ),
            environment="production",
            version=2,
            expires_at=(
                timezone.now()
                + timedelta(minutes=30)
            ),
        )

        latest = PublicSnapshotRepository.latest(
            PublicSnapshotType.BOOTSTRAP,
            "production",
        )

        self.assertEqual(latest.id, active.id)


class PublicWebsiteServiceTests(
    PublicWebsiteFixtureMixin,
    TestCase,
):
    def setUp(self):
        self.user = User.objects.create_user(
            username="public_website_admin",
            email="public-api@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.user)

        self.create_public_configuration()

    def test_build_settings(self):
        settings = (
            PublicWebsiteService.build_settings(
                "production"
            )
        )

        self.assertEqual(
            settings["public-site-name"],
            "LKProfessionals",
        )

    def test_build_navigation(self):
        navigation = (
            PublicWebsiteService.build_navigation()
        )

        menus = navigation["header_primary"]

        self.assertEqual(len(menus), 1)
        self.assertEqual(
            menus[0]["items"][0]["label"],
            "Home",
        )

    def test_build_bootstrap(self):
        payload = (
            PublicWebsiteService.build_bootstrap(
                "production"
            )
        )

        self.assertEqual(
            payload["environment"],
            "production",
        )
        self.assertIn("settings", payload)
        self.assertIn("navigation", payload)

    def test_generate_snapshot(self):
        snapshot = PublicSnapshotService.generate(
            request=self.request,
            snapshot_type=(
                PublicSnapshotType.BOOTSTRAP
            ),
            environment="production",
            ttl_minutes=30,
        )

        self.assertEqual(snapshot.version, 1)
        self.assertTrue(snapshot.is_active)
        self.assertTrue(snapshot.checksum)
        self.assertIn(
            "settings",
            snapshot.payload,
        )

    def test_generate_new_snapshot_deactivates_old(self):
        first = PublicSnapshotService.generate(
            request=self.request,
            snapshot_type=(
                PublicSnapshotType.BOOTSTRAP
            ),
            environment="production",
        )

        second = PublicSnapshotService.generate(
            request=self.request,
            snapshot_type=(
                PublicSnapshotType.BOOTSTRAP
            ),
            environment="production",
        )

        first.refresh_from_db()

        self.assertFalse(first.is_active)
        self.assertTrue(second.is_active)
        self.assertEqual(second.version, 2)

    def test_homepage_payload_has_sections(self):
        payload = (
            PublicWebsiteService.build_homepage(
                "production"
            )
        )

        expected = {
            "settings",
            "navigation",
            "featured_services",
            "featured_packages",
            "featured_industries",
            "latest_insights",
            "featured_case_studies",
            "featured_testimonials",
            "teams",
        }

        self.assertTrue(
            expected.issubset(payload)
        )



class PublicWebsiteFinalizationTests(
    PublicWebsiteFixtureMixin,
    TestCase,
):
    def setUp(self):
        self.user = User.objects.create_user(
            username="public_website_final",
            email="public-final@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.user)

        self.create_public_configuration()

    def test_invalidate_active_snapshots(self):
        first = PublicSnapshotService.generate(
            request=self.request,
            snapshot_type=(
                PublicSnapshotType.BOOTSTRAP
            ),
            environment="production",
        )

        second = PublicSnapshotService.generate(
            request=self.request,
            snapshot_type=(
                PublicSnapshotType.CATALOG
            ),
            environment="production",
        )

        count = PublicSnapshotService.invalidate(
            request=self.request,
            environment="production",
        )

        self.assertEqual(count, 2)

        first.refresh_from_db()
        second.refresh_from_db()

        self.assertFalse(first.is_active)
        self.assertFalse(second.is_active)

    def test_targeted_snapshot_invalidation(self):
        bootstrap = PublicSnapshotService.generate(
            request=self.request,
            snapshot_type=(
                PublicSnapshotType.BOOTSTRAP
            ),
            environment="production",
        )

        catalog = PublicSnapshotService.generate(
            request=self.request,
            snapshot_type=(
                PublicSnapshotType.CATALOG
            ),
            environment="production",
        )

        count = PublicSnapshotService.invalidate(
            request=self.request,
            snapshot_type=(
                PublicSnapshotType.BOOTSTRAP
            ),
            environment="production",
        )

        self.assertEqual(count, 1)

        bootstrap.refresh_from_db()
        catalog.refresh_from_db()

        self.assertFalse(bootstrap.is_active)
        self.assertTrue(catalog.is_active)

    def test_refresh_all_generates_four_snapshots(self):
        snapshots = (
            PublicSnapshotService.refresh_all(
                request=self.request,
                environment="production",
                ttl_minutes=15,
            )
        )

        self.assertEqual(len(snapshots), 4)

        snapshot_types = {
            snapshot.snapshot_type
            for snapshot in snapshots
        }

        self.assertEqual(
            snapshot_types,
            {
                PublicSnapshotType.BOOTSTRAP,
                PublicSnapshotType.HOMEPAGE,
                PublicSnapshotType.CATALOG,
                PublicSnapshotType.CONTENT,
            },
        )

        self.assertTrue(
            all(
                snapshot.is_active
                for snapshot in snapshots
            )
        )

    def test_refresh_command_is_repeatable(self):
        call_command(
            "refresh_public_snapshots",
            environment="production",
            ttl_minutes=10,
            verbosity=0,
        )

        self.assertEqual(
            PublicWebsiteSnapshot.objects.filter(
                environment="production",
                is_active=True,
            ).count(),
            4,
        )

        call_command(
            "refresh_public_snapshots",
            environment="production",
            ttl_minutes=10,
            verbosity=0,
        )

        active = (
            PublicWebsiteSnapshot.objects.filter(
                environment="production",
                is_active=True,
            )
        )

        self.assertEqual(active.count(), 4)

        for snapshot_type in (
            PublicSnapshotType.BOOTSTRAP,
            PublicSnapshotType.HOMEPAGE,
            PublicSnapshotType.CATALOG,
            PublicSnapshotType.CONTENT,
        ):
            snapshot = active.get(
                snapshot_type=snapshot_type
            )

            self.assertEqual(snapshot.version, 2)

    def test_snapshot_checksum_is_deterministic(self):
        payload = {
            "name": "LKProfessionals",
            "enabled": True,
            "items": [1, 2, 3],
        }

        first = PublicSnapshotService.checksum(
            payload
        )

        second = PublicSnapshotService.checksum(
            {
                "items": [1, 2, 3],
                "enabled": True,
                "name": "LKProfessionals",
            }
        )

        self.assertEqual(first, second)
