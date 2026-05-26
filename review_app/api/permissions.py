# Custom permissions for review access control.
from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """Grants access only to authenticated users whose type is 'customer'."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == "customer"


class IsReviewOwner(BasePermission):
    """Grants object-level access only to the user who wrote the review."""

    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user
