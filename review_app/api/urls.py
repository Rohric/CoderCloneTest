# URL routes for review list and single review detail.
from django.urls import path

from review_app.api.views import ReviewDetailView, ReviewListView

urlpatterns = [
    path("reviews/", ReviewListView.as_view(), name="review-list"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
]
