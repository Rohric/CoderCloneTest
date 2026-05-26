import pytest
import json
from django.urls import reverse
from offers_app.tests.conftest import UserFactory, OfferFactory


@pytest.mark.django_db
def test_filter_by_creator_id(client):
    user_a = UserFactory(type="business")
    user_b = UserFactory(type="business")

    OfferFactory(user=user_a)
    OfferFactory(user=user_a)
    OfferFactory(user=user_b)

    url = reverse("offer-list")

    response = client.get(url, {"creator_id": user_a.id})
    print(json.dumps(response.json(), indent=2, default=str))

    assert response.status_code == 200
    assert response.data["count"] == 2
    for offer in response.data["results"]:
        assert offer["user"] == user_a.id


@pytest.mark.django_db
def test_filter_by_max_delivery_time(client):
    user_a = UserFactory(type="business")

    offer_1 = OfferFactory(user=user_a)
    offer_1.details.all().update(delivery_time_in_days=5)

    offer_2 = OfferFactory(user=user_a)
    offer_2.details.all().update(delivery_time_in_days=20)

    offer_3 = OfferFactory(user=user_a)
    offer_3.details.all().update(delivery_time_in_days=10)

    url = reverse("offer-list")
    response = client.get(url, {"max_delivery_time": 15})
    print(json.dumps(response.json(), indent=2, default=str))

    assert response.status_code == 200
    assert response.data["count"] == 2
    returned_ids = [offer["id"] for offer in response.data["results"]]
    assert offer_1.id in returned_ids
    assert offer_3.id in returned_ids
    assert offer_2.id not in returned_ids


@pytest.mark.django_db
def test_ordering_by_min_price(client):
    user_a = UserFactory(type="business")

    offer_1 = OfferFactory(user=user_a)
    offer_1.details.all().update(price=300)

    offer_2 = OfferFactory(user=user_a)
    offer_2.details.all().update(price=100)

    offer_3 = OfferFactory(user=user_a)
    offer_3.details.all().update(price=200)

    url = reverse("offer-list")
    response = client.get(url, {"ordering": "min_price"})
    print(json.dumps(response.json(), indent=2, default=str))

    assert response.status_code == 200
    results = response.data["results"]

    assert results[0]["id"] == offer_2.id
    assert results[1]["id"] == offer_3.id
    assert results[2]["id"] == offer_1.id


@pytest.mark.django_db
def test_search(client):
    user_a = UserFactory(type="business")
    user_b = UserFactory(type="business")

    offer_found1 = OfferFactory(user=user_a)
    offer_found1.title = "Django Entwicklung"
    offer_found1.save()

    offer_not_found1 = OfferFactory(user=user_a)
    offer_not_found1.title = "React Frontend"
    offer_not_found1.save()

    offer_found2 = OfferFactory(user=user_a)
    offer_found2.title = "Django DeepDive"
    offer_found2.save()

    offer_not_found2 = OfferFactory(user=user_b)
    offer_not_found2.title = "Angular Frontend"
    offer_not_found2.save()

    offer_found3 = OfferFactory(user=user_b)
    offer_found3.title = "Django Research"
    offer_found3.save()

    url = reverse("offer-list")
    response = client.get(url, {"search": "Django"})
    print(json.dumps(response.json(), indent=2, default=str))

    assert response.status_code == 200
    assert response.data["count"] == 3


@pytest.mark.django_db
def test_filter_by_max_delivery_time_invalid_string(client):
    url = reverse("offer-list")
    response = client.get(url, {"max_delivery_time": "abc"})

    assert response.status_code == 400


@pytest.mark.django_db
def test_filter_by_min_price_invalid_string(client):
    url = reverse("offer-list")
    response = client.get(url, {"min_price": "abc"})

    assert response.status_code == 400


@pytest.mark.django_db
def test_filter_by_creator_id_invalid_string(client):
    url = reverse("offer-list")
    response = client.get(url, {"creator_id": "abc"})

    assert response.status_code == 400


@pytest.mark.django_db
def test_page_size(client):
    user_a = UserFactory(type="business")

    for _ in range(5):
        OfferFactory(user=user_a)

    url = reverse("offer-list")
    response = client.get(url, {"page_size": 2})
    print(json.dumps(response.json(), indent=2, default=str))

    assert response.status_code == 200
    assert response.data["count"] == 5
    assert len(response.data["results"]) == 2
    assert response.data["next"] is not None
