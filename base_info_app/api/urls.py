# URL route for the public base-info statistics endpoint.
from django.urls import path

from base_info_app.api.views import BaseInfoView

urlpatterns = [
    path("base-info/", BaseInfoView.as_view(), name="base-info"),
]
