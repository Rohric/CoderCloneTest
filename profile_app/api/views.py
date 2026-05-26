from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from profile_app.models import Profile

from .permissions import IsProfileOwnerForPatch
from .serializers import ProfileBusinessSerializer, ProfileCustomerSerializer, ProfileSerializer


class ProfileDetailView(APIView):
    """GET and PATCH a single profile. Only the owner may PATCH their own profile."""

    permission_classes = [IsAuthenticated, IsProfileOwnerForPatch]

    def get(self, request, pk):
        profile = get_object_or_404(Profile, user_id=pk)
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request, pk):
        profile = get_object_or_404(Profile, user_id=pk)
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfileBusinessView(APIView):
    """Returns all profiles belonging to business users."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = Profile.objects.filter(user__type="business")
        serializer = ProfileBusinessSerializer(profiles, many=True)
        return Response(serializer.data)


class ProfileCustomerView(APIView):
    """Returns all profiles belonging to customer users."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = Profile.objects.filter(user__type="customer")
        serializer = ProfileCustomerSerializer(profiles, many=True)
        return Response(serializer.data)
