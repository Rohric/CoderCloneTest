import factory
import factory.django
import pytest
from rest_framework.test import APIClient


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "user_auth_app.User"
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@test.de")
    password = factory.PostGenerationMethodCall("set_password", "Test1234!")
    type = "customer"

    class Params:
        business = factory.Trait(type="business")

    @factory.post_generation
    def profile(self, create, extracted, **kwargs):
        if not create:
            return
        from profile_app.models import Profile
        from faker import Faker

        fake = Faker("de_DE")

        Profile.objects.get_or_create(
            user=self,
            defaults={
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
            },
        )


class OfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "offers_app.Offer"
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory, type="business")

    title = factory.Sequence(lambda n: f"Angebot {n}")
    description = "Eine professionelle Test-Dienstleistung."
    image = None

    @factory.post_generation
    def details(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for detail in extracted:
                detail.offer = self
                detail.save()
        else:
            OfferDetailFactory(
                offer=self,
                title="Basic Paket",
                revisions=2,
                delivery_time_in_days=5,
                price=100,
                features=["Logo Design"],
                offer_type="basic",
            )
            OfferDetailFactory(
                offer=self,
                title="Standard Paket",
                revisions=5,
                delivery_time_in_days=7,
                price=200,
                features=["Logo Design", "Visitenkarte"],
                offer_type="standard",
            )
            OfferDetailFactory(
                offer=self,
                title="Premium Paket",
                revisions=10,
                delivery_time_in_days=10,
                price=500,
                features=["Logo Design", "Visitenkarte", "Briefpapier"],
                offer_type="premium",
            )


class OfferDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "offers_app.OfferDetail"

    offer = factory.SubFactory("offers_app.tests.conftest.OfferFactory")

    title = factory.Sequence(lambda n: f"Paket {n}")
    revisions = 2
    delivery_time_in_days = 5
    price = factory.Sequence(lambda n: 100 + n * 50)

    features = ["Logo Design", "Visitenkarte"]

    offer_type = "basic"


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def business_user(db):
    return UserFactory(type="business")


@pytest.fixture
def customer_user(db):
    return UserFactory(type="customer")


@pytest.fixture
def offer(db):
    return OfferFactory()


@pytest.fixture
def authenticated_business_client(db):
    user = UserFactory(type="business")
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def authenticated_customer_client(db):
    user = UserFactory(type="customer")
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user
