import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_GET_all_orders_as_customer(order_setup, client):
    c1 = order_setup["customers"][0]
    client.force_authenticate(user=c1)

    url = reverse("order-list")
    response = client.get(url)
    print(json.dumps(response.json(), indent=2, default=str))

    assert response.status_code == 200

    ids_in_antwort = [order["id"] for order in response.data]

    assert order_setup["order_in_progress"].id in ids_in_antwort
    assert order_setup["order_completed"].id in ids_in_antwort

    assert order_setup["orders"][2].id not in ids_in_antwort
    assert order_setup["orders"][3].id not in ids_in_antwort


@pytest.mark.django_db
def test_GET_all_orders_as_customer_not_auth(order_setup, client):

    url = reverse("order-list")
    response = client.get(url)

    assert response.status_code == 401
