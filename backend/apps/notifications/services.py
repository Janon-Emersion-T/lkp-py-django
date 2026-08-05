from django.utils import timezone

from .models import (
    Notification,
    NotificationChannel,
    NotificationType,
)


class NotificationService:
    @staticmethod
    def create(
        *,
        recipient,
        title: str,
        message: str,
        notification_type: str = NotificationType.INFO,
        channel: str = NotificationChannel.DASHBOARD,
        action_url: str = "",
        metadata: dict | None = None,
        created_by=None,
    ) -> Notification:
        return Notification.objects.create(
            recipient=recipient,
            title=title,
            message=message,
            notification_type=notification_type,
            channel=channel,
            action_url=action_url,
            metadata=metadata or {},
            created_by=created_by,
        )

    @staticmethod
    def mark_as_read(
        *,
        notification: Notification,
    ) -> Notification:
        if notification.is_read:
            return notification

        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save(
            update_fields=[
                "is_read",
                "read_at",
                "updated_at",
            ],
        )

        return notification

    @staticmethod
    def mark_all_as_read(*, user) -> int:
        return Notification.objects.filter(
            recipient=user,
            is_read=False,
        ).update(
            is_read=True,
            read_at=timezone.now(),
        )
