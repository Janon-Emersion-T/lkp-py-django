from django.core.management.base import BaseCommand
from django.db import transaction

from apps.website_settings.models import (
    SettingEnvironment,
    SettingValueType,
    WebsiteSetting,
    WebsiteSettingGroup,
)


GROUPS = [
    {
        "name": "General",
        "slug": "general",
        "description": (
            "General website identity and company information."
        ),
        "icon": "settings",
        "sort_order": 10,
    },
    {
        "name": "Contact",
        "slug": "contact",
        "description": (
            "Public contact information and communication channels."
        ),
        "icon": "contact",
        "sort_order": 20,
    },
    {
        "name": "Branding",
        "slug": "branding",
        "description": (
            "Brand colors, logos, and visual identity settings."
        ),
        "icon": "palette",
        "sort_order": 30,
    },
    {
        "name": "Social Media",
        "slug": "social-media",
        "description": (
            "Public social media profile links."
        ),
        "icon": "share",
        "sort_order": 40,
    },
    {
        "name": "SEO",
        "slug": "seo",
        "description": (
            "Global search-engine metadata defaults."
        ),
        "icon": "search",
        "sort_order": 50,
    },
    {
        "name": "Analytics",
        "slug": "analytics",
        "description": (
            "Public analytics and tracking identifiers."
        ),
        "icon": "chart",
        "sort_order": 60,
    },
    {
        "name": "Operations",
        "slug": "operations",
        "description": (
            "Operational website behaviour and maintenance settings."
        ),
        "icon": "tools",
        "sort_order": 70,
    },
]


SETTINGS = [
    {
        "group": "general",
        "key": "site-name",
        "label": "Site name",
        "value_type": SettingValueType.STRING,
        "value": "LKProfessionals",
        "is_public": True,
        "is_required": True,
        "sort_order": 10,
    },
    {
        "group": "general",
        "key": "company-legal-name",
        "label": "Company legal name",
        "value_type": SettingValueType.STRING,
        "value": "LKProfessionals (Pvt) Ltd",
        "is_public": True,
        "is_required": True,
        "sort_order": 20,
    },
    {
        "group": "general",
        "key": "company-short-name",
        "label": "Company short name",
        "value_type": SettingValueType.STRING,
        "value": "LKP",
        "is_public": True,
        "sort_order": 30,
    },
    {
        "group": "general",
        "key": "site-tagline",
        "label": "Site tagline",
        "value_type": SettingValueType.STRING,
        "value": (
            "Empowering Businesses Through Reliable IT Solutions."
        ),
        "is_public": True,
        "sort_order": 40,
    },
    {
        "group": "general",
        "key": "company-founded-year",
        "label": "Company founded year",
        "value_type": SettingValueType.INTEGER,
        "value": "2013",
        "is_public": True,
        "sort_order": 50,
    },
    {
        "group": "general",
        "key": "default-language",
        "label": "Default language",
        "value_type": SettingValueType.STRING,
        "value": "en",
        "is_public": True,
        "is_required": True,
        "sort_order": 60,
    },
    {
        "group": "general",
        "key": "default-timezone",
        "label": "Default timezone",
        "value_type": SettingValueType.STRING,
        "value": "Asia/Colombo",
        "is_public": True,
        "is_required": True,
        "sort_order": 70,
    },
    {
        "group": "general",
        "key": "default-currency",
        "label": "Default currency",
        "value_type": SettingValueType.STRING,
        "value": "LKR",
        "is_public": True,
        "is_required": True,
        "sort_order": 80,
    },
    {
        "group": "contact",
        "key": "primary-email",
        "label": "Primary email",
        "value_type": SettingValueType.EMAIL,
        "value": "info@lkprofessionals.com",
        "is_public": True,
        "is_required": True,
        "sort_order": 10,
    },
    {
        "group": "contact",
        "key": "sales-email",
        "label": "Sales email",
        "value_type": SettingValueType.EMAIL,
        "value": "sales@lkprofessionals.com",
        "is_public": True,
        "sort_order": 20,
    },
    {
        "group": "contact",
        "key": "hr-email",
        "label": "HR email",
        "value_type": SettingValueType.EMAIL,
        "value": "hr@lkprofessionals.com",
        "is_public": True,
        "sort_order": 30,
    },
    {
        "group": "contact",
        "key": "primary-phone",
        "label": "Primary phone",
        "value_type": SettingValueType.STRING,
        "value": "+94761234321",
        "is_public": True,
        "is_required": True,
        "sort_order": 40,
    },
    {
        "group": "contact",
        "key": "whatsapp-number",
        "label": "WhatsApp number",
        "value_type": SettingValueType.STRING,
        "value": "+94761234321",
        "is_public": True,
        "sort_order": 50,
    },
    {
        "group": "contact",
        "key": "office-city",
        "label": "Office city",
        "value_type": SettingValueType.STRING,
        "value": "Jaffna",
        "is_public": True,
        "sort_order": 60,
    },
    {
        "group": "contact",
        "key": "office-country",
        "label": "Office country",
        "value_type": SettingValueType.STRING,
        "value": "Sri Lanka",
        "is_public": True,
        "sort_order": 70,
    },
    {
        "group": "branding",
        "key": "primary-color",
        "label": "Primary brand color",
        "value_type": SettingValueType.COLOR,
        "value": "#000000",
        "is_public": True,
        "sort_order": 10,
    },
    {
        "group": "branding",
        "key": "secondary-color",
        "label": "Secondary brand color",
        "value_type": SettingValueType.COLOR,
        "value": "#FFFFFF",
        "is_public": True,
        "sort_order": 20,
    },
    {
        "group": "branding",
        "key": "logo",
        "label": "Primary logo",
        "value_type": SettingValueType.MEDIA,
        "is_public": True,
        "sort_order": 30,
    },
    {
        "group": "branding",
        "key": "favicon",
        "label": "Favicon",
        "value_type": SettingValueType.MEDIA,
        "is_public": True,
        "sort_order": 40,
    },
    {
        "group": "social-media",
        "key": "facebook-url",
        "label": "Facebook URL",
        "value_type": SettingValueType.URL,
        "value": "",
        "is_public": True,
        "sort_order": 10,
    },
    {
        "group": "social-media",
        "key": "instagram-url",
        "label": "Instagram URL",
        "value_type": SettingValueType.URL,
        "value": "",
        "is_public": True,
        "sort_order": 20,
    },
    {
        "group": "social-media",
        "key": "linkedin-url",
        "label": "LinkedIn URL",
        "value_type": SettingValueType.URL,
        "value": "",
        "is_public": True,
        "sort_order": 30,
    },
    {
        "group": "social-media",
        "key": "tiktok-url",
        "label": "TikTok URL",
        "value_type": SettingValueType.URL,
        "value": "",
        "is_public": True,
        "sort_order": 40,
    },
    {
        "group": "social-media",
        "key": "youtube-url",
        "label": "YouTube URL",
        "value_type": SettingValueType.URL,
        "value": "",
        "is_public": True,
        "sort_order": 50,
    },
    {
        "group": "seo",
        "key": "default-meta-title",
        "label": "Default meta title",
        "value_type": SettingValueType.STRING,
        "value": (
            "LKProfessionals | Reliable IT Solutions"
        ),
        "is_public": True,
        "validation_rules": {
            "max_length": 70,
        },
        "sort_order": 10,
    },
    {
        "group": "seo",
        "key": "default-meta-description",
        "label": "Default meta description",
        "value_type": SettingValueType.TEXT,
        "value": (
            "LKProfessionals provides web development, "
            "custom software, mobile applications, SEO, "
            "digital marketing, hosting, and IT consulting."
        ),
        "is_public": True,
        "validation_rules": {
            "max_length": 180,
        },
        "sort_order": 20,
    },
    {
        "group": "seo",
        "key": "default-og-image",
        "label": "Default Open Graph image",
        "value_type": SettingValueType.MEDIA,
        "is_public": True,
        "sort_order": 30,
    },
    {
        "group": "seo",
        "key": "robots-index-enabled",
        "label": "Search engine indexing enabled",
        "value_type": SettingValueType.BOOLEAN,
        "value": "true",
        "is_public": True,
        "sort_order": 40,
    },
    {
        "group": "analytics",
        "key": "google-tag-manager-id",
        "label": "Google Tag Manager ID",
        "value_type": SettingValueType.STRING,
        "value": "",
        "is_public": True,
        "sort_order": 10,
    },
    {
        "group": "analytics",
        "key": "google-analytics-id",
        "label": "Google Analytics ID",
        "value_type": SettingValueType.STRING,
        "value": "",
        "is_public": True,
        "sort_order": 20,
    },
    {
        "group": "analytics",
        "key": "meta-pixel-id",
        "label": "Meta Pixel ID",
        "value_type": SettingValueType.STRING,
        "value": "",
        "is_public": True,
        "sort_order": 30,
    },
    {
        "group": "operations",
        "key": "maintenance-mode",
        "label": "Maintenance mode",
        "value_type": SettingValueType.BOOLEAN,
        "value": "false",
        "is_public": True,
        "sort_order": 10,
    },
    {
        "group": "operations",
        "key": "maintenance-message",
        "label": "Maintenance message",
        "value_type": SettingValueType.TEXT,
        "value": (
            "The website is temporarily unavailable "
            "while scheduled maintenance is completed."
        ),
        "is_public": True,
        "sort_order": 20,
    },
    {
        "group": "operations",
        "key": "contact-form-enabled",
        "label": "Contact form enabled",
        "value_type": SettingValueType.BOOLEAN,
        "value": "true",
        "is_public": True,
        "sort_order": 30,
    },
    {
        "group": "operations",
        "key": "quote-form-enabled",
        "label": "Quote form enabled",
        "value_type": SettingValueType.BOOLEAN,
        "value": "true",
        "is_public": True,
        "sort_order": 40,
    },
    {
        "group": "operations",
        "key": "newsletter-enabled",
        "label": "Newsletter enabled",
        "value_type": SettingValueType.BOOLEAN,
        "value": "true",
        "is_public": True,
        "sort_order": 50,
    },
    {
        "group": "operations",
        "key": "careers-enabled",
        "label": "Careers enabled",
        "value_type": SettingValueType.BOOLEAN,
        "value": "true",
        "is_public": True,
        "sort_order": 60,
    },
]


class Command(BaseCommand):
    help = (
        "Seed deterministic default global website "
        "settings for LKProfessionals."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        groups_created = 0
        groups_updated = 0
        settings_created = 0
        settings_updated = 0

        groups = {}

        for item in GROUPS:
            defaults = {
                "name": item["name"],
                "description": item["description"],
                "icon": item["icon"],
                "is_active": True,
                "sort_order": item["sort_order"],
            }

            group, created = (
                WebsiteSettingGroup.all_objects
                .update_or_create(
                    slug=item["slug"],
                    defaults={
                        **defaults,
                        "is_deleted": False,
                        "deleted_at": None,
                    },
                )
            )

            groups[item["slug"]] = group

            if created:
                groups_created += 1
            else:
                groups_updated += 1

        for item in SETTINGS:
            group_slug = item["group"]
            group = groups[group_slug]

            defaults = {
                "group": group,
                "label": item["label"],
                "description": item.get(
                    "description",
                    "",
                ),
                "value_type": item["value_type"],
                "value": item.get("value", ""),
                "json_value": item.get(
                    "json_value",
                    {},
                ),
                "default_value": item.get(
                    "default_value",
                    "",
                ),
                "validation_rules": item.get(
                    "validation_rules",
                    {},
                ),
                "is_public": item.get(
                    "is_public",
                    False,
                ),
                "is_editable": item.get(
                    "is_editable",
                    True,
                ),
                "is_required": item.get(
                    "is_required",
                    False,
                ),
                "is_active": True,
                "sort_order": item["sort_order"],
                "is_deleted": False,
                "deleted_at": None,
            }

            setting, created = (
                WebsiteSetting.all_objects
                .update_or_create(
                    key=item["key"],
                    environment=(
                        SettingEnvironment.GLOBAL
                    ),
                    defaults=defaults,
                )
            )

            setting.full_clean()
            setting.save()

            if created:
                settings_created += 1
            else:
                settings_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Website settings seeding completed: "
                f"{groups_created} groups created, "
                f"{groups_updated} groups updated; "
                f"{settings_created} settings created, "
                f"{settings_updated} settings updated."
            )
        )
