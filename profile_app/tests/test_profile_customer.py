import pytest
from django.urls import reverse

from profile_app.models import Profile


@pytest.mark.django_db
def test_get_customer_profiles(client, django_user_model):
    viewer = django_user_model.objects.create_user(
        username="viewer", password="Test1234!"
    )
    user1 = django_user_model.objects.create_user(
        username="cust1", password="Test1234!", email="cust1@test.de", type="customer"
    )
    user2 = django_user_model.objects.create_user(
        username="cust2", password="Test1234!", email="cust2@test.de", type="customer"
    )
    user3 = django_user_model.objects.create_user(
        username="biz1", password="Test1234!", email="biz@test.de", type="business"
    )

    Profile.objects.create(user=user1, first_name="Cust1")
    Profile.objects.create(user=user2, first_name="Cust2")
    Profile.objects.create(user=user3, first_name="Biz1")

    client.force_authenticate(user=viewer)

    url = reverse("profile-customer-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2

    types = [item["type"] for item in response.data]
    assert all(t == "customer" for t in types)


@pytest.mark.django_db
def test_get_customer_profiles_unauthorized(client):
    url = reverse("profile-customer-list")

    response = client.get(url)

    assert response.status_code == 401
