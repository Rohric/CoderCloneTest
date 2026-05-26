import pytest
from django.urls import reverse

from review_app.models import Review


@pytest.mark.django_db
def test_DELETE_review_owner_success(review_setup, client):
    client.force_authenticate(user=review_setup["customer"])
    review_pk = review_setup["review"].pk

    url = reverse("review-detail", kwargs={"pk": review_pk})
    response = client.delete(url)

    assert response.status_code == 204
    assert not Review.objects.filter(pk=review_pk).exists()


@pytest.mark.django_db
def test_DELETE_review_not_auth(review_setup, client):
    review = review_setup["review"]

    url = reverse("review-detail", kwargs={"pk": review.pk})
    response = client.delete(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_DELETE_review_non_owner_gets_403(review_setup, client):
    client.force_authenticate(user=review_setup["second_customer"])
    review = review_setup["review"]

    url = reverse("review-detail", kwargs={"pk": review.pk})
    response = client.delete(url)

    assert response.status_code == 403
    assert Review.objects.filter(pk=review.pk).exists()


@pytest.mark.django_db
def test_DELETE_review_not_found(review_setup, client):
    client.force_authenticate(user=review_setup["customer"])

    url = reverse("review-detail", kwargs={"pk": 9999})
    response = client.delete(url)

    assert response.status_code == 404
