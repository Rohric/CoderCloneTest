from django.contrib.auth import get_user_model
from django.db.models import Min
from rest_framework import serializers

from offers_app.models import Offer, OfferDetail

User = get_user_model()


class OfferDetailSerializer(serializers.ModelSerializer):
    """Full read serializer for a single OfferDetail tier."""

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """Embeds a hyperlink to each detail tier instead of its full data."""

    url = serializers.HyperlinkedIdentityField(
        view_name="offerdetail-detail",
    )

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]


class OfferTypeSerializer(serializers.ModelSerializer):
    """Used internally to validate incoming detail data before create/update."""

    class Meta:
        model = OfferDetail
        fields = [
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class UserDetailsSerializer(serializers.ModelSerializer):
    """Exposes the author's name alongside their username for offer listings."""

    first_name = serializers.CharField(source="profile.first_name")
    last_name = serializers.CharField(source="profile.last_name")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class OfferSerializer(serializers.ModelSerializer):
    """Full offer serializer with nested detail links and computed price/time fields."""

    details = OfferDetailLinkSerializer(many=True, read_only=True)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source="user", read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def to_internal_value(self, data):
        # Validate and pre-process the nested details list before the rest of the fields.
        details_data = data.get("details", [])

        if details_data:
            detail_serializer = OfferTypeSerializer(many=True, data=details_data)
            if not detail_serializer.is_valid():
                raise serializers.ValidationError({"details": detail_serializer.errors})

            # On creation exactly 3 tiers (basic, standard, premium) are required.
            if self.instance is None and len(detail_serializer.validated_data) != 3:
                raise serializers.ValidationError({"details": "Ein Offer muss genau 3 Details enthalten."})

            ret = super().to_internal_value(data)
            ret["details"] = detail_serializer.validated_data
            return ret

        return super().to_internal_value(data)

    def create(self, validated_data):
        details_data = validated_data.pop("details")

        offer = Offer.objects.create(
            user=self.context["request"].user,
            **validated_data,
        )

        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)

        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data:
            # Update each tier by matching on offer_type, not by position.
            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")
                detail = instance.details.get(offer_type=offer_type)
                for attr, value in detail_data.items():
                    setattr(detail, attr, value)
                detail.save()

        return instance

    def get_min_price(self, obj):
        return obj.details.aggregate(Min("price"))["price__min"]

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(Min("delivery_time_in_days"))["delivery_time_in_days__min"]


class OfferCreateResponseSerializer(serializers.ModelSerializer):
    """Response serializer for POST/PATCH — returns full detail objects instead of links."""

    details = OfferDetailSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source="user", read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_min_price(self, obj):
        return obj.details.aggregate(Min("price"))["price__min"]

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(Min("delivery_time_in_days"))["delivery_time_in_days__min"]
