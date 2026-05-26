# URL routes for profile detail, business profiles list, and customer profiles list.
from django.urls import path

from .views import ProfileBusinessView, ProfileCustomerView, ProfileDetailView

urlpatterns = [
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profiles/business/", ProfileBusinessView.as_view(), name="profile-business-list"),
    path("profiles/customer/", ProfileCustomerView.as_view(), name="profile-customer-list"),
]
