from rest_framework import serializers

from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Read-only serializer returning the full order representation."""

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class OrderCreateSerializer(serializers.Serializer):
    """
    Accepts only an offer_detail_id and derives all other order fields from it.
    This ensures the order is a snapshot of the OfferDetail at creation time.
    """

    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=OfferDetail.objects.all(),
    )

    def create(self, validated_data):
        offer_detail = validated_data["offer_detail_id"]

        business_user = offer_detail.offer.user
        customer_user = self.context["request"].user

        order = Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            offer_detail=offer_detail,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )

        return order

    def to_representation(self, instance):
        # Delegate the output representation to the full read serializer.
        return OrderSerializer(instance, context=self.context).data


class OrderStatusSerializer(serializers.ModelSerializer):
    """Allows updating only the status field of an existing order."""

    class Meta:
        model = Order
        fields = ["status"]

    def validate_status(self, value):
        allowed = [choice[0] for choice in Order.STATUS_CHOICES]

        if value not in allowed:
            raise serializers.ValidationError(f"Ungültiger Status. Erlaubt: {allowed}")
        return value
