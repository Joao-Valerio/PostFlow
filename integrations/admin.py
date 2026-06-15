from django.contrib import admin

from .models import SocialAccount


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ("account_name", "platform", "organization", "is_active", "created_at")
    list_filter = ("platform", "is_active", "organization")
    readonly_fields = ("created_at", "updated_at")
