import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_GET_completed_order_count_authenticated(order_setup, authenticated_customer_client):
    client, _ = authenticated_customer_client
    b1 = order_setup["business_users"][0]

    url = reverse("completed-order-count", kwargs={"business_user_id": b1.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["completed_order_count"] == 1


@pytest.mark.django_db
def test_GET_completed_order_count_not_auth(order_setup, client):
    b1 = order_setup["business_users"][0]

    url = reverse("completed-order-count", kwargs={"business_user_id": b1.pk})
    response = client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_GET_completed_order_count_business_user_not_found(order_setup, authenticated_customer_client):
    client, _ = authenticated_customer_client

    url = reverse("completed-order-count", kwargs={"business_user_id": 9999})
    response = client.get(url)

    assert response.status_code == 404
