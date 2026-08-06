from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.accounts.models import User

from .models import (
    MenuItemLinkType,
    NavigationLocation,
    NavigationMenu,
    NavigationMenuItem,
)
from .repositories import (
    NavigationMenuItemRepository,
    NavigationMenuRepository,
)
from .services import NavigationService


class RequestStub:
    def __init__(self, user):
        self.auth = user
        self.user = user
        self.META = {}
        self.headers = {}


class NavigationModelTests(TestCase):
    def setUp(self):
        self.menu = NavigationMenu.objects.create(
            name="Main Navigation",
            slug="main-navigation",
            location=(
                NavigationLocation.HEADER_PRIMARY
            ),
        )

    def test_menu_string(self):
        self.assertEqual(
            str(self.menu),
            "Main Navigation",
        )

    def test_internal_item_requires_url(self):
        item = NavigationMenuItem(
            menu=self.menu,
            label="Home",
            link_type=MenuItemLinkType.INTERNAL,
        )

        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_contact_item_resolves_url(self):
        item = NavigationMenuItem.objects.create(
            menu=self.menu,
            label="Contact",
            link_type=MenuItemLinkType.CONTACT,
        )

        self.assertEqual(
            item.resolved_url,
            "/contact",
        )

    def test_child_depth(self):
        parent = NavigationMenuItem.objects.create(
            menu=self.menu,
            label="Services",
            link_type=MenuItemLinkType.INTERNAL,
            url="/services",
        )

        child = NavigationMenuItem.objects.create(
            menu=self.menu,
            parent=parent,
            label="Web Development",
            link_type=MenuItemLinkType.INTERNAL,
            url="/services/web-development",
        )

        self.assertEqual(child.depth, 1)

    def test_parent_must_use_same_menu(self):
        second_menu = NavigationMenu.objects.create(
            name="Footer",
            slug="footer",
        )

        parent = NavigationMenuItem.objects.create(
            menu=second_menu,
            label="About",
            link_type=MenuItemLinkType.INTERNAL,
            url="/about",
        )

        item = NavigationMenuItem(
            menu=self.menu,
            parent=parent,
            label="Invalid",
            link_type=MenuItemLinkType.INTERNAL,
            url="/invalid",
        )

        with self.assertRaises(ValidationError):
            item.full_clean()


class NavigationRepositoryTests(TestCase):
    def setUp(self):
        self.menu = NavigationMenu.objects.create(
            name="Primary Header",
            slug="primary-header",
            location=(
                NavigationLocation.HEADER_PRIMARY
            ),
            is_public=True,
        )

        self.item = NavigationMenuItem.objects.create(
            menu=self.menu,
            label="Home",
            link_type=MenuItemLinkType.INTERNAL,
            url="/",
        )

    def test_search_menu(self):
        queryset = NavigationMenuRepository.search(
            search="Primary",
            location=(
                NavigationLocation.HEADER_PRIMARY
            ),
        )

        self.assertEqual(queryset.count(), 1)

    def test_find_menu_by_slug(self):
        menu = NavigationMenuRepository.find_by_slug(
            "primary-header"
        )

        self.assertEqual(menu.id, self.menu.id)

    def test_filter_items_for_menu(self):
        queryset = (
            NavigationMenuItemRepository.for_menu(
                self.menu.id,
            )
        )

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(
            queryset.first().id,
            self.item.id,
        )


class NavigationServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="navigation_admin",
            email="navigation-admin@example.com",
            password="StrongPassword123!",
        )

        self.request = RequestStub(self.user)

        self.menu = NavigationMenu.objects.create(
            name="Service Menu",
            slug="service-menu",
        )

    def test_create_menu(self):
        menu = NavigationService.create_menu(
            request=self.request,
            values={
                "name": "Footer Menu",
                "slug": "footer-menu",
                "location": (
                    NavigationLocation.FOOTER_PRIMARY
                ),
            },
        )

        self.assertEqual(
            menu.location,
            NavigationLocation.FOOTER_PRIMARY,
        )

    def test_create_item(self):
        item = NavigationService.create_item(
            request=self.request,
            values={
                "menu": self.menu,
                "label": "About",
                "link_type": (
                    MenuItemLinkType.INTERNAL
                ),
                "url": "/about",
            },
        )

        self.assertEqual(
            item.resolved_url,
            "/about",
        )

    def test_update_item(self):
        item = NavigationMenuItem.objects.create(
            menu=self.menu,
            label="Old Label",
            link_type=MenuItemLinkType.INTERNAL,
            url="/old",
        )

        item = NavigationService.update_item(
            request=self.request,
            item=item,
            values={
                "label": "New Label",
                "url": "/new",
            },
        )

        self.assertEqual(item.label, "New Label")
        self.assertEqual(item.url, "/new")

    def test_reorder_items(self):
        first = NavigationMenuItem.objects.create(
            menu=self.menu,
            label="First",
            link_type=MenuItemLinkType.INTERNAL,
            url="/first",
            sort_order=0,
        )

        second = NavigationMenuItem.objects.create(
            menu=self.menu,
            label="Second",
            link_type=MenuItemLinkType.INTERNAL,
            url="/second",
            sort_order=1,
        )

        NavigationService.reorder_items(
            request=self.request,
            menu=self.menu,
            items=[
                {
                    "id": str(first.id),
                    "parent_id": None,
                    "sort_order": 2,
                },
                {
                    "id": str(second.id),
                    "parent_id": None,
                    "sort_order": 1,
                },
            ],
        )

        first.refresh_from_db()
        second.refresh_from_db()

        self.assertEqual(first.sort_order, 2)
        self.assertEqual(second.sort_order, 1)



from .models import MenuItemVisibility
from .repositories import PublicNavigationRepository
from .services import PublicNavigationService


class PublicNavigationTests(TestCase):
    def setUp(self):
        self.menu = NavigationMenu.objects.create(
            name="Public Header",
            slug="public-header",
            location=(
                NavigationLocation.HEADER_PRIMARY
            ),
            is_active=True,
            is_public=True,
        )

        self.parent = NavigationMenuItem.objects.create(
            menu=self.menu,
            label="Services",
            link_type=MenuItemLinkType.INTERNAL,
            url="/services",
            visibility=MenuItemVisibility.EVERYONE,
            sort_order=1,
        )

        self.child = NavigationMenuItem.objects.create(
            menu=self.menu,
            parent=self.parent,
            label="Web Development",
            link_type=MenuItemLinkType.INTERNAL,
            url="/services/web-development",
            visibility=MenuItemVisibility.EVERYONE,
            sort_order=1,
        )

        self.private_item = (
            NavigationMenuItem.objects.create(
                menu=self.menu,
                label="Dashboard",
                link_type=MenuItemLinkType.INTERNAL,
                url="/dashboard",
                visibility=(
                    MenuItemVisibility.AUTHENTICATED
                ),
                sort_order=2,
            )
        )

        self.inactive_item = (
            NavigationMenuItem.objects.create(
                menu=self.menu,
                label="Inactive",
                link_type=MenuItemLinkType.INTERNAL,
                url="/inactive",
                visibility=(
                    MenuItemVisibility.EVERYONE
                ),
                is_active=False,
                sort_order=3,
            )
        )

    def test_public_menu_by_slug(self):
        menu = (
            PublicNavigationRepository.menu_by_slug(
                "public-header"
            )
        )

        self.assertEqual(menu.id, self.menu.id)

    def test_private_menu_is_not_public(self):
        self.menu.is_public = False
        self.menu.save()

        menu = (
            PublicNavigationRepository.menu_by_slug(
                "public-header"
            )
        )

        self.assertIsNone(menu)

    def test_public_items_exclude_restricted_items(self):
        items = list(
            PublicNavigationRepository.items_for_menu(
                self.menu.id
            )
        )

        item_ids = {
            item.id
            for item in items
        }

        self.assertIn(self.parent.id, item_ids)
        self.assertIn(self.child.id, item_ids)
        self.assertNotIn(
            self.private_item.id,
            item_ids,
        )
        self.assertNotIn(
            self.inactive_item.id,
            item_ids,
        )

    def test_public_tree_contains_nested_child(self):
        items = list(
            PublicNavigationRepository.items_for_menu(
                self.menu.id
            )
        )

        tree = PublicNavigationService.build_tree(
            items
        )

        self.assertEqual(len(tree), 1)
        self.assertEqual(
            tree[0]["label"],
            "Services",
        )
        self.assertEqual(
            tree[0]["children"][0]["label"],
            "Web Development",
        )

    def test_orphaned_child_is_not_returned_as_root(self):
        self.parent.visibility = (
            MenuItemVisibility.AUTHENTICATED
        )
        self.parent.save()

        items = list(
            PublicNavigationRepository.items_for_menu(
                self.menu.id
            )
        )

        tree = PublicNavigationService.build_tree(
            items
        )

        self.assertEqual(tree, [])

    def test_public_locations_filter(self):
        menus = list(
            PublicNavigationRepository
            .menus_by_location(
                NavigationLocation.HEADER_PRIMARY
            )
        )

        self.assertEqual(len(menus), 1)
        self.assertEqual(
            menus[0].id,
            self.menu.id,
        )
