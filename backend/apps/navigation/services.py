from django.db import transaction

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    NavigationMenu,
    NavigationMenuItem,
)


class NavigationService:
    @staticmethod
    def menu_snapshot(menu):
        return {
            "id": str(menu.id),
            "name": menu.name,
            "slug": menu.slug,
            "location": menu.location,
            "is_active": menu.is_active,
            "is_public": menu.is_public,
            "sort_order": menu.sort_order,
        }

    @staticmethod
    def item_snapshot(item):
        return {
            "id": str(item.id),
            "menu_id": str(item.menu_id),
            "parent_id": (
                str(item.parent_id)
                if item.parent_id
                else None
            ),
            "label": item.label,
            "link_type": item.link_type,
            "url": item.url,
            "visibility": item.visibility,
            "is_active": item.is_active,
            "is_featured": item.is_featured,
            "sort_order": item.sort_order,
        }

    @classmethod
    @transaction.atomic
    def create_menu(
        cls,
        *,
        request,
        values,
    ):
        menu = NavigationMenu.objects.create(
            **values,
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="navigation",
            message="Navigation menu created.",
            target_type="navigation.NavigationMenu",
            target_id=str(menu.pk),
            metadata={
                "after": cls.menu_snapshot(menu),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="create_menu",
            module="navigation",
            description=(
                f"Created navigation menu {menu.name}."
            ),
            entity_type="navigation.NavigationMenu",
            entity_id=str(menu.pk),
        )

        return menu

    @classmethod
    @transaction.atomic
    def update_menu(
        cls,
        *,
        request,
        menu,
        values,
    ):
        before = cls.menu_snapshot(menu)

        for field, value in values.items():
            setattr(menu, field, value)

        menu.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="navigation",
            message="Navigation menu updated.",
            target_type="navigation.NavigationMenu",
            target_id=str(menu.pk),
            metadata={
                "before": before,
                "after": cls.menu_snapshot(menu),
            },
        )

        return menu

    @classmethod
    @transaction.atomic
    def create_item(
        cls,
        *,
        request,
        values,
    ):
        item = NavigationMenuItem(**values)
        item.full_clean()
        item.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="navigation",
            message="Navigation menu item created.",
            target_type="navigation.NavigationMenuItem",
            target_id=str(item.pk),
            metadata={
                "after": cls.item_snapshot(item),
            },
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="create_menu_item",
            module="navigation",
            description=(
                f"Created navigation item {item.label}."
            ),
            entity_type="navigation.NavigationMenuItem",
            entity_id=str(item.pk),
        )

        return item

    @classmethod
    @transaction.atomic
    def update_item(
        cls,
        *,
        request,
        item,
        values,
    ):
        before = cls.item_snapshot(item)

        for field, value in values.items():
            setattr(item, field, value)

        item.full_clean()
        item.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="navigation",
            message="Navigation menu item updated.",
            target_type="navigation.NavigationMenuItem",
            target_id=str(item.pk),
            metadata={
                "before": before,
                "after": cls.item_snapshot(item),
            },
        )

        return item

    @classmethod
    @transaction.atomic
    def reorder_items(
        cls,
        *,
        request,
        menu,
        items,
    ):
        item_ids = [
            item["id"]
            for item in items
        ]

        existing = {
            str(item.id): item
            for item in (
                NavigationMenuItem.objects.filter(
                    menu=menu,
                    id__in=item_ids,
                )
            )
        }

        if len(existing) != len(set(item_ids)):
            raise ValueError(
                "One or more navigation items are invalid."
            )

        for item_data in items:
            item = existing[str(item_data["id"])]

            parent_id = item_data.get("parent_id")

            if parent_id:
                parent = existing.get(str(parent_id))

                if parent is None:
                    parent = (
                        NavigationMenuItem.objects.filter(
                            menu=menu,
                            pk=parent_id,
                        ).first()
                    )

                if parent is None:
                    raise ValueError(
                        "Navigation parent item is invalid."
                    )

                item.parent = parent
            else:
                item.parent = None

            item.sort_order = item_data["sort_order"]
            item.full_clean()

        NavigationMenuItem.objects.bulk_update(
            list(existing.values()),
            fields=[
                "parent",
                "sort_order",
            ],
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="reorder_menu_items",
            module="navigation",
            description=(
                f"Reordered items for menu {menu.name}."
            ),
            entity_type="navigation.NavigationMenu",
            entity_id=str(menu.pk),
        )

        return menu



class PublicNavigationService:
    @staticmethod
    def build_tree(items):
        item_map = {
            item.id: item
            for item in items
        }

        children_map = {}

        for item in items:
            parent_id = item.parent_id

            if (
                parent_id is not None
                and parent_id not in item_map
            ):
                continue

            children_map.setdefault(
                parent_id,
                [],
            ).append(item)

        def serialize(item, ancestry):
            if item.id in ancestry:
                return None

            next_ancestry = {
                *ancestry,
                item.id,
            }

            children = []

            for child in children_map.get(
                item.id,
                [],
            ):
                serialized = serialize(
                    child,
                    next_ancestry,
                )

                if serialized is not None:
                    children.append(serialized)

            return {
                "id": item.id,
                "parent_id": item.parent_id,
                "label": item.label,
                "link_type": item.link_type,
                "url": item.resolved_url,
                "icon": item.icon,
                "css_class": item.css_class,
                "target_blank": item.target_blank,
                "rel_attribute": item.rel_attribute,
                "is_featured": item.is_featured,
                "sort_order": item.sort_order,
                "metadata": item.metadata,
                "children": children,
            }

        roots = []

        for item in children_map.get(None, []):
            serialized = serialize(item, set())

            if serialized is not None:
                roots.append(serialized)

        return roots
