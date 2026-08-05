from typing import Generic, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import QuerySet


ModelType = TypeVar(
    "ModelType",
    bound=models.Model,
)


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    @classmethod
    def queryset(cls) -> QuerySet[ModelType]:
        return cls.model.objects.all()

    @classmethod
    def all(cls) -> QuerySet[ModelType]:
        return cls.queryset()

    @classmethod
    def get_by_id(cls, object_id) -> ModelType:
        return cls.queryset().get(pk=object_id)

    @classmethod
    def find_by_id(
        cls,
        object_id,
    ) -> ModelType | None:
        try:
            return cls.get_by_id(object_id)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def exists(cls, **filters) -> bool:
        return cls.queryset().filter(**filters).exists()

    @classmethod
    def filter(cls, **filters) -> QuerySet[ModelType]:
        return cls.queryset().filter(**filters)

    @classmethod
    def create(cls, **values) -> ModelType:
        return cls.model.objects.create(**values)
