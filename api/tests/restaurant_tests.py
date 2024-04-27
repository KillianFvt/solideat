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


@pytest.mark.django_db
def test_restaurantViewSet_create_restaurant(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    response = api_client.post('/api/restaurants/', {
        'name': 'Test Restaurant',
        'address': '123 Test St',
        'postal_code': '12345',
        'city': 'Test City',
        'owner': test_user.id
    })
    assert response.status_code == 201
    assert response.data['name'] == 'Test Restaurant'
    assert response.data['address'] == '123 Test St'
    assert response.data['postal_code'] == '12345'
    assert response.data['city'] == 'Test City'
    assert response.data['owner'] == test_user.id


@pytest.mark.django_db
def test_restaurantViewSet_create_restaurant_without_required_fields(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    response = api_client.post('/api/restaurants/', {
        'name': 'Test Restaurant',
    })
    assert response.status_code == 400


@pytest.mark.django_db
def test_restaurantViewSet_create_restaurant_without_required_fields(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    response = api_client.post('/api/restaurants/', {
        'name': 'Test Restaurant',
    })
    assert response.status_code == 400
