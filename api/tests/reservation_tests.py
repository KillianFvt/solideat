from datetime import datetime
from time import sleep

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
def test_restaurant_no_meals(test_user):
    return RestaurantFactory(owner=test_user, available_meals=50)


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


@pytest.mark.django_db
def test_reservationViewSet_create_reservation(api_client, test_user, test_restaurant):
    api_client.force_authenticate(user=test_user)
    response = api_client.post('/api/reservations/', {
        'date': '2022-12-31',
        'time': '12:00:00',
        'restaurant': test_restaurant.id,
        'user': test_user.id
    })
    assert response.status_code == 201
    assert response.data['date'] == '2022-12-31'
    assert response.data['time'] == '12:00:00'
    assert response.data['restaurant'] == test_restaurant.id
    assert response.data['user'] == test_user.id


@pytest.mark.django_db
def test_reservationViewSet_create_reservation_without_required_fields(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    response = api_client.post('/api/reservations/', {
        'date': '2022-12-31',
    })
    assert response.status_code == 400


@pytest.mark.django_db
def test_make_reservation_in_4hours(api_client, test_user, test_restaurant):
    api_client.force_authenticate(user=test_user)

    response = api_client.post('/api/reservations/', {
        'date': str(datetime.now().date()),
        'time': '12:00:00',
        'restaurant': test_restaurant.id,
        'user': test_user.id
    })
    assert response.status_code == 201

    response = api_client.post('/api/reservations/', {
        'date': str(datetime.now().date()),
        'time': '13:00:00',
        'restaurant': test_restaurant.id,
        'user': test_user.id
    })
    assert response.status_code == 403
