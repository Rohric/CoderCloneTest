import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_GET_reviews_authenticated(review_setup, client):
    client.force_authenticate(user=review_setup["customer"])

    url = reverse("review-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_GET_reviews_not_auth(review_setup, client):
    url = reverse("review-list")
    response = client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_GET_reviews_filter_by_business_user_id(review_setup, client):
    client.force_authenticate(user=review_setup["customer"])

    url = reverse("review-list")
    response = client.get(url, {"business_user_id": review_setup["business"].pk})

    assert response.status_code == 200
    for review in response.data:
        assert review["business_user"] == review_setup["business"].pk


@pytest.mark.django_db
def test_GET_reviews_filter_by_reviewer_id(review_setup, client):
    client.force_authenticate(user=review_setup["customer"])

    url = reverse("review-list")
    response = client.get(url, {"reviewer_id": review_setup["customer"].pk})

    assert response.status_code == 200
    for review in response.data:
        assert review["reviewer"] == review_setup["customer"].pk
