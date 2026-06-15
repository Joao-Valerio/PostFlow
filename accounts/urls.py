from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("password/change/", views.UserPasswordChangeView.as_view(), name="password_change"),
    path("password/reset/", views.UserPasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/done/",
        views.UserPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password/reset/<uidb64>/<token>/",
        views.UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/complete/",
        views.UserPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
