from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.common.request_context import get_client_ip

from .exceptions import ApiHttpError
from .models import RateLimitBucket


def enforce_rate_limit(
    request,
    *,
    scope: str,
    limit: int,
    window_seconds: int,
):
    client_ip = get_client_ip(request) or "unknown"
    key = f"{scope}:{client_ip}"
    now = timezone.now()
    window = timedelta(seconds=window_seconds)

    with transaction.atomic():
        bucket, _ = RateLimitBucket.objects.select_for_update().get_or_create(
            key=key,
            defaults={
                "count": 0,
                "window_started_at": now,
            },
        )

        if now - bucket.window_started_at >= window:
            bucket.count = 0
            bucket.window_started_at = now

        if bucket.count >= limit:
            retry_after = max(
                1,
                int(
                    window_seconds
                    - (now - bucket.window_started_at).total_seconds()
                ),
            )

            raise ApiHttpError(
                429,
                "Too many requests.",
                code="rate_limit_exceeded",
                details={
                    "retry_after_seconds": retry_after,
                },
            )

        bucket.count += 1
        bucket.save(
            update_fields=[
                "count",
                "window_started_at",
            ],
        )
