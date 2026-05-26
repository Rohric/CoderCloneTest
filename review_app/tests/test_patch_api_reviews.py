import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_PATCH_review_owner_success(review_setup, client):
    client.force_authenticate(user=review_setup["customer"])
    review = review_setup["review"]

    url = reverse("review-detail", kwargs={"pk": review.pk})
    response = client.patch(url, {"rating": 2, "description": "Geändert."}, format="json")

    assert response.status_code == 200
    assert response.data["rating"] == 2
    assert response.data["description"] == "Geändert."


@pytest.mark.django_db
def test_PATCH_review_not_auth(review_setup, client):
    review = review_setup["review"]

    url = reverse("review-detail", kwargs={"pk": review.pk})
    response = client.patch(url, {"rating": 1}, format="json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_PATCH_review_non_owner_gets_403(review_setup, client):
    client.force_authenticate(user=review_setup["second_customer"])
    review = review_setup["review"]

    url = reverse("review-detail", kwargs={"pk": review.pk})
    response = client.patch(url, {"rating": 1}, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_PATCH_review_invalid_data_gets_400(review_setup, client):
    client.force_authenticate(user=review_setup["customer"])
    review = review_setup["review"]

    url = reverse("review-detail", kwargs={"pk": review.pk})
    response = client.patch(url, {"rating": "kein_integer"}, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_PATCH_review_not_found(review_setup, client):
    client.force_authenticate(user=review_setup["customer"])

    url = reverse("review-detail", kwargs={"pk": 9999})
    response = client.patch(url, {"rating": 3}, format="json")

    assert response.status_code == 404
