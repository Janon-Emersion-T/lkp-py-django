from django.db.models import QuerySet

from .models import SystemSetting


class SystemSettingRepository:
    @staticmethod
    def list_settings(
        *,
        group: str | None = None,
    ) -> QuerySet[SystemSetting]:
        queryset = SystemSetting.objects.all()

        if group:
            queryset = queryset.filter(group=group)

        return queryset.order_by("group", "key")

    @staticmethod
    def get_setting(
        *,
        group: str,
        key: str,
    ) -> SystemSetting | None:
        return SystemSetting.objects.filter(
            group=group,
            key=key,
        ).first()
