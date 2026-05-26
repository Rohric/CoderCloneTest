import json

import pytest
from django.urls import reverse

from offers_app.tests.conftest import OfferFactory

VALID_PAYLOAD = {
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


@pytest.mark.django_db
def test_not_auth(client):
    url = reverse("offer-list")
    response = client.post(url, VALID_PAYLOAD, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_not_business_write_offer(authenticated_customer_client):
    client, user = authenticated_customer_client
    url = reverse("offer-list")
    response = client.post(url, VALID_PAYLOAD, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_missing_details(authenticated_business_client):
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
        ],
    }

    response = client.post(url, payload, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_offer_by_id_not_auth(client):
    offer = OfferFactory()

    url = reverse("offer-detail", args=[offer.id])
    response = client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_get_offer_by_id_not_found(authenticated_business_client):
    client, user = authenticated_business_client

    offer_1 = OfferFactory(user=user)
    offer_2 = OfferFactory(user=user)

    not_existing_id = 3
    assert not_existing_id != offer_1.id
    assert not_existing_id != offer_2.id

    url = reverse("offer-detail", args=[not_existing_id])
    response = client.get(url)
    print(json.dumps(response.json(), indent=2, default=str))

    assert response.status_code == 404
