from django.db import models

from apps.common.models import BaseModel


class SettingDataType(models.TextChoices):
    STRING = "string", "String"
    INTEGER = "integer", "Integer"
    BOOLEAN = "boolean", "Boolean"
    DECIMAL = "decimal", "Decimal"
    JSON = "json", "JSON"
    SECRET = "secret", "Secret"


class SystemSetting(BaseModel):
    group = models.CharField(
        max_length=100,
        db_index=True,
    )
    key = models.CharField(
        max_length=150,
    )
    value = models.JSONField(
        null=True,
        blank=True,
    )
    data_type = models.CharField(
        max_length=20,
        choices=SettingDataType.choices,
        default=SettingDataType.STRING,
    )
    description = models.TextField(blank=True)

    is_public = models.BooleanField(default=False)
    is_editable = models.BooleanField(default=True)
    is_required = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("group", "key"),
                condition=models.Q(is_deleted=False),
                name="unique_active_system_setting",
            ),
        ]
        indexes = [
            models.Index(fields=("group", "key")),
        ]

    def __str__(self):
        return f"{self.group}.{self.key}"
