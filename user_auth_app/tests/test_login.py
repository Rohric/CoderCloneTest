import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
def test_login_user(client):
    url = reverse("login")

    User.objects.create_user(
        username="cust", email="cust@test.de", password="Test1234!"
    )

    data = {
        "username": "cust",
        "password": "Test1234!",
    }

    response = client.post(url, data)

    assert response.status_code == 200
    assert "token" in response.data
    assert response.data["username"] == "cust"
    assert "email" in response.data
    assert "user_id" in response.data


@pytest.mark.django_db
def test_login_invalid_username(client):
    url = reverse("login")

    User.objects.create_user(
        username="cust", email="cust@test.de", password="Test1234!"
    )

    data = {
        "username": "WRONG",
        "password": "Test1234!",
    }

    response = client.post(url, data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_invalid_password(client):
    url = reverse("login")

    User.objects.create_user(
        username="cust", email="cust@test.de", password="Test1234!"
    )

    data = {
        "username": "cust",
        "password": "WRONG",
    }

    response = client.post(url, data)

    assert response.status_code == 400
