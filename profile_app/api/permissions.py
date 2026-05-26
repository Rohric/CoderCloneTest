# Custom permission restricting PATCH to the profile owner.
from rest_framework.permissions import BasePermission


class IsProfileOwnerForPatch(BasePermission):
    """Allows any authenticated user to GET a profile, but only the owner to PATCH it."""

    message = "Der Benutzer kann NUR sein eigenes Profil bearbeiten."

    def has_object_permission(self, request, view, obj):
        if request.method != "PATCH":
            return True

        return obj.user == request.user
