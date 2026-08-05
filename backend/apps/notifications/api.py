from django.shortcuts import get_object_or_404
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import MessageSchema

from .models import Notification
from .schemas import NotificationSchema
from .services import NotificationService


router = Router(
    tags=["Notifications"],
    auth=jwt_auth,
)


@router.get(
    "",
    response=list[NotificationSchema],
)
def list_notifications(request, unread_only: bool = False):
    queryset = Notification.objects.filter(
        recipient=request.auth,
    )

    if unread_only:
        queryset = queryset.filter(is_read=False)

    return queryset.order_by("-created_at")


@router.post(
    "/{notification_id}/read",
    response=NotificationSchema,
)
def mark_notification_read(request, notification_id: str):
    notification = get_object_or_404(
        Notification,
        pk=notification_id,
        recipient=request.auth,
    )

    return NotificationService.mark_as_read(
        notification=notification,
    )


@router.post(
    "/read-all",
    response=MessageSchema,
)
def mark_all_notifications_read(request):
    updated = NotificationService.mark_all_as_read(
        user=request.auth,
    )

    return {
        "status": "ok",
        "message": f"{updated} notifications marked as read.",
    }
