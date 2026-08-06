from django.db.models import Q

from .models import (
    SettingEnvironment,
    WebsiteSetting,
    WebsiteSettingGroup,
)


class WebsiteSettingGroupRepository:
    @staticmethod
    def queryset():
        return WebsiteSettingGroup.objects.prefetch_related(
            "settings",
            "settings__media_asset",
        )

    @classmethod
    def find_by_id(cls, group_id):
        return cls.queryset().filter(
            pk=group_id,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        is_active=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(slug__icontains=search)
                | Q(description__icontains=search)
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        return queryset


class WebsiteSettingRepository:
    ALLOWED_ORDERING_FIELDS = {
        "key",
        "label",
        "value_type",
        "environment",
        "sort_order",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return WebsiteSetting.objects.select_related(
            "group",
            "media_asset",
        )

    @classmethod
    def find_by_id(cls, setting_id):
        return cls.queryset().filter(
            pk=setting_id,
        ).first()

    @classmethod
    def find_by_key(
        cls,
        key,
        *,
        environment=SettingEnvironment.GLOBAL,
    ):
        return cls.queryset().filter(
            key=key,
            environment=environment,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        group_id=None,
        value_type=None,
        environment=None,
        is_public=None,
        is_editable=None,
        is_active=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(key__icontains=search)
                | Q(label__icontains=search)
                | Q(description__icontains=search)
                | Q(value__icontains=search)
            )

        if group_id:
            queryset = queryset.filter(
                group_id=group_id,
            )

        if value_type:
            queryset = queryset.filter(
                value_type=value_type,
            )

        if environment:
            queryset = queryset.filter(
                environment=environment,
            )

        if is_public is not None:
            queryset = queryset.filter(
                is_public=is_public,
            )

        if is_editable is not None:
            queryset = queryset.filter(
                is_editable=is_editable,
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset


class PublicWebsiteSettingRepository:
    @classmethod
    def values_for_environment(cls, environment):
        settings = WebsiteSetting.objects.select_related(
            "media_asset",
        ).filter(
            is_active=True,
            is_public=True,
            environment__in=[
                SettingEnvironment.GLOBAL,
                environment,
            ],
        ).order_by(
            "key",
            "environment",
        )

        resolved = {}

        for setting in settings:
            current = resolved.get(setting.key)

            if (
                current is None
                or setting.environment == environment
            ):
                resolved[setting.key] = setting

        return resolved
