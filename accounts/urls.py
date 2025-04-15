from django.urls import path

from .views import (
    SignUpAPIView,
    LogInAPIView,
    RequestPasswordResetAPIView,
    ResetPasswordAPIView,
    ResetPasswordPageView,
    LogoutAPIView,
)

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("login/", LogInAPIView.as_view(), name="login"),
    path(
        "reset-password-request/",
        RequestPasswordResetAPIView.as_view(),
        name="reset_password_request",
    ),
    path(
        "reset-password/<str:token>/",
        ResetPasswordPageView.as_view(),
        name="reset_password",
    ),
    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="logout",
    ),
]
