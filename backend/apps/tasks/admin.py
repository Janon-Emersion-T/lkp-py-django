from django.contrib import admin

from .models import (
    Task,
    TaskAssignee,
    TaskAttachment,
    TaskChecklistItem,
    TaskComment,
    TaskDependency,
    TaskEvent,
    TaskTimeLog,
    TaskWatcher,
)


class TaskChecklistInline(admin.TabularInline):
    model = TaskChecklistItem
    extra = 0


class TaskAssigneeInline(admin.TabularInline):
    model = TaskAssignee
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "status",
        "priority",
        "assignee",
        "progress",
        "due_date",
        "actual_hours",
    )
    list_filter = (
        "status",
        "priority",
        "is_recurring",
        "due_date",
    )
    search_fields = (
        "title",
        "description",
        "project__title",
        "project__project_code",
    )
    readonly_fields = (
        "completed_at",
        "actual_hours",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        TaskChecklistInline,
        TaskAssigneeInline,
    )


admin.site.register(TaskWatcher)
admin.site.register(TaskComment)
admin.site.register(TaskAttachment)
admin.site.register(TaskDependency)
admin.site.register(TaskTimeLog)
admin.site.register(TaskEvent)
