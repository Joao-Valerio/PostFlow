from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "user", "resource_type", "created_at")
    list_filter = ("action", "resource_type")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
