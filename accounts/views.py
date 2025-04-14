from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken

from mindInk.settings import BASE_URL
from .models import User, PasswordReset
from .serializers import (
    SignupSerializer,
    LogInSerializer,
    ResetPasswordSerializer,
    ResetPasswordRequestSerializer,
)


class SignUpAPIView(APIView):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "New User Created, Successfully!",
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogInAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LogInSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]
            password = serializer.data["password"]

            user = authenticate(email=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)

                response = {
                    "message": f"{user.get_username()} logged in successfully!",
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }

                return Response(data=response, status=status.HTTP_200_OK)
            else:
                Response(
                    data={"message": "Invalid credentials"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]
            user = User.objects.get(email=email)

            if user:
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                reset = PasswordReset(email=email, token=token)
                reset.save()

                reset_url = f"{BASE_URL}/auth/reset-password/{token}/"

                return Response(
                    data={
                        "reset_url": reset_url,
                    }
                )
            else:
                return Response(
                    data={"message": "No User with the provided email"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request: Request, token: str) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            new_password = data["new_password"]
            reset_obj = PasswordReset.objects.filter(token=token).first()

            if not reset_obj:
                return Response(
                    data={"error": "Invalid token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = User.objects.get(email=reset_obj.email)

            if user:
                user.set_password(new_password)
                user.save()

                reset_obj.delete()

                return Response(
                    data={"message": "Password reset successful"},
                    status=status.HTTP_200_OK,
                )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
