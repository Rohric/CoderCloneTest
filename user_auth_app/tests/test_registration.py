import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register_customer_success(client):
    url = reverse("registration")

    data = {
        "username": "cust",
        "email": "cust@test.de",
        "password": "Test1234!",
        "repeated_password": "Test1234!",
        "type": "customer",
    }

    response = client.post(url, data)

    assert response.status_code == 201
    assert "token" in response.data
    assert response.data["username"] == "cust"
    assert response.data["email"] == "cust@test.de"
    assert "user_id" in response.data


@pytest.mark.django_db
def test_register_business_success(client):
    url = reverse("registration")

    data = {
        "username": "biz",
        "email": "biz@test.de",
        "password": "Test1234!",
        "repeated_password": "Test1234!",
        "type": "business",
    }

    response = client.post(url, data)

    assert response.status_code == 201
    assert "token" in response.data
    assert response.data["username"] == "biz"
    assert response.data["email"] == "biz@test.de"
    assert "user_id" in response.data


@pytest.mark.django_db
def test_register_missing_type(client):
    url = reverse("registration")

    data = {
        "username": "fail",
        "email": "fail@test.de",
        "password": "Test1234!",
        "repeated_password": "Test1234!",
    }

    response = client.post(url, data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_password_mismatch(client):
    url = reverse("registration")

    data = {
        "username": "fail",
        "email": "fail@test.de",
        "password": "Test1234!",
        "repeated_password": "DIFFERENT",
        "type": "customer",
    }

    response = client.post(url, data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_invalid_email(client):
    url = reverse("registration")

    data = {
        "username": "fail",
        "email": "failtest.de",
        "password": "Test1234!",
        "repeated_password": "Test1234!",
        "type": "customer",
    }

    response = client.post(url, data)

    assert response.status_code == 400
