import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_POST_order_as_customer(order_setup, authenticated_customer_client):
    client, customer = authenticated_customer_client

    offer = order_setup["offers"][0]
    detail = offer.details.first()

    url = reverse("order-list")
    payload = {"offer_detail_id": detail.id}
    response = client.post(url, payload, format="json")
    print(json.dumps(response.json(), indent=2, default=str))

    assert response.status_code == 201

    assert "id" in response.data
    assert "customer_user" in response.data
    assert "business_user" in response.data
    assert "title" in response.data
    assert "revisions" in response.data
    assert "delivery_time_in_days" in response.data
    assert "price" in response.data
    assert "features" in response.data
    assert "offer_type" in response.data
    assert "status" in response.data
    assert "created_at" in response.data
    assert "updated_at" in response.data

    assert response.data["title"] == detail.title
    assert response.data["offer_type"] == detail.offer_type
    assert int(response.data["revisions"]) == detail.revisions
    assert float(response.data["price"]) == float(detail.price)

    assert response.data["customer_user"] == customer.id

    assert response.data["business_user"] == offer.user.id

    assert response.data["status"] == "in_progress"


@pytest.mark.django_db
def test_POST_order_not_authenticated(client, order_setup):
    detail = order_setup["offers"][0].details.first()

    url = reverse("order-list")
    payload = {"offer_detail_id": detail.id}
    response = client.post(url, payload, format="json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_POST_order_as_business_user(order_setup, authenticated_business_client):
    client, business = authenticated_business_client

    detail = order_setup["offers"][0].details.first()

    url = reverse("order-list")
    payload = {"offer_detail_id": detail.id}
    response = client.post(url, payload, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_POST_order_offer_detail_not_found(authenticated_customer_client):
    client, customer = authenticated_customer_client

    url = reverse("order-list")
    payload = {"offer_detail_id": 99999}
    response = client.post(url, payload, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_POST_order_missing_offer_detail_id(authenticated_customer_client):
    client, customer = authenticated_customer_client

    url = reverse("order-list")
    payload = {}
    response = client.post(url, payload, format="json")

    assert response.status_code == 400
