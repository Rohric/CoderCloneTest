from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Validates that the email is unique and both passwords match before creating a user."""

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "repeated_password",
            "type",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Diese E-Mail-Adresse ist bereits vergeben."
            )
        return value

    def validate(self, data):
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Passwörter stimmen nicht überein."}
            )
        return data

    def create(self, validated_data):
        # Remove the confirmation field before passing to create_user.
        validated_data.pop("repeated_password")
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer exposing basic user identity fields."""

    class Meta:
        model = User
        fields = ["user_id", "username", "email", "type"]
