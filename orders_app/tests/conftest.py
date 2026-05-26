import random

import factory
import factory.django
import pytest
from rest_framework.test import APIClient

from offers_app.tests.conftest import OfferFactory, UserFactory


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "orders_app.Order"

    customer_user = factory.SubFactory(UserFactory, type="customer")
    business_user = factory.SubFactory(UserFactory, type="business")

    offer_detail = None

    title = factory.Sequence(lambda n: f"Logo Design {n}")
    revisions = factory.LazyFunction(lambda: random.choice([1, 2, 3, 5, 10]))
    delivery_time_in_days = factory.LazyFunction(lambda: random.choice([3, 5, 7, 10, 14]))
    price = factory.LazyFunction(lambda: random.choice([50, 100, 150, 200, 300, 500]))
    features = factory.LazyFunction(lambda: ["Logo Design"])
    offer_type = factory.LazyFunction(lambda: random.choice(["basic", "standard", "premium"]))
    status = "in_progress"


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def order_setup(db):
    b1 = UserFactory(type="business")
    b2 = UserFactory(type="business")
    b3 = UserFactory(type="business")

    c1 = UserFactory(type="customer")
    c2 = UserFactory(type="customer")

    offer_b1_1 = OfferFactory(user=b1)
    offer_b1_2 = OfferFactory(user=b1)
    offer_b2_1 = OfferFactory(user=b2)
    offer_b2_2 = OfferFactory(user=b2)
    offer_b3_1 = OfferFactory(user=b3)
    offer_b3_2 = OfferFactory(user=b3)

    d_b1_1 = offer_b1_1.details.first()
    d_b1_2 = offer_b1_2.details.first()
    d_b2_1 = offer_b2_1.details.first()
    d_b2_2 = offer_b2_2.details.first()
    d_b3_1 = offer_b3_1.details.first()
    d_b3_2 = offer_b3_2.details.first()

    def make_order(customer, business, detail, status):
        return OrderFactory(
            customer_user=customer,
            business_user=business,
            offer_detail=detail,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status=status,
        )

    order_1 = make_order(c1, b1, d_b1_1, "in_progress")
    order_2 = make_order(c1, b1, d_b1_2, "completed")
    order_3 = make_order(c2, b2, d_b2_1, "in_progress")
    order_4 = make_order(c2, b2, d_b2_2, "cancelled")
    order_5 = make_order(c1, b3, d_b3_1, "in_progress")
    order_6 = make_order(c2, b3, d_b3_2, "completed")

    return {
        "business_users": [b1, b2, b3],
        "customers": [c1, c2],
        "offers": [offer_b1_1, offer_b1_2, offer_b2_1, offer_b2_2, offer_b3_1, offer_b3_2],
        "orders": [order_1, order_2, order_3, order_4, order_5, order_6],
        "order_in_progress": order_1,
        "order_completed": order_2,
        "order_cancelled": order_4,
    }


@pytest.fixture
def authenticated_customer_client(db):
    user = UserFactory(type="customer")
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def authenticated_business_client(db):
    user = UserFactory(type="business")
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client, user
