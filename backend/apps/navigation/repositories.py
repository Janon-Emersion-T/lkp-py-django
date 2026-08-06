from django.db.models import Q

from .models import (
    NavigationMenu,
    NavigationMenuItem,
)


class NavigationMenuRepository:
    ALLOWED_ORDERING_FIELDS = {
        "name",
        "location",
        "sort_order",
        "created_at",
        "updated_at",
    }

    @staticmethod
    def queryset():
        return NavigationMenu.objects.prefetch_related(
            "items",
            "items__parent",
            "items__cms_page",
            "items__service",
            "items__package",
            "items__industry",
            "items__insight",
            "items__case_study",
        )

    @classmethod
    def find_by_id(cls, menu_id):
        return cls.queryset().filter(
            pk=menu_id,
        ).first()

    @classmethod
    def find_by_slug(cls, slug):
        return cls.queryset().filter(
            slug=slug,
        ).first()

    @classmethod
    def search(
        cls,
        *,
        search=None,
        location=None,
        is_active=None,
        is_public=None,
        ordering=None,
    ):
        queryset = cls.queryset()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(slug__icontains=search)
                | Q(description__icontains=search)
            )

        if location:
            queryset = queryset.filter(
                location=location,
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        if is_public is not None:
            queryset = queryset.filter(
                is_public=is_public,
            )

        if ordering:
            descending = ordering.startswith("-")
            field = ordering.lstrip("-")

            if field in cls.ALLOWED_ORDERING_FIELDS:
                queryset = queryset.order_by(
                    f"-{field}" if descending else field
                )

        return queryset


class NavigationMenuItemRepository:
    @staticmethod
    def queryset():
        return NavigationMenuItem.objects.select_related(
            "menu",
            "parent",
            "cms_page",
            "service",
            "package",
            "industry",
            "insight",
            "case_study",
        ).prefetch_related(
            "children",
        )

    @classmethod
    def find_by_id(cls, item_id):
        return cls.queryset().filter(
            pk=item_id,
        ).first()

    @classmethod
    def for_menu(
        cls,
        menu_id,
        *,
        parent_id=None,
        is_active=None,
    ):
        queryset = cls.queryset().filter(
            menu_id=menu_id,
        )

        if parent_id == "root":
            queryset = queryset.filter(
                parent__isnull=True,
            )
        elif parent_id:
            queryset = queryset.filter(
                parent_id=parent_id,
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active,
            )

        return queryset

    @classmethod
    def public_items(cls, menu_id):
        return cls.queryset().filter(
            menu_id=menu_id,
            is_active=True,
        )



class PublicNavigationRepository:
    @staticmethod
    def menu_by_slug(slug):
        return NavigationMenu.objects.filter(
            slug=slug,
            is_active=True,
            is_public=True,
        ).first()

    @staticmethod
    def menus_by_location(location):
        return NavigationMenu.objects.filter(
            location=location,
            is_active=True,
            is_public=True,
        ).order_by(
            "sort_order",
            "name",
        )

    @staticmethod
    def items_for_menu(menu_id):
        return NavigationMenuItem.objects.select_related(
            "menu",
            "parent",
            "cms_page",
            "service",
            "package",
            "industry",
            "insight",
            "case_study",
        ).filter(
            menu_id=menu_id,
            is_active=True,
            visibility="everyone",
        ).order_by(
            "sort_order",
            "label",
        )
