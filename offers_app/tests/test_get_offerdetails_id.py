import json

import pytest
from django.urls import reverse

from offers_app.tests.conftest import OfferFactory


@pytest.mark.django_db
def test_get_offer_item_by_id(authenticated_business_client):
    client, user = authenticated_business_client

    offer_1 = OfferFactory(user=user)
    offer_2 = OfferFactory(user=user)

    detail = offer_2.details.get(offer_type="premium")
    url = reverse("offerdetail-detail", args=[detail.id])
    response = client.get(url)
    print(json.dumps(response.json(), indent=2, default=str))

    assert response.status_code == 200
    assert response.data["id"] == detail.id
    assert response.data["offer_type"] == "premium"
    assert "title" in response.data
    assert "revisions" in response.data
    assert "delivery_time_in_days" in response.data
    assert "price" in response.data
    assert "features" in response.data


@pytest.mark.django_db
def test_get_offer_item_not_found(authenticated_business_client):
    client, user = authenticated_business_client

    url = reverse("offerdetail-detail", args=[999])
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_get_offer_item_user_not_auth(client):
    offer = OfferFactory()
    detail = offer.details.first()

    url = reverse("offerdetail-detail", args=[detail.id])
    response = client.get(url)

    assert response.status_code == 401
