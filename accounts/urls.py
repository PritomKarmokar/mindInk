from django.urls import path

from .views import SignUpAPIView, LogInAPIView

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("login/", LogInAPIView.as_view(), name="login"),
]
