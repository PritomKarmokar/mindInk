from django.urls import path

from .views import (
    SignUpAPIView,
    LogInAPIView,
    RequestPasswordResetAPIView,
    ResetPasswordAPIView,
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
        ResetPasswordAPIView.as_view(),
        name="reset_password",
    ),
]
