import pytest
from django.urls import reverse

from offers_app.models import Offer
from offers_app.tests.conftest import OfferFactory, UserFactory


@pytest.mark.django_db
def test_delete_offer_success(authenticated_business_client):
    client, user = authenticated_business_client
    offer = OfferFactory(user=user)

    url = reverse("offer-detail", args=[offer.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert not Offer.objects.filter(id=offer.id).exists()


@pytest.mark.django_db
def test_delete_offer_not_auth(client):
    offer = OfferFactory()

    url = reverse("offer-detail", args=[offer.id])
    response = client.delete(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_offer_not_owner(client):
    user_a = UserFactory(type="business")
    user_b = UserFactory(type="business")
    offer = OfferFactory(user=user_a)

    client.force_authenticate(user=user_b)

    url = reverse("offer-detail", args=[offer.id])
    response = client.delete(url)

    assert response.status_code == 403
    assert Offer.objects.filter(id=offer.id).exists()


@pytest.mark.django_db
def test_delete_offer_not_found(authenticated_business_client):
    client, user = authenticated_business_client

    url = reverse("offer-detail", args=[99999])
    response = client.delete(url)

    assert response.status_code == 404
