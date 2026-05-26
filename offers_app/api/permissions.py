# Custom permissions for offer access control.
from rest_framework.permissions import BasePermission


class IsBusinessProfile(BasePermission):
    """Grants access only to authenticated users whose type is 'business'."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.type == "business"


class IsOfferOwner(BasePermission):
    """Grants object-level access only to the user who created the offer."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
