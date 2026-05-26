from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("user_auth_app.api.urls")),
    path("api/", include("profile_app.api.urls")),
    path("api/", include("offers_app.api.urls")),
    path("api/", include("orders_app.api.urls")),
    path("api/", include("review_app.api.urls")),
    path("api/", include("base_info_app.api.urls")),
]
