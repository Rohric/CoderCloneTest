# Profile model storing extended user information beyond the auth User.
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    """One-to-one extension of User holding contact and presentation details."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    file = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    working_hours = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"
