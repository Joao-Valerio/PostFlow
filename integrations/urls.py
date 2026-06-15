from django.urls import path

from . import views

app_name = "integrations"

urlpatterns = [
    path("accounts/", views.account_list, name="account_list"),
    path("connect/<str:platform>/", views.oauth_connect, name="oauth_connect"),
    path("callback/<str:platform>/", views.oauth_callback, name="oauth_callback"),
    path(
        "disconnect/<uuid:account_id>/",
        views.account_disconnect,
        name="account_disconnect",
    ),
]
