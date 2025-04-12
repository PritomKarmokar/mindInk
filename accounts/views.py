from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer, LogInSerializer


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
