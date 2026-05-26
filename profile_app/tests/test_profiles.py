import pytest
from django.urls import reverse

from profile_app.models import Profile


@pytest.mark.django_db
def test_get_profile_id(django_user_model, client):
    user = django_user_model.objects.create_user(
        username="max", password="Test1234!", email="max@test.de", type="business"
    )

    Profile.objects.create(
        user=user,
        first_name="Max",
        last_name="Mustermann",
        file="profile.jpg",
        location="Berlin",
        tel="123456789",
        description="Business description",
        working_hours="9-17",
    )

    client.force_authenticate(user=user)

    url = reverse("profile-detail", args=[user.id])
    response = client.get(url)

    assert response.status_code == 200

    assert response.data["user"] == user.id
    assert response.data["username"] == "max"
    assert response.data["first_name"] == "Max"
    assert response.data["last_name"] == "Mustermann"
    assert response.data["file"] == "profile.jpg"
    assert response.data["location"] == "Berlin"
    assert response.data["tel"] == "123456789"
    assert response.data["description"] == "Business description"
    assert response.data["working_hours"] == "9-17"
    assert response.data["type"] == "business"
    assert response.data["email"] == "max@test.de"
    assert "created_at" in response.data


@pytest.mark.django_db
def test_patch_profile_success(client, django_user_model):
    user = django_user_model.objects.create_user(username="max", password="Test1234!", type="customer")

    Profile.objects.create(
        user=user,
        first_name="Max",
    )

    client.force_authenticate(user=user)

    url = reverse("profile-detail", args=[user.id])
    data = {
        "first_name": "Updated",
    }

    response = client.patch(url, data)

    assert response.status_code == 200
    assert response.data["first_name"] == "Updated"


@pytest.mark.django_db
def test_patch_profile_email_update(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="max", password="Test1234!", email="old@test.de", type="business"
    )

    Profile.objects.create(user=user, first_name="Max")

    client.force_authenticate(user=user)

    url = reverse("profile-detail", args=[user.id])
    response = client.patch(url, {"email": "new@test.de"})

    assert response.status_code == 200
    assert response.data["email"] == "new@test.de"

    user.refresh_from_db()
    assert user.email == "new@test.de"


@pytest.mark.django_db
def test_get_profile_not_found(client, django_user_model):
    user = django_user_model.objects.create_user(username="max", password="Test1234!")

    client.force_authenticate(user=user)

    url = reverse("profile-detail", args=[999])
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_get_profile_unauthorized(client, django_user_model):
    user = django_user_model.objects.create_user(username="max", password="Test1234!")

    url = reverse("profile-detail", args=[user.id])
    response = client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_patch_profile_not_allowed(client, django_user_model):
    owner = django_user_model.objects.create_user(
        username="owner", password="Test1234!", type="customer"
    )

    other_user = django_user_model.objects.create_user(
        username="hacker", password="Test1234!", type="customer"
    )

    Profile.objects.create(
        user=owner,
        first_name="Max",
    )

    client.force_authenticate(user=other_user)

    url = reverse("profile-detail", args=[owner.id])
    data = {
        "first_name": "Hacked",
    }

    response = client.patch(url, data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_patch_profile_not_found(client, django_user_model):
    user = django_user_model.objects.create_user(username="max", password="Test1234!")

    client.force_authenticate(user=user)

    url = reverse("profile-detail", args=[999])
    data = {
        "first_name": "Updated",
    }

    response = client.patch(url, data)

    assert response.status_code == 404
