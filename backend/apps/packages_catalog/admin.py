from django.contrib import admin

from .models import (
    Package,
    PackageAddon,
    PackageComparisonGroup,
    PackageComparisonItem,
    PackageFaq,
    PackageFeature,
    PackageRevision,
    PackageSeo,
    PackageTargetAudience,
)


class PackageFeatureInline(admin.TabularInline):
    model = PackageFeature
    extra = 0


class PackageAddonInline(admin.TabularInline):
    model = PackageAddon
    extra = 0


class PackageAudienceInline(admin.TabularInline):
    model = PackageTargetAudience
    extra = 0


class PackageFaqInline(admin.TabularInline):
    model = PackageFaq
    extra = 0


class PackageSeoInline(admin.StackedInline):
    model = PackageSeo
    extra = 0
    max_num = 1


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "service",
        "pricing_type",
        "price",
        "currency",
        "billing_cycle",
        "status",
        "is_featured",
        "is_popular",
        "is_active",
    )
    list_filter = (
        "category",
        "pricing_type",
        "billing_cycle",
        "status",
        "currency",
        "is_featured",
        "is_popular",
        "is_active",
    )
    search_fields = (
        "name",
        "slug",
        "short_description",
        "service__title",
    )
    readonly_fields = (
        "current_revision_number",
        "published_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        PackageSeoInline,
        PackageFeatureInline,
        PackageAddonInline,
        PackageAudienceInline,
        PackageFaqInline,
    )


@admin.register(PackageRevision)
class PackageRevisionAdmin(admin.ModelAdmin):
    list_display = (
        "package",
        "revision_number",
        "change_summary",
        "created_at",
    )
    search_fields = (
        "package__name",
        "change_summary",
    )


class PackageComparisonItemInline(admin.TabularInline):
    model = PackageComparisonItem
    extra = 0


@admin.register(PackageComparisonGroup)
class PackageComparisonGroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_active",
        "sort_order",
    )
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "slug",
        "description",
    )
    inlines = (PackageComparisonItemInline,)
