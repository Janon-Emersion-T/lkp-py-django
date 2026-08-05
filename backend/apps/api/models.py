from django.db import models


class RateLimitBucket(models.Model):
    key = models.CharField(
        max_length=255,
        unique=True,
    )
    count = models.PositiveIntegerField(default=0)
    window_started_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=("key", "window_started_at")),
        ]

    def __str__(self):
        return self.key
