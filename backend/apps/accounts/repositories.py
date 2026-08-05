from django.db.models import QuerySet

from .models import User


class UserRepository:
    @staticmethod
    def list_active() -> QuerySet[User]:
        return User.objects.filter(
            is_deleted=False,
        ).order_by("email")

    @staticmethod
    def get_by_id(user_id: int) -> User:
        return User.objects.get(
            pk=user_id,
            is_deleted=False,
        )

    @staticmethod
    def get_by_email(email: str) -> User | None:
        return User.objects.filter(
            email__iexact=email,
            is_deleted=False,
        ).first()
