from django.contrib import admin

from .models import (
    Project,
    ProjectEvent,
    ProjectFile,
    ProjectMilestone,
    ProjectNote,
    ProjectTeamMember,
)


class ProjectTeamMemberInline(admin.TabularInline):
    model = ProjectTeamMember
    extra = 0


class ProjectMilestoneInline(admin.TabularInline):
    model = ProjectMilestone
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "project_code",
        "title",
        "client",
        "status",
        "priority",
        "progress",
        "deadline",
        "project_manager",
    )
    list_filter = (
        "status",
        "priority",
        "currency",
        "deadline",
    )
    search_fields = (
        "project_code",
        "title",
        "client__company_name",
    )
    readonly_fields = (
        "project_code",
        "completed_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        ProjectTeamMemberInline,
        ProjectMilestoneInline,
    )


admin.site.register(ProjectTeamMember)
admin.site.register(ProjectMilestone)
admin.site.register(ProjectNote)
admin.site.register(ProjectFile)
admin.site.register(ProjectEvent)
