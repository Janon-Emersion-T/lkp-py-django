from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase

from apps.accounts.models import User

from .models import (
    SettingEnvironment,
    SettingValueType,
    WebsiteSetting,
    WebsiteSettingGroup,
)
from .repositories import (
    PublicWebsiteSettingRepository,
    WebsiteSettingRepository,
)
from .services import WebsiteSettingService


class RequestStub:
    def __init__(self, user):
        self.auth = user
        self.user = user
        self.META = {}
        self.headers = {}


class WebsiteSettingModelTests(TestCase):
    def setUp(self):
        self.group = WebsiteSettingGroup.objects.create(
            name="General",
            slug="general",
        )

    def test_string_setting_value(self):
        setting = WebsiteSetting.objects.create(
            group=self.group,
            key="site-name",
            label="Site name",
            value="LKProfessionals",
        )

        self.assertEqual(
            setting.typed_value,
            "LKProfessionals",
        )

    def test_integer_setting_value(self):
        setting = WebsiteSetting.objects.create(
            group=self.group,
            key="items-per-page",
            label="Items per page",
            value_type=SettingValueType.INTEGER,
            value="25",
        )

        self.assertEqual(setting.typed_value, 25)

    def test_decimal_setting_value(self):
        setting = WebsiteSetting.objects.create(
            group=self.group,
            key="tax-rate",
            label="Tax rate",
            value_type=SettingValueType.DECIMAL,
            value="18.50",
        )

        self.assertEqual(
            setting.typed_value,
            Decimal("18.50"),
        )

    def test_boolean_setting_value(self):
        setting = WebsiteSetting.objects.create(
            group=self.group,
            key="maintenance-mode",
            label="Maintenance mode",
            value_type=SettingValueType.BOOLEAN,
            value="true",
        )

        self.assertTrue(setting.typed_value)

    def test_invalid_integer_is_rejected(self):
        setting = WebsiteSetting(
            group=self.group,
            key="invalid-integer",
            label="Invalid integer",
            value_type=SettingValueType.INTEGER,
            value="not-an-integer",
        )

        with self.assertRaises(ValidationError):
            setting.full_clean()

    def test_invalid_email_is_rejected(self):
        setting = WebsiteSetting(
            group=self.group,
            key="contact-email",
            label="Contact email",
            value_type=SettingValueType.EMAIL,
            value="invalid-email",
        )

        with self.assertRaises(ValidationError):
            setting.full_clean()

    def test_invalid_color_is_rejected(self):
        setting = WebsiteSetting(
            group=self.group,
            key="brand-color",
            label="Brand color",
            value_type=SettingValueType.COLOR,
            value="red",
        )

        with self.assertRaises(ValidationError):
            setting.full_clean()


class WebsiteSettingRepositoryTests(TestCase):
    def setUp(self):
        self.group = WebsiteSettingGroup.objects.create(
            name="SEO",
            slug="seo",
        )

        self.global_setting = WebsiteSetting.objects.create(
            group=self.group,
            key="site-title",
            label="Site title",
            value="Global title",
            environment=SettingEnvironment.GLOBAL,
            is_public=True,
        )

        self.production_setting = (
            WebsiteSetting.objects.create(
                group=self.group,
                key="site-title",
                label="Production site title",
                value="Production title",
                environment=(
                    SettingEnvironment.PRODUCTION
                ),
                is_public=True,
            )
        )

        self.private_setting = WebsiteSetting.objects.create(
            group=self.group,
            key="internal-key",
            label="Internal key",
            value="secret",
            environment=SettingEnvironment.GLOBAL,
            is_public=False,
        )

    def test_find_setting_by_key(self):
        setting = WebsiteSettingRepository.find_by_key(
            "site-title",
            environment=SettingEnvironment.GLOBAL,
        )

        self.assertEqual(
            setting.id,
            self.global_setting.id,
        )

    def test_public_environment_overrides_global(self):
        resolved = (
            PublicWebsiteSettingRepository
            .values_for_environment(
                SettingEnvironment.PRODUCTION
            )
        )

        self.assertEqual(
            resolved["site-title"].id,
            self.production_setting.id,
        )

    def test_private_setting_is_excluded(self):
        resolved = (
            PublicWebsiteSettingRepository
            .values_for_environment(
                SettingEnvironment.PRODUCTION
            )
        )

        self.assertNotIn(
            "internal-key",
            resolved,
        )


class WebsiteSettingServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="website_settings_admin",
            email="settings-admin@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.user)

        self.group = WebsiteSettingGroup.objects.create(
            name="Company",
            slug="company",
        )

    def test_create_setting_group(self):
        group = WebsiteSettingService.create_group(
            request=self.request,
            values={
                "name": "Social",
                "slug": "social",
            },
        )

        self.assertEqual(group.name, "Social")

    def test_create_setting(self):
        setting = WebsiteSettingService.create_setting(
            request=self.request,
            values={
                "group": self.group,
                "key": "company-phone",
                "label": "Company phone",
                "value": "+94761234321",
            },
        )

        self.assertEqual(
            setting.typed_value,
            "+94761234321",
        )

    def test_update_setting(self):
        setting = WebsiteSetting.objects.create(
            group=self.group,
            key="company-name",
            label="Company name",
            value="Old company",
        )

        setting = WebsiteSettingService.update_setting(
            request=self.request,
            setting=setting,
            values={
                "value": "LKProfessionals",
            },
        )

        self.assertEqual(
            setting.value,
            "LKProfessionals",
        )

    def test_non_editable_setting_cannot_update(self):
        setting = WebsiteSetting.objects.create(
            group=self.group,
            key="protected-setting",
            label="Protected setting",
            value="protected",
            is_editable=False,
        )

        with self.assertRaises(ValueError):
            WebsiteSettingService.update_setting(
                request=self.request,
                setting=setting,
                values={
                    "value": "changed",
                },
            )

    def test_bulk_update_settings(self):
        first = WebsiteSetting.objects.create(
            group=self.group,
            key="first-setting",
            label="First setting",
            value="one",
        )

        second = WebsiteSetting.objects.create(
            group=self.group,
            key="second-setting",
            label="Second setting",
            value="two",
        )

        updated = (
            WebsiteSettingService.bulk_update_values(
                request=self.request,
                updates=[
                    {
                        "setting": first,
                        "value": "updated-one",
                    },
                    {
                        "setting": second,
                        "value": "updated-two",
                    },
                ],
            )
        )

        self.assertEqual(len(updated), 2)

        first.refresh_from_db()
        second.refresh_from_db()

        self.assertEqual(
            first.value,
            "updated-one",
        )
        self.assertEqual(
            second.value,
            "updated-two",
        )



class WebsiteSettingSeedCommandTests(TestCase):
    def test_seed_command_creates_default_groups(self):
        call_command(
            "seed_website_settings",
            verbosity=0,
        )

        self.assertTrue(
            WebsiteSettingGroup.objects.filter(
                slug="general",
            ).exists()
        )
        self.assertTrue(
            WebsiteSettingGroup.objects.filter(
                slug="contact",
            ).exists()
        )
        self.assertTrue(
            WebsiteSettingGroup.objects.filter(
                slug="seo",
            ).exists()
        )

    def test_seed_command_creates_public_settings(self):
        call_command(
            "seed_website_settings",
            verbosity=0,
        )

        site_name = WebsiteSetting.objects.get(
            key="site-name",
            environment=SettingEnvironment.GLOBAL,
        )

        self.assertEqual(
            site_name.typed_value,
            "LKProfessionals",
        )
        self.assertTrue(site_name.is_public)

        primary_phone = WebsiteSetting.objects.get(
            key="primary-phone",
            environment=SettingEnvironment.GLOBAL,
        )

        self.assertEqual(
            primary_phone.typed_value,
            "+94761234321",
        )

    def test_seed_command_is_idempotent(self):
        call_command(
            "seed_website_settings",
            verbosity=0,
        )

        group_count = (
            WebsiteSettingGroup.objects.count()
        )
        setting_count = WebsiteSetting.objects.count()

        call_command(
            "seed_website_settings",
            verbosity=0,
        )

        self.assertEqual(
            WebsiteSettingGroup.objects.count(),
            group_count,
        )
        self.assertEqual(
            WebsiteSetting.objects.count(),
            setting_count,
        )

    def test_public_repository_returns_seeded_values(self):
        call_command(
            "seed_website_settings",
            verbosity=0,
        )

        resolved = (
            PublicWebsiteSettingRepository
            .values_for_environment(
                SettingEnvironment.PRODUCTION
            )
        )

        self.assertIn("site-name", resolved)
        self.assertIn("primary-email", resolved)
        self.assertIn("maintenance-mode", resolved)

        self.assertEqual(
            resolved["site-name"].typed_value,
            "LKProfessionals",
        )
        self.assertFalse(
            resolved["maintenance-mode"].typed_value
        )
