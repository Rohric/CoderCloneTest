# Custom permissions controlling who can place or manage orders.
from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """Grants access only to authenticated users whose type is 'customer'."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == "customer"


class IsBusinessProfileFromOrder(BasePermission):
    """Grants object-level access only to the business user assigned to the order."""

    def has_object_permission(self, request, view, obj):
        return obj.business_user == request.user


class IsAdminUser(BasePermission):
    """Grants access only to staff users (is_staff=True)."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
