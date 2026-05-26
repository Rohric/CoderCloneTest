import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from offers_app.tests.conftest import UserFactory


@pytest.mark.django_db
def test_DELETE_order_as_admin(order_setup):
    admin = UserFactory(type="business")
    admin.is_staff = True
    admin.save()

    order = order_setup["order_in_progress"]

    client = APIClient()
    client.force_authenticate(user=admin)

    url = reverse("order-detail", args=[order.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert response.data is None


@pytest.mark.django_db
def test_DELETE_order_not_authenticated(client, order_setup):
    order = order_setup["order_in_progress"]

    url = reverse("order-detail", args=[order.id])
    response = client.delete(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_DELETE_order_as_customer_forbidden(order_setup, authenticated_customer_client):
    client, customer = authenticated_customer_client

    order = order_setup["order_in_progress"]

    url = reverse("order-detail", args=[order.id])
    response = client.delete(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_DELETE_order_as_business_forbidden(order_setup):
    business = order_setup["business_users"][0]
    order = order_setup["order_in_progress"]

    client = APIClient()
    client.force_authenticate(user=business)

    url = reverse("order-detail", args=[order.id])
    response = client.delete(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_DELETE_order_not_found(order_setup):
    admin = UserFactory(type="business")
    admin.is_staff = True
    admin.save()

    client = APIClient()
    client.force_authenticate(user=admin)

    url = reverse("order-detail", args=[99999])
    response = client.delete(url)

    assert response.status_code == 404
