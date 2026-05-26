from rest_framework import serializers

from review_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Read-only serializer returning the full review representation."""

    class Meta:
        model = Review
        fields = ["id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "business_user", "reviewer", "created_at", "updated_at"]


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Handles review creation.
    Prevents a customer from submitting a second review for the same business user.
    """

    class Meta:
        model = Review
        fields = ["id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate(self, attrs):
        reviewer = self.context["request"].user
        business_user = attrs.get("business_user")

        if Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise serializers.ValidationError("Du hast bereits eine Bewertung für diesen Business-User abgegeben.")

        return attrs


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Allows updating rating and description; business_user and reviewer are immutable."""

    class Meta:
        model = Review
        fields = ["id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "business_user", "reviewer", "created_at", "updated_at"]
