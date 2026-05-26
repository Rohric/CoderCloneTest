from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer
from review_app.models import Review

User = get_user_model()


class BaseInfoView(APIView):
    """
    Public endpoint returning aggregate platform stats.
    No authentication required so the landing page can display these figures.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        review_count = Review.objects.count()

        avg = Review.objects.aggregate(avg=Avg("rating"))["avg"]
        # Round to one decimal place; fall back to 0 when no reviews exist yet.
        average_rating = round(avg, 1) if avg else 0

        business_profile_count = User.objects.filter(type="business").count()
        offer_count = Offer.objects.count()

        return Response(
            {
                "review_count": review_count,
                "average_rating": average_rating,
                "business_profile_count": business_profile_count,
                "offer_count": offer_count,
            }
        )
