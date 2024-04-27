import pytest
from rest_framework.test import APIClient
from api.factories import UserFactory, RestaurantFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return UserFactory()


@pytest.fixture
def test_restaurant(test_user):
    return RestaurantFactory(owner=test_user)


@pytest.mark.django_db
def test_restaurantViewSet_get_all_restaurants(api_client, test_restaurant):
    response = api_client.get('/api/restaurants/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == test_restaurant.name


@pytest.mark.django_db
def test_restaurantViewSet_get_single_restaurant(api_client, test_restaurant):
    response = api_client.get(f'/api/restaurants/{test_restaurant.id}/')
    assert response.status_code == 200
    assert response.data['name'] == test_restaurant.name


@pytest.mark.django_db
def test_restaurantViewSet_get_nonexistent_restaurant(api_client):
    response = api_client.get('/api/restaurants/999/')
    assert response.status_code == 404
