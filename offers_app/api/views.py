from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer, OfferDetail

from .filters import apply_offer_filters
from .pagination import OfferPagination
from .permissions import IsBusinessProfile, IsOfferOwner
from .serializers import OfferCreateResponseSerializer, OfferDetailSerializer, OfferSerializer


class OfferListView(APIView):
    """
    GET: Public list of offers with optional filtering, ordering, search, and pagination.
    POST: Business users only may create a new offer.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsBusinessProfile()]

    def get(self, request):
        queryset = apply_offer_filters(Offer.objects.all(), request.query_params)
        paginator = OfferPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = OfferSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = OfferSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_serializer = OfferCreateResponseSerializer(serializer.instance, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OfferDetailView(APIView):
    """
    GET: Any authenticated user may view a single offer.
    PATCH/DELETE: Only the offer owner may modify or remove it.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOfferOwner()]

    def get(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        serializer = OfferSerializer(offer, context={"request": request})
        return Response(serializer.data)

    def patch(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        self.check_object_permissions(request, offer)
        serializer = OfferSerializer(offer, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_serializer = OfferCreateResponseSerializer(serializer.instance, context={"request": request})
        return Response(response_serializer.data)

    def delete(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        self.check_object_permissions(request, offer)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OfferDetailItemView(APIView):
    """Returns a single OfferDetail tier by its own primary key."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        detail = get_object_or_404(OfferDetail, pk=pk)
        serializer = OfferDetailSerializer(detail)
        return Response(serializer.data)
