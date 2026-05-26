import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from review_app.models import Review

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def review_setup(db):
    customer = User.objects.create_user(
        username="customer_jane",
        email="jane@customer.de",
        password="Test123!",
        type="customer",
    )

    business = User.objects.create_user(
        username="business_max",
        email="max@business.de",
        password="Test123!",
        type="business",
    )

    second_customer = User.objects.create_user(
        username="customer_bob",
        email="bob@customer.de",
        password="Test123!",
        type="customer",
    )

    review = Review.objects.create(
        business_user=business,
        reviewer=customer,
        rating=4,
        description="Sehr professioneller Service.",
    )

    return {
        "customer": customer,
        "business": business,
        "second_customer": second_customer,
        "review": review,
    }
