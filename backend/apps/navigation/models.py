from django.core.exceptions import ValidationError
from django.db import models

from apps.common.models import BaseModel


class NavigationLocation(models.TextChoices):
    HEADER_PRIMARY = (
        "header_primary",
        "Header primary",
    )
    HEADER_SECONDARY = (
        "header_secondary",
        "Header secondary",
    )
    FOOTER_PRIMARY = (
        "footer_primary",
        "Footer primary",
    )
    FOOTER_SECONDARY = (
        "footer_secondary",
        "Footer secondary",
    )
    FOOTER_LEGAL = (
        "footer_legal",
        "Footer legal",
    )
    MOBILE = "mobile", "Mobile"
    DASHBOARD = "dashboard", "Dashboard"
    CLIENT_PORTAL = (
        "client_portal",
        "Client portal",
    )
    CUSTOM = "custom", "Custom"


class MenuItemLinkType(models.TextChoices):
    INTERNAL = "internal", "Internal URL"
    EXTERNAL = "external", "External URL"
    ROUTE = "route", "Named route"
    CMS_PAGE = "cms_page", "CMS page"
    SERVICE = "service", "Service"
    PACKAGE = "package", "Package"
    INDUSTRY = "industry", "Industry"
    INSIGHT = "insight", "Insight"
    CASE_STUDY = "case_study", "Case study"
    CAREERS = "careers", "Careers"
    CONTACT = "contact", "Contact"
    QUOTE = "quote", "Request quote"
    CUSTOM = "custom", "Custom"


class MenuItemVisibility(models.TextChoices):
    EVERYONE = "everyone", "Everyone"
    GUESTS = "guests", "Guests only"
    AUTHENTICATED = (
        "authenticated",
        "Authenticated users",
    )
    STAFF = "staff", "Staff only"
    SUPERUSER = "superuser", "Superusers only"


class NavigationMenu(BaseModel):
    name = models.CharField(
        max_length=150,
        db_index=True,
    )

    slug = models.SlugField(
        max_length=170,
        unique=True,
        db_index=True,
    )

    location = models.CharField(
        max_length=40,
        choices=NavigationLocation.choices,
        default=NavigationLocation.CUSTOM,
        db_index=True,
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    is_public = models.BooleanField(
        default=True,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "name",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("name",),
                condition=models.Q(is_deleted=False),
                name="unique_active_navigation_menu_name",
            ),
        ]
        indexes = [
            models.Index(
                fields=("location", "is_active"),
            ),
            models.Index(
                fields=("is_public", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.name


class NavigationMenuItem(BaseModel):
    menu = models.ForeignKey(
        NavigationMenu,
        on_delete=models.CASCADE,
        related_name="items",
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    label = models.CharField(
        max_length=150,
        db_index=True,
    )

    link_type = models.CharField(
        max_length=30,
        choices=MenuItemLinkType.choices,
        default=MenuItemLinkType.INTERNAL,
        db_index=True,
    )

    url = models.CharField(
        max_length=500,
        blank=True,
    )

    route_name = models.CharField(
        max_length=200,
        blank=True,
    )

    route_parameters = models.JSONField(
        default=dict,
        blank=True,
    )

    cms_page = models.ForeignKey(
        "cms.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="navigation_items",
    )

    service = models.ForeignKey(
        "services_catalog.Service",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="navigation_items",
    )

    package = models.ForeignKey(
        "packages_catalog.Package",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="navigation_items",
    )

    industry = models.ForeignKey(
        "industries.Industry",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="navigation_items",
    )

    insight = models.ForeignKey(
        "insights.InsightArticle",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="navigation_items",
    )

    case_study = models.ForeignKey(
        "case_studies.CaseStudy",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="navigation_items",
    )

    visibility = models.CharField(
        max_length=30,
        choices=MenuItemVisibility.choices,
        default=MenuItemVisibility.EVERYONE,
        db_index=True,
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    css_class = models.CharField(
        max_length=200,
        blank=True,
    )

    target_blank = models.BooleanField(default=False)

    rel_attribute = models.CharField(
        max_length=100,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    is_featured = models.BooleanField(
        default=False,
        db_index=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "label",
        )
        indexes = [
            models.Index(
                fields=("menu", "parent", "sort_order"),
            ),
            models.Index(
                fields=("menu", "is_active"),
            ),
            models.Index(
                fields=("visibility", "is_active"),
            ),
            models.Index(
                fields=("is_featured", "sort_order"),
            ),
        ]

    def clean(self):
        super().clean()

        if self.parent_id:
            if self.parent_id == self.id:
                raise ValidationError(
                    {
                        "parent": (
                            "A menu item cannot be its own parent."
                        ),
                    }
                )

            if self.parent.menu_id != self.menu_id:
                raise ValidationError(
                    {
                        "parent": (
                            "Parent item must belong to the same menu."
                        ),
                    }
                )

            ancestor = self.parent

            while ancestor is not None:
                if ancestor.pk == self.pk:
                    raise ValidationError(
                        {
                            "parent": (
                                "Circular menu nesting is not allowed."
                            ),
                        }
                    )

                ancestor = ancestor.parent

        required_relationships = {
            MenuItemLinkType.CMS_PAGE: self.cms_page_id,
            MenuItemLinkType.SERVICE: self.service_id,
            MenuItemLinkType.PACKAGE: self.package_id,
            MenuItemLinkType.INDUSTRY: self.industry_id,
            MenuItemLinkType.INSIGHT: self.insight_id,
            MenuItemLinkType.CASE_STUDY: (
                self.case_study_id
            ),
        }

        required_id = required_relationships.get(
            self.link_type
        )

        if (
            self.link_type in required_relationships
            and not required_id
        ):
            raise ValidationError(
                {
                    "link_type": (
                        f"{self.get_link_type_display()} "
                        "requires a linked object."
                    ),
                }
            )

        if (
            self.link_type
            in {
                MenuItemLinkType.INTERNAL,
                MenuItemLinkType.EXTERNAL,
                MenuItemLinkType.CUSTOM,
            }
            and not self.url
        ):
            raise ValidationError(
                {
                    "url": (
                        "A URL is required for this link type."
                    ),
                }
            )

        if (
            self.link_type == MenuItemLinkType.ROUTE
            and not self.route_name
        ):
            raise ValidationError(
                {
                    "route_name": (
                        "A route name is required."
                    ),
                }
            )

    @property
    def depth(self):
        depth = 0
        ancestor = self.parent

        while ancestor is not None:
            depth += 1
            ancestor = ancestor.parent

        return depth

    @property
    def resolved_url(self):
        if self.link_type in {
            MenuItemLinkType.INTERNAL,
            MenuItemLinkType.EXTERNAL,
            MenuItemLinkType.CUSTOM,
        }:
            return self.url

        if self.link_type == MenuItemLinkType.CONTACT:
            return "/contact"

        if self.link_type == MenuItemLinkType.QUOTE:
            return "/request-quote"

        if self.link_type == MenuItemLinkType.CAREERS:
            return "/careers"

        if self.link_type == MenuItemLinkType.CMS_PAGE:
            return (
                f"/{self.cms_page.slug}"
                if self.cms_page
                else ""
            )

        if self.link_type == MenuItemLinkType.SERVICE:
            return (
                f"/services/{self.service.slug}"
                if self.service
                else ""
            )

        if self.link_type == MenuItemLinkType.PACKAGE:
            return (
                f"/packages/{self.package.slug}"
                if self.package
                else ""
            )

        if self.link_type == MenuItemLinkType.INDUSTRY:
            return (
                f"/industries/{self.industry.slug}"
                if self.industry
                else ""
            )

        if self.link_type == MenuItemLinkType.INSIGHT:
            return (
                f"/insights/{self.insight.slug}"
                if self.insight
                else ""
            )

        if self.link_type == MenuItemLinkType.CASE_STUDY:
            return (
                f"/case-studies/{self.case_study.slug}"
                if self.case_study
                else ""
            )

        if self.link_type == MenuItemLinkType.ROUTE:
            return self.route_name

        return ""

    def __str__(self):
        return f"{self.menu.name} — {self.label}"
