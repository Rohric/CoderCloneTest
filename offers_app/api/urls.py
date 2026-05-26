# URL routes for offer list, single offer, and individual offer detail items.
from django.urls import path

from .views import OfferDetailItemView, OfferDetailView, OfferListView

urlpatterns = [
    path("offers/", OfferListView.as_view(), name="offer-list"),
    path("offers/<int:pk>/", OfferDetailView.as_view(), name="offer-detail"),
    path("offerdetails/<int:pk>/", OfferDetailItemView.as_view(), name="offerdetail-detail"),
]
