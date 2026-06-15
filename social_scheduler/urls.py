from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from scheduler.views import dashboard, landing

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing, name="landing"),
    path("dashboard/", dashboard, name="dashboard"),
    path("accounts/", include("accounts.urls")),
    path("scheduler/", include("scheduler.urls")),
    path("integrations/", include("integrations.urls")),
]

handler404 = "social_scheduler.views.page_not_found"
handler500 = "social_scheduler.views.server_error"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
