from django.contrib import admin

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "author_name",
        "company_name",
        "rating",
        "source",
        "status",
        "is_featured",
        "is_verified",
        "is_active",
        "published_at",
    )

    list_filter = (
        "status",
        "source",
        "rating",
        "is_featured",
        "is_verified",
        "is_active",
    )

    search_fields = (
        "author_name",
        "author_position",
        "company_name",
        "content",
        "client__name",
        "project__title",
    )

    autocomplete_fields = (
        "client",
        "project",
        "author_image",
        "company_logo",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    ordering = (
        "sort_order",
        "-published_at",
        "-created_at",
    )
