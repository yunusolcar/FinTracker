from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
        min_length=8,
        error_messages={
            "min_length": "Password must be at least 8 characters.",
            "required": "Password field is required.",
        },
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        error_messages={"required": "Password confirmation field is required."},
    )

    class Meta:
        model = User
        fields = ("id", "email", "username", "password", "password2")
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "required": "Email field is required.",
                    "invalid": "Please enter a valid email address.",
                }
            },
            "username": {
                "error_messages": {
                    "required": "Username field is required.",
                    "min_length": "Username must be at least 3 characters.",
                },
                "min_length": 3,
            },
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username")
