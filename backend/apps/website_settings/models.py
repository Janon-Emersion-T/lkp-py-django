from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.core.validators import (
    EmailValidator,
    URLValidator,
)
from django.db import models

from apps.common.models import BaseModel


class SettingValueType(models.TextChoices):
    STRING = "string", "String"
    TEXT = "text", "Text"
    INTEGER = "integer", "Integer"
    DECIMAL = "decimal", "Decimal"
    BOOLEAN = "boolean", "Boolean"
    JSON = "json", "JSON"
    EMAIL = "email", "Email"
    URL = "url", "URL"
    COLOR = "color", "Color"
    MEDIA = "media", "Media asset"


class SettingEnvironment(models.TextChoices):
    GLOBAL = "global", "Global"
    DEVELOPMENT = "development", "Development"
    STAGING = "staging", "Staging"
    PRODUCTION = "production", "Production"


class WebsiteSettingGroup(BaseModel):
    name = models.CharField(
        max_length=150,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=170,
        unique=True,
        db_index=True,
    )

    description = models.TextField(blank=True)

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "name",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("name",),
                condition=models.Q(is_deleted=False),
                name="unique_active_website_setting_group_name",
            ),
        ]
        indexes = [
            models.Index(
                fields=("is_active", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.name


class WebsiteSetting(BaseModel):
    group = models.ForeignKey(
        WebsiteSettingGroup,
        on_delete=models.PROTECT,
        related_name="settings",
    )

    key = models.SlugField(
        max_length=200,
        db_index=True,
    )

    label = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    value_type = models.CharField(
        max_length=30,
        choices=SettingValueType.choices,
        default=SettingValueType.STRING,
        db_index=True,
    )

    environment = models.CharField(
        max_length=30,
        choices=SettingEnvironment.choices,
        default=SettingEnvironment.GLOBAL,
        db_index=True,
    )

    value = models.TextField(blank=True)

    json_value = models.JSONField(
        default=dict,
        blank=True,
    )

    media_asset = models.ForeignKey(
        "media_library.MediaAsset",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="website_setting_usages",
    )

    default_value = models.TextField(blank=True)

    validation_rules = models.JSONField(
        default=dict,
        blank=True,
    )

    is_public = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_editable = models.BooleanField(
        default=True,
        db_index=True,
    )

    is_required = models.BooleanField(default=False)

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "group__sort_order",
            "sort_order",
            "key",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("key", "environment"),
                condition=models.Q(is_deleted=False),
                name="unique_active_website_setting_key_environment",
            ),
        ]
        indexes = [
            models.Index(
                fields=("group", "is_active"),
            ),
            models.Index(
                fields=("environment", "is_active"),
            ),
            models.Index(
                fields=("is_public", "is_active"),
            ),
            models.Index(
                fields=("value_type", "is_active"),
            ),
        ]

    def __str__(self):
        return f"{self.key} ({self.environment})"

    @property
    def typed_value(self):
        if self.value_type == SettingValueType.JSON:
            return self.json_value

        if self.value_type == SettingValueType.MEDIA:
            return self.media_asset_id

        raw = self.value

        if raw == "":
            raw = self.default_value

        if self.value_type in {
            SettingValueType.STRING,
            SettingValueType.TEXT,
            SettingValueType.EMAIL,
            SettingValueType.URL,
            SettingValueType.COLOR,
        }:
            return raw

        if self.value_type == SettingValueType.INTEGER:
            return int(raw) if raw != "" else None

        if self.value_type == SettingValueType.DECIMAL:
            return Decimal(raw) if raw != "" else None

        if self.value_type == SettingValueType.BOOLEAN:
            return str(raw).strip().lower() in {
                "1",
                "true",
                "yes",
                "on",
            }

        return raw

    def clean(self):
        super().clean()

        errors = {}

        if self.is_required:
            has_value = bool(
                self.value
                or self.default_value
                or self.json_value
                or self.media_asset_id
            )

            if not has_value:
                errors["value"] = (
                    "A value is required for this setting."
                )

        if self.value_type == SettingValueType.MEDIA:
            if (
                self.is_required
                and not self.media_asset_id
            ):
                errors["media_asset"] = (
                    "A media asset is required."
                )

        elif self.value_type == SettingValueType.JSON:
            if not isinstance(
                self.json_value,
                (dict, list),
            ):
                errors["json_value"] = (
                    "JSON value must be an object or list."
                )

        else:
            raw = self.value or self.default_value

            if raw:
                try:
                    self._validate_scalar_value(raw)
                except ValidationError as exc:
                    errors["value"] = exc.messages

        if errors:
            raise ValidationError(errors)

    def _validate_scalar_value(self, raw):
        if self.value_type == SettingValueType.INTEGER:
            try:
                int(raw)
            except (TypeError, ValueError) as exc:
                raise ValidationError(
                    "Value must be an integer."
                ) from exc

        elif self.value_type == SettingValueType.DECIMAL:
            try:
                Decimal(raw)
            except (
                TypeError,
                ValueError,
                InvalidOperation,
            ) as exc:
                raise ValidationError(
                    "Value must be a decimal number."
                ) from exc

        elif self.value_type == SettingValueType.BOOLEAN:
            if str(raw).strip().lower() not in {
                "1",
                "0",
                "true",
                "false",
                "yes",
                "no",
                "on",
                "off",
            }:
                raise ValidationError(
                    "Value must be a valid boolean."
                )

        elif self.value_type == SettingValueType.EMAIL:
            EmailValidator()(raw)

        elif self.value_type == SettingValueType.URL:
            URLValidator()(raw)

        elif self.value_type == SettingValueType.COLOR:
            normalized = str(raw).strip()

            if not (
                len(normalized) in {4, 7, 9}
                and normalized.startswith("#")
                and all(
                    character in "0123456789abcdefABCDEF"
                    for character in normalized[1:]
                )
            ):
                raise ValidationError(
                    "Value must be a valid hexadecimal color."
                )

        minimum_length = self.validation_rules.get(
            "min_length"
        )

        maximum_length = self.validation_rules.get(
            "max_length"
        )

        if (
            minimum_length is not None
            and len(str(raw)) < int(minimum_length)
        ):
            raise ValidationError(
                f"Value must contain at least "
                f"{minimum_length} characters."
            )

        if (
            maximum_length is not None
            and len(str(raw)) > int(maximum_length)
        ):
            raise ValidationError(
                f"Value must contain no more than "
                f"{maximum_length} characters."
            )
