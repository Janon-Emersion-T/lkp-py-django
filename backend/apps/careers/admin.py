from django.contrib import admin

from .models import (
    ApplicationAnswer,
    ApplicationEvaluation,
    ApplicationNote,
    ApplicationQuestion,
    EmploymentType,
    Interview,
    InterviewParticipant,
    JobApplication,
    JobDepartment,
    JobListing,
    JobPosition,
)


@admin.register(JobDepartment)
class JobDepartmentAdmin(admin.ModelAdmin):
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
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
        "sort_order",
    )
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "code",
        "description",
    )


@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "department",
        "employment_type",
        "experience_level",
        "remote_policy",
        "location",
        "is_active",
    )
    list_filter = (
        "department",
        "employment_type",
        "experience_level",
        "remote_policy",
        "is_active",
    )
    search_fields = (
        "title",
        "slug",
        "summary",
        "location",
    )
    autocomplete_fields = (
        "department",
        "employment_type",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }


@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = (
        "reference_code",
        "position",
        "status",
        "number_of_openings",
        "application_deadline",
        "published_at",
        "is_featured",
        "is_active",
    )
    list_filter = (
        "status",
        "is_featured",
        "is_active",
        "position__department",
        "position__employment_type",
    )
    search_fields = (
        "reference_code",
        "position__title",
        "position__department__name",
    )
    autocomplete_fields = ("position",)
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )



class ApplicationAnswerInline(admin.TabularInline):
    model = ApplicationAnswer
    extra = 0
    readonly_fields = (
        "question",
        "answer",
        "created_at",
    )
    can_delete = False


class ApplicationNoteInline(admin.TabularInline):
    model = ApplicationNote
    extra = 0
    fields = (
        "author",
        "note",
        "is_private",
        "created_at",
    )
    readonly_fields = ("created_at",)


@admin.register(ApplicationQuestion)
class ApplicationQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "listing",
        "question_type",
        "is_required",
        "is_active",
        "sort_order",
    )
    list_filter = (
        "question_type",
        "is_required",
        "is_active",
    )
    search_fields = (
        "question",
        "listing__reference_code",
        "listing__position__title",
    )
    autocomplete_fields = ("listing",)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "applicant_name",
        "email",
        "listing",
        "status",
        "source",
        "assigned_to",
        "submitted_at",
        "rating",
    )
    list_filter = (
        "status",
        "source",
        "listing__position__department",
        "listing__position__employment_type",
    )
    search_fields = (
        "applicant_name",
        "email",
        "phone",
        "current_company",
        "current_position",
        "listing__reference_code",
        "listing__position__title",
    )
    autocomplete_fields = (
        "listing",
        "resume_asset",
        "assigned_to",
    )
    readonly_fields = (
        "id",
        "submitted_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (
        ApplicationAnswerInline,
        ApplicationNoteInline,
    )


@admin.register(ApplicationNote)
class ApplicationNoteAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "author",
        "is_private",
        "created_at",
    )
    list_filter = ("is_private",)
    search_fields = (
        "application__applicant_name",
        "application__email",
        "note",
    )
    autocomplete_fields = (
        "application",
        "author",
    )



class InterviewParticipantInline(admin.TabularInline):
    model = InterviewParticipant
    extra = 0
    autocomplete_fields = ("user",)


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "application",
        "interview_type",
        "status",
        "scheduled_start",
        "scheduled_end",
        "organizer",
    )
    list_filter = (
        "interview_type",
        "status",
        "timezone_name",
    )
    search_fields = (
        "title",
        "application__applicant_name",
        "application__email",
        "application__listing__reference_code",
        "location",
    )
    autocomplete_fields = (
        "application",
        "organizer",
    )
    readonly_fields = (
        "id",
        "completed_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (InterviewParticipantInline,)


@admin.register(ApplicationEvaluation)
class ApplicationEvaluationAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "evaluator",
        "overall_score",
        "recommendation",
        "interview",
        "submitted_at",
    )
    list_filter = (
        "recommendation",
        "overall_score",
    )
    search_fields = (
        "application__applicant_name",
        "application__email",
        "evaluator__username",
        "strengths",
        "concerns",
        "comments",
    )
    autocomplete_fields = (
        "application",
        "interview",
        "evaluator",
    )
    readonly_fields = (
        "id",
        "submitted_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
