import pytest
from django.urls import reverse

from profile_app.models import Profile


@pytest.mark.django_db
def test_get_business_profiles(client, django_user_model):
    viewer = django_user_model.objects.create_user(
        username="viewer", password="Test1234!"
    )

    biz_user = django_user_model.objects.create_user(
        username="biz", password="Test1234!", type="business"
    )

    Profile.objects.create(
        user=biz_user,
        first_name="Max",
        last_name="Mustermann",
        file="profile_picture.jpg",
        location="Berlin",
        tel="123456789",
        description="Business description",
        working_hours="9-17",
    )

    client.force_authenticate(user=viewer)

    url = reverse("profile-business-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1

    data = response.data[0]

    assert data["user"] == biz_user.id
    assert data["username"] == "biz"
    assert data["first_name"] == "Max"
    assert data["last_name"] == "Mustermann"
    assert data["file"] == "profile_picture.jpg"
    assert data["location"] == "Berlin"
    assert data["tel"] == "123456789"
    assert data["description"] == "Business description"
    assert data["working_hours"] == "9-17"
    assert data["type"] == "business"


@pytest.mark.django_db
def test_get_business_profiles_unauthorized(client):
    url = reverse("profile-business-list")

    response = client.get(url)

    assert response.status_code == 401
