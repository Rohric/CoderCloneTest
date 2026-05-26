# URL routes for authentication: registration, login, logout, and profile.
from django.urls import path
from .views import RegistrationView, CustomLoginView, LogoutView, ProfileView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
