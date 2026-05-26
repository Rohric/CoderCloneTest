import pytest
from django.urls import reverse

from review_app.models import Review


@pytest.mark.django_db
def test_POST_review_customer_success(review_setup, client):
    client.force_authenticate(user=review_setup["second_customer"])

    url = reverse("review-list")
    payload = {"business_user": review_setup["business"].pk, "rating": 5, "description": "Top!"}
    response = client.post(url, payload, format="json")

    assert response.status_code == 201
    assert response.data["reviewer"] == review_setup["second_customer"].pk


@pytest.mark.django_db
def test_POST_review_not_auth(review_setup, client):
    url = reverse("review-list")
    payload = {"business_user": review_setup["business"].pk, "rating": 4, "description": "Test."}
    response = client.post(url, payload, format="json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_POST_review_business_user_gets_403(review_setup, client):
    client.force_authenticate(user=review_setup["business"])

    url = reverse("review-list")
    payload = {"business_user": review_setup["business"].pk, "rating": 3, "description": "Test."}
    response = client.post(url, payload, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_POST_review_invalid_data_gets_400(review_setup, client):
    client.force_authenticate(user=review_setup["second_customer"])

    url = reverse("review-list")
    payload = {"business_user": review_setup["business"].pk}
    response = client.post(url, payload, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_POST_review_duplicate_gets_400_or_403(review_setup, client):
    client.force_authenticate(user=review_setup["customer"])

    url = reverse("review-list")
    payload = {"business_user": review_setup["business"].pk, "rating": 5, "description": "Nochmal."}
    response = client.post(url, payload, format="json")

    assert response.status_code in [400, 403]
    assert Review.objects.filter(reviewer=review_setup["customer"]).count() == 1
