from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from review_app.models import Review

from .permissions import IsCustomer, IsReviewOwner
from .serializers import ReviewCreateSerializer, ReviewSerializer, ReviewUpdateSerializer


class ReviewListView(APIView):
    """
    GET: Any authenticated user may list reviews, with optional filtering and ordering.
    POST: Customers only may submit a new review.
    """

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]

    def get(self, request):
        queryset = Review.objects.all()

        business_user_id = request.query_params.get("business_user_id")
        reviewer_id = request.query_params.get("reviewer_id")
        ordering = request.query_params.get("ordering")

        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)

        valid_ordering = ["rating", "-rating", "updated_at", "-updated_at"]
        if ordering in valid_ordering:
            queryset = queryset.order_by(ordering)

        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewer=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewDetailView(APIView):
    """PATCH/DELETE: Only the reviewer who created the review may modify or remove it."""

    def get_permissions(self):
        return [IsAuthenticated(), IsReviewOwner()]

    def patch(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        self.check_object_permissions(request, review)
        serializer = ReviewUpdateSerializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        self.check_object_permissions(request, review)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
