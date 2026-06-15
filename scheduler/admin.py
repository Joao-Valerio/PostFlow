from django.contrib import admin

from .models import Post, ScheduledPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "author", "status", "created_at")
    list_filter = ("status", "organization")
    search_fields = ("title", "content")


@admin.register(ScheduledPost)
class ScheduledPostAdmin(admin.ModelAdmin):
    list_display = ("post", "social_account", "scheduled_at", "status", "retry_count")
    list_filter = ("status",)
    date_hierarchy = "scheduled_at"
