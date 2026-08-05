from django.db import transaction
from django.utils import timezone

from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event
from apps.rbac.models import Role, UserRole

from .models import User
from .repositories import UserRepository


class UserService:
    @staticmethod
    @transaction.atomic
    def create_user(
        *,
        request,
        email: str,
        username: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        phone: str = "",
        job_title: str = "",
        department: str = "",
        role_ids: list[str] | None = None,
        is_active: bool = True,
        is_staff: bool = False,
    ) -> User:
        normalized_email = email.strip().lower()

        if UserRepository.get_by_email(normalized_email):
            raise ValueError("A user with this email already exists.")

        user = User.objects.create_user(
            email=normalized_email,
            username=username.strip(),
            password=password,
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            phone=phone.strip(),
            job_title=job_title.strip(),
            department=department.strip(),
            is_active=is_active,
            is_staff=is_staff,
            must_change_password=True,
        )

        if role_ids:
            roles = Role.objects.filter(
                id__in=role_ids,
                is_active=True,
            )

            for role in roles:
                UserRole.objects.create(
                    user=user,
                    role=role,
                    assigned_by=request.auth,
                    created_by=request.auth,
                )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="users",
            message="User account created.",
            target_type="accounts.User",
            target_id=str(user.pk),
            after={
                "email": user.email,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
            },
        )

        return user

    @staticmethod
    @transaction.atomic
    def update_user(
        *,
        request,
        user: User,
        first_name: str,
        last_name: str,
        phone: str,
        job_title: str,
        department: str,
        timezone_name: str,
        preferred_language: str,
        is_active: bool,
        is_staff: bool,
    ) -> User:
        before = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "job_title": user.job_title,
            "department": user.department,
            "timezone": user.timezone,
            "preferred_language": user.preferred_language,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
        }

        user.first_name = first_name.strip()
        user.last_name = last_name.strip()
        user.phone = phone.strip()
        user.job_title = job_title.strip()
        user.department = department.strip()
        user.timezone = timezone_name
        user.preferred_language = preferred_language
        user.is_active = is_active
        user.is_staff = is_staff

        user.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="users",
            message="User account updated.",
            target_type="accounts.User",
            target_id=str(user.pk),
            before=before,
            after={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "job_title": user.job_title,
                "department": user.department,
                "timezone": user.timezone,
                "preferred_language": user.preferred_language,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
            },
        )

        return user

    @staticmethod
    @transaction.atomic
    def soft_delete_user(
        *,
        request,
        user: User,
    ) -> None:
        if user.pk == request.auth.pk:
            raise ValueError("You cannot delete your own account.")

        user.is_deleted = True
        user.deleted_at = timezone.now()
        user.is_active = False

        user.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
                "is_active",
            ],
        )

        UserRole.objects.filter(
            user=user,
            is_active=True,
        ).update(is_active=False)

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="users",
            message="User account soft deleted.",
            target_type="accounts.User",
            target_id=str(user.pk),
            before={
                "email": user.email,
                "is_active": True,
            },
            after={
                "email": user.email,
                "is_active": False,
                "is_deleted": True,
            },
        )
