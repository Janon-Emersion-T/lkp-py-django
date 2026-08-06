from django.contrib import admin

from .models import (
    Team,
    TeamMember,
    TeamMembership,
    TeamMemberService,
)


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 0
    autocomplete_fields = (
        "team",
    )


class TeamMemberServiceInline(admin.TabularInline):
    model = TeamMemberService
    extra = 0
    autocomplete_fields = (
        "service",
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "team_type",
        "parent",
        "manager",
        "is_active",
        "is_public",
        "sort_order",
    )
    list_filter = (
        "team_type",
        "is_active",
        "is_public",
    )
    search_fields = (
        "name",
        "slug",
        "description",
    )
    prepopulated_fields = {
        "slug": ("name",),
    }
    autocomplete_fields = (
        "parent",
        "manager",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "employee_code",
        "display_name",
        "job_title",
        "employment_status",
        "engagement_type",
        "work_location_type",
        "reports_to",
        "is_public",
        "is_featured",
        "sort_order",
    )
    list_filter = (
        "employment_status",
        "engagement_type",
        "work_location_type",
        "country",
        "is_leadership",
        "is_public",
        "is_featured",
    )
    search_fields = (
        "employee_code",
        "first_name",
        "last_name",
        "preferred_name",
        "job_title",
        "professional_title",
        "email",
    )
    autocomplete_fields = (
        "user",
        "profile_image",
        "reports_to",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        TeamMembershipInline,
        TeamMemberServiceInline,
    )


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "team",
        "role_title",
        "is_primary",
        "is_active",
        "joined_at",
        "left_at",
        "sort_order",
    )
    list_filter = (
        "team",
        "is_primary",
        "is_active",
    )
    search_fields = (
        "member__employee_code",
        "member__first_name",
        "member__last_name",
        "team__name",
        "role_title",
    )
    autocomplete_fields = (
        "member",
        "team",
    )


@admin.register(TeamMemberService)
class TeamMemberServiceAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "service",
        "expertise_level",
        "years_of_experience",
        "is_primary",
        "is_public",
        "sort_order",
    )
    list_filter = (
        "expertise_level",
        "is_primary",
        "is_public",
    )
    search_fields = (
        "member__employee_code",
        "member__first_name",
        "member__last_name",
        "service__title",
    )
    autocomplete_fields = (
        "member",
        "service",
    )
