from rest_framework import serializers

from profile_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Full profile serializer used for GET/PATCH on a single profile."""

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(required=False)
    type = serializers.CharField(source="user.type", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["email"] = instance.user.email
        for key, value in data.items():
            if value is None:
                data[key] = ""
        return data

    def update(self, instance, validated_data):
        email = validated_data.pop("email", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if email is not None:
            instance.user.email = email
            instance.user.save()
        return instance


class ProfileBusinessSerializer(serializers.ModelSerializer):
    """Reduced profile serializer for the public business profiles list."""

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            if value is None:
                data[key] = ""
        return data


class ProfileCustomerSerializer(serializers.ModelSerializer):
    """Minimal profile serializer for the public customer profiles list."""

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    # Exposed as uploaded_at to match the frontend contract.
    uploaded_at = serializers.DateTimeField(source="created_at", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "uploaded_at",
            "type",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            if value is None:
                data[key] = ""
        return data
