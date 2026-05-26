import json
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_PATCH_order_status_as_business(order_setup):
    from rest_framework.test import APIClient

    order = order_setup["order_in_progress"]
    business = order_setup["business_users"][0]

    client = APIClient()
    client.force_authenticate(user=business)

    url = reverse("order-detail", args=[order.id])
    payload = {"status": "completed"}
    response = client.patch(url, payload, format="json")
    print(json.dumps(response.json(), indent=2, default=str))

    assert response.status_code == 200
    assert response.data["status"] == "completed"

    # Response must contain the full order object, not just status
    assert "id" in response.data
    assert "customer_user" in response.data
    assert "business_user" in response.data
    assert "title" in response.data
    assert "price" in response.data


@pytest.mark.django_db
def test_PATCH_order_not_authenticated(client, order_setup):
    order = order_setup["order_in_progress"]

    url = reverse("order-detail", args=[order.id])
    payload = {"status": "completed"}
    response = client.patch(url, payload, format="json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_PATCH_order_as_customer_forbidden(order_setup, authenticated_customer_client):
    client, customer = authenticated_customer_client

    order = order_setup["order_in_progress"]

    url = reverse("order-detail", args=[order.id])
    payload = {"status": "completed"}
    response = client.patch(url, payload, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_PATCH_order_as_wrong_business(order_setup):
    from rest_framework.test import APIClient

    order = order_setup["order_in_progress"]
    wrong_business = order_setup["business_users"][1]

    client = APIClient()
    client.force_authenticate(user=wrong_business)

    url = reverse("order-detail", args=[order.id])
    payload = {"status": "completed"}
    response = client.patch(url, payload, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_PATCH_order_not_found(order_setup):
    from rest_framework.test import APIClient

    business = order_setup["business_users"][0]

    client = APIClient()
    client.force_authenticate(user=business)

    url = reverse("order-detail", args=[99999])
    payload = {"status": "completed"}
    response = client.patch(url, payload, format="json")

    assert response.status_code == 404


@pytest.mark.django_db
def test_PATCH_order_invalid_status(order_setup):
    from rest_framework.test import APIClient

    order = order_setup["order_in_progress"]
    business = order_setup["business_users"][0]

    client = APIClient()
    client.force_authenticate(user=business)

    url = reverse("order-detail", args=[order.id])
    payload = {"status": "fertig"}
    response = client.patch(url, payload, format="json")

    assert response.status_code == 400
