from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Organization

try:
    from django.contrib import admin
except ImportError:
    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "organization", "role", "is_active")
    list_filter = ("role", "organization", "is_active", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Organização", {"fields": ("organization", "role")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Organização", {"fields": ("organization", "role")}),
    )
