from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=5, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate(self, attrs):
        email = attrs["email"]

        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise ValidationError("Email already exists")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user


class LogInSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=5)
