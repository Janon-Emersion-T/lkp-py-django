from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "username", "is_staff", "is_active")
    ordering = ("email",)
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("full_name",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email", "full_name")}),)

