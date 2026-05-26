from pprint import pprint
import json

import pytest
from django.urls import reverse

from offers_app.tests.conftest import OfferFactory, UserFactory


@pytest.mark.django_db
def test_GET_all_offers(client):
    user = UserFactory(type="business")

    OfferFactory(user=user)

    url = reverse("offer-list")
    response = client.get(url)
    assert response.status_code == 200

    assert "count" in response.data
    assert "results" in response.data

    assert response.data["count"] == 1


@pytest.mark.django_db
def test_create_offer_success(authenticated_business_client):
    client, user = authenticated_business_client

    url = reverse("offer-list")

    payload = {
        "title": "Grafikdesign-Paket",
        "description": "Ein professionelles Paket.",
        "details": [
            {
                "title": "Basic Design",
                "revisions": 2,
                "delivery_time_in_days": 5,
                "price": 100,
                "features": ["Logo Design"],
                "offer_type": "basic",
            },
            {
                "title": "Standard Design",
                "revisions": 5,
                "delivery_time_in_days": 7,
                "price": 200,
                "features": ["Logo Design", "Visitenkarte"],
                "offer_type": "standard",
            },
            {
                "title": "Premium Design",
                "revisions": 10,
                "delivery_time_in_days": 10,
                "price": 500,
                "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                "offer_type": "premium",
            },
        ],
    }

    response = client.post(url, payload, format="json")
    pprint(response.json())

    assert response.status_code == 201
    assert response.data["title"] == "Grafikdesign-Paket"
    assert response.data["user"] == user.id
    assert len(response.data["details"]) == 3
    assert "min_price" in response.data
    assert "min_delivery_time" in response.data

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
def test_get_offer_by_id(authenticated_business_client):
    client, user = authenticated_business_client

    offer_1 = OfferFactory(user=user)
    offer_2 = OfferFactory(user=user)

    url = reverse("offer-detail", args=[offer_1.id])
    response = client.get(url)
    print(json.dumps(response.json(), indent=2, default=str))

    assert response.status_code == 200

    assert response.data["id"] == offer_1.id
    assert response.data["title"] == offer_1.title
    assert len(response.data["details"]) == 3
    assert "min_price" in response.data
    assert "min_delivery_time" in response.data
    assert "user_details" in response.data

    assert response.data["id"] != offer_2.id
