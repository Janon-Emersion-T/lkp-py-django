from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.rbac.constants import DEFAULT_ROLES
from apps.rbac.models import Role


class Command(BaseCommand):
    help = "Create or update LKProfessionals default system roles."

    @transaction.atomic
    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for role_data in DEFAULT_ROLES:
            slug = role_data["slug"]

            role = Role.all_objects.filter(slug=slug).first()

            defaults = {
                "name": role_data["name"],
                "description": role_data["description"],
                "priority": role_data["priority"],
                "is_system": True,
                "is_active": True,
                "is_deleted": False,
                "deleted_at": None,
            }

            if role is None:
                role = Role.objects.create(
                    slug=slug,
                    **defaults,
                )
                created_count += 1
            else:
                changed = False

                for field, value in defaults.items():
                    if getattr(role, field) != value:
                        setattr(role, field, value)
                        changed = True

                if changed:
                    role.save()
                    updated_count += 1

            if slug == "super-admin":
                role.permissions.set(Permission.objects.all())

        self.stdout.write(
            self.style.SUCCESS(
                f"Role seeding completed: "
                f"{created_count} created, "
                f"{updated_count} updated."
            )
        )
