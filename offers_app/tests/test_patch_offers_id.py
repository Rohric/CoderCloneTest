import json

import pytest
from django.urls import reverse

from offers_app.tests.conftest import OfferFactory, UserFactory


@pytest.mark.django_db
def test_patch_offer_success(authenticated_business_client):
    client, user = authenticated_business_client

    offer = OfferFactory(user=user)
    basic_detail = offer.details.get(offer_type="basic")

    url = reverse("offer-detail", args=[offer.id])
    data = {
        "title": "Updated Grafikdesign-Paket",
        "details": [
            {
                "title": "Basic Design Updated",
                "revisions": 3,
                "delivery_time_in_days": 6,
                "price": 120,
                "features": ["Logo Design", "Flyer"],
                "offer_type": "basic",
            }
        ],
    }
    response = client.patch(url, data, format="json")
    print(json.dumps(response.json(), indent=2, default=str))
    assert response.status_code == 200
    assert response.data["title"] == "Updated Grafikdesign-Paket"

    updated_basic = offer.details.get(offer_type="basic")
    assert updated_basic.id == basic_detail.id
    assert updated_basic.price == 120

    assert "id" in response.data
    assert "user" in response.data
    assert "description" in response.data
    assert "details" in response.data
    assert "min_price" in response.data
    assert "min_delivery_time" in response.data
    assert "user_details" in response.data

    # Details must be full objects, not just links
    first_detail = response.data["details"][0]
    assert "title" in first_detail
    assert "revisions" in first_detail
    assert "delivery_time_in_days" in first_detail
    assert "price" in first_detail
    assert "features" in first_detail
    assert "offer_type" in first_detail
    assert "url" not in first_detail


@pytest.mark.django_db
def test_patch_offer_invalid_offer_type(authenticated_business_client):
    client, user = authenticated_business_client

    offer = OfferFactory(user=user)

    url = reverse("offer-detail", args=[offer.id])
    data = {
        "title": "Updated Grafikdesign-Paket",
        "details": [
            {
                "title": "Basic Design Updated",
                "revisions": 3,
                "delivery_time_in_days": 6,
                "price": 120,
                "features": ["Logo Design", "Flyer"],
                "offer_type": "",
            }
        ],
    }
    response = client.patch(url, data, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_patch_offer_user_not_auth(client):

    offer = OfferFactory()

    url = reverse("offer-detail", args=[offer.id])
    data = {
        "title": "Updated Grafikdesign-Paket",
        "details": [
            {
                "title": "Basic Design Updated",
                "revisions": 3,
                "delivery_time_in_days": 6,
                "price": 120,
                "features": ["Logo Design", "Flyer"],
                "offer_type": "basic",
            }
        ],
    }
    response = client.patch(url, data, format="json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_patch_offer_user_not_owner(client):
    user_a = UserFactory(type="business")
    user_b = UserFactory(type="business")
    offer_1 = OfferFactory(user=user_a)
    client.force_authenticate(user=user_b)
    url = reverse("offer-detail", args=[offer_1.id])
    data = {
        "title": "Updated Grafikdesign-Paket",
        "details": [
            {
                "title": "Basic Design Updated",
                "revisions": 3,
                "delivery_time_in_days": 6,
                "price": 120,
                "features": ["Logo Design", "Flyer"],
                "offer_type": "basic",
            }
        ],
    }
    response = client.patch(url, data, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_patch_offer_not_found(authenticated_business_client):
    client, user = authenticated_business_client

    url = reverse("offer-detail", args=[20])
    response = client.patch(url, {}, format="json")

    assert response.status_code == 404
