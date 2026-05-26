from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.models import Order

from .permissions import IsAdminUser, IsBusinessProfileFromOrder, IsCustomer
from .serializers import OrderCreateSerializer, OrderSerializer, OrderStatusSerializer

User = get_user_model()


class OrderListView(APIView):
    """
    GET: Returns all orders where the authenticated user is either customer or business party.
    POST: Customers only may place a new order by supplying an offer_detail_id.
    """

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]

    def get(self, request):
        orders = Order.objects.filter(customer_user=request.user) | Order.objects.filter(business_user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    """
    PATCH: Business party of the order may update its status.
    DELETE: Admin users only may permanently remove an order.
    """

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        if self.request.method == "PATCH":
            return [IsAuthenticated(), IsBusinessProfileFromOrder()]
        return [IsAuthenticated()]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(request, order)
        serializer = OrderStatusSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(serializer.instance).data)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class OrderCountView(APIView):
    """Returns the number of in-progress orders for a given business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(User, pk=business_user_id)
        count = Order.objects.filter(business_user=business_user, status="in_progress").count()
        return Response({"order_count": count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """Returns the number of completed orders for a given business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(User, pk=business_user_id)
        count = Order.objects.filter(business_user=business_user, status="completed").count()
        return Response({"completed_order_count": count}, status=status.HTTP_200_OK)
