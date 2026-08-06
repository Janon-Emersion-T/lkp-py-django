from django.apps import AppConfig


class PublicWebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.public_website"
    verbose_name = "Public Website API"
