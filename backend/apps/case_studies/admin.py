from django.contrib import admin

from .models import (
    CaseStudy,
    CaseStudyMedia,
    CaseStudyMetric,
    CaseStudyMilestone,
    CaseStudyRevision,
    CaseStudySeo,
    CaseStudyService,
    CaseStudyTechnology,
)


class CaseStudyServiceInline(admin.TabularInline):
    model = CaseStudyService
    extra = 0


class CaseStudyTechnologyInline(admin.TabularInline):
    model = CaseStudyTechnology
    extra = 0


class CaseStudyMediaInline(admin.TabularInline):
    model = CaseStudyMedia
    extra = 0


class CaseStudyMetricInline(admin.TabularInline):
    model = CaseStudyMetric
    extra = 0


class CaseStudyMilestoneInline(admin.TabularInline):
    model = CaseStudyMilestone
    extra = 0


class CaseStudySeoInline(admin.StackedInline):
    model = CaseStudySeo
    extra = 0
    max_num = 1


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "project",
        "industry",
        "status",
        "is_featured",
        "is_active",
        "published_at",
        "scheduled_for",
        "view_count",
    )
    list_filter = (
        "status",
        "industry",
        "is_featured",
        "is_active",
    )
    search_fields = (
        "title",
        "slug",
        "client_name",
        "client__company_name",
        "project__title",
        "short_description",
    )
    readonly_fields = (
        "view_count",
        "current_revision_number",
        "published_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        CaseStudySeoInline,
        CaseStudyServiceInline,
        CaseStudyTechnologyInline,
        CaseStudyMediaInline,
        CaseStudyMetricInline,
        CaseStudyMilestoneInline,
    )


@admin.register(CaseStudyRevision)
class CaseStudyRevisionAdmin(admin.ModelAdmin):
    list_display = (
        "case_study",
        "revision_number",
        "change_summary",
        "created_at",
    )
    search_fields = (
        "case_study__title",
        "change_summary",
    )
