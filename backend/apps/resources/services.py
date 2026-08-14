from django.utils import timezone

from .models import ResourceStatus
from .repositories import ResourceRepository


class ResourceService:
    @staticmethod
    def create_resource(*, values):
        return ResourceRepository.create(
            **values,
        )

    @staticmethod
    def update_resource(
        *,
        resource,
        values,
    ):
        clean_values = {
            key: value
            for key, value in values.items()
            if value is not None
        }

        return ResourceRepository.update(
            resource,
            **clean_values,
        )

    @staticmethod
    def publish_resource(*, resource):
        resource.status = ResourceStatus.PUBLISHED

        if resource.published_at is None:
            resource.published_at = timezone.now()

        resource.scheduled_for = None

        resource.save(
            update_fields=[
                "status",
                "published_at",
                "scheduled_for",
                "updated_at",
            ],
        )

        return resource

    @staticmethod
    def schedule_resource(
        *,
        resource,
        scheduled_for,
    ):
        if scheduled_for <= timezone.now():
            raise ValueError(
                "Scheduled publication must be in the future."
            )

        resource.status = ResourceStatus.SCHEDULED
        resource.scheduled_for = scheduled_for

        resource.save(
            update_fields=[
                "status",
                "scheduled_for",
                "updated_at",
            ],
        )

        return resource

    @staticmethod
    def increment_download(resource):
        resource.download_count += 1

        resource.save(
            update_fields=[
                "download_count",
                "updated_at",
            ],
        )

        return resource
