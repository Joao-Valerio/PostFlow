from django.urls import path

from . import views

app_name = "scheduler"

urlpatterns = [
    path("posts/", views.post_list, name="post_list"),
    path("posts/create/", views.post_create, name="post_create"),
    path("posts/<uuid:post_id>/edit/", views.post_edit, name="post_edit"),
    path("posts/<uuid:post_id>/delete/", views.post_delete, name="post_delete"),
    path("posts/<uuid:post_id>/schedule/", views.post_schedule, name="post_schedule"),
    path("calendar/", views.calendar, name="calendar"),
    path("calendar/events/", views.calendar_events, name="calendar_events"),
    path(
        "calendar/reschedule/<uuid:schedule_id>/",
        views.calendar_reschedule,
        name="calendar_reschedule",
    ),
    path("history/", views.history, name="history"),
    path(
        "history/<uuid:schedule_id>/cancel/",
        views.schedule_cancel,
        name="schedule_cancel",
    ),
]
