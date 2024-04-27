import pytest
from rest_framework.test import APIClient
from api.factories import UserFactory, RestaurantFactory, ReservationFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return UserFactory()


@pytest.fixture
def test_restaurant(test_user):
    return RestaurantFactory(owner=test_user)


@pytest.fixture
def test_reservation(test_user, test_restaurant):
    return ReservationFactory(user=test_user, restaurant=test_restaurant)


@pytest.mark.django_db
def test_reservationViewSet_get_all_reservations(api_client, test_reservation):
    response = api_client.get('/api/reservations/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == test_reservation.id


@pytest.mark.django_db
def test_reservationViewSet_get_single_reservation(api_client, test_reservation):
    response = api_client.get(f'/api/reservations/{test_reservation.id}/')
    assert response.status_code == 200
    assert response.data['id'] == test_reservation.id


@pytest.mark.django_db
def test_reservationViewSet_get_nonexistent_reservation(api_client):
    response = api_client.get('/api/reservations/654655646/')
    assert response.status_code == 404
