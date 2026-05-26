import factory
import pytest
from rest_framework.test import APIClient


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "user_auth_app.User"

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@test.de")
    password = factory.PostGenerationMethodCall("set_password", "Test1234!")
    type = "customer"

    class Params:
        business = factory.Trait(type="business")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile_app.Profile"

    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    location = ""
    tel = ""
    description = ""
    working_hours = ""


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def business_user(db):
    return UserFactory(business=True)


@pytest.fixture
def customer_user(db):
    return UserFactory()


@pytest.fixture
def business_profile(db):
    return ProfileFactory(user=UserFactory(business=True))
