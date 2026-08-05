from django.contrib import admin

from .models import (
    Service,
    ServiceFaq,
    ServiceFeature,
    ServiceProcessStep,
    ServiceRevision,
    ServiceSeo,
    ServiceTechnology,
)


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 0


class ServiceProcessStepInline(admin.TabularInline):
    model = ServiceProcessStep
    extra = 0


class ServiceTechnologyInline(admin.TabularInline):
    model = ServiceTechnology
    extra = 0


class ServiceFaqInline(admin.TabularInline):
    model = ServiceFaq
    extra = 0


class ServiceSeoInline(admin.StackedInline):
    model = ServiceSeo
    extra = 0
    max_num = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "status",
        "is_featured",
        "is_active",
        "sort_order",
        "published_at",
        "scheduled_for",
    )
    list_filter = (
        "status",
        "is_featured",
        "is_active",
    )
    search_fields = (
        "title",
        "slug",
        "short_description",
    )
    readonly_fields = (
        "current_revision_number",
        "published_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        ServiceSeoInline,
        ServiceFeatureInline,
        ServiceProcessStepInline,
        ServiceTechnologyInline,
        ServiceFaqInline,
    )


@admin.register(ServiceRevision)
class ServiceRevisionAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "revision_number",
        "change_summary",
        "created_at",
    )
    search_fields = (
        "service__title",
        "change_summary",
    )
