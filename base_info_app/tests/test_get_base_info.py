import pytest
from django.urls import reverse

from offers_app.tests.conftest import OfferFactory, UserFactory
from review_app.models import Review


@pytest.mark.django_db
def test_GET_base_info_success(client):
    business = UserFactory(type="business")
    customer = UserFactory(type="customer")
    OfferFactory(user=business)
    Review.objects.create(business_user=business, reviewer=customer, rating=4, description="Gut.")

    url = reverse("base-info")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["review_count"] == 1
    assert response.data["average_rating"] == 4.0
    assert response.data["business_profile_count"] == 1
    assert response.data["offer_count"] == 1


@pytest.mark.django_db
def test_GET_base_info_no_auth_required(client):
    url = reverse("base-info")
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_GET_base_info_average_rating_one_decimal(client):
    businesses = [UserFactory(type="business") for _ in range(3)]
    customers = [UserFactory(type="customer") for _ in range(3)]

    for business, customer, rating in zip(businesses, customers, [4, 5, 3]):
        Review.objects.create(business_user=business, reviewer=customer, rating=rating, description=".")

    url = reverse("base-info")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["average_rating"] == 4.0
    assert response.data["review_count"] == 3


@pytest.mark.django_db
def test_GET_base_info_empty_database_no_crash(client):
    url = reverse("base-info")
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["review_count"] == 0
    assert response.data["average_rating"] == 0
    assert response.data["business_profile_count"] == 0
    assert response.data["offer_count"] == 0
