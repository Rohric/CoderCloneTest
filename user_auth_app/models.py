# Custom User model extending Django's AbstractUser.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User with an additional type field distinguishing customers from businesses."""

    USER_TYPE_CHOICES = [
        ("customer", "Customer"),
        ("business", "Business"),
    ]

    type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
    )

    def __str__(self):
        return self.username
