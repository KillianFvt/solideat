import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Restaurant


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def test_restaurant(test_user):
    return Restaurant.objects.create(
        name='Test Restaurant',
        address='123 Test St',
        postal_code='12345',
        city='Test City',
        owner=test_user
    )


@pytest.mark.django_db
def restaurantViewSet_get_all_restaurants(api_client, test_restaurant):
    response = api_client.get('/api/restaurants/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Restaurant'


@pytest.mark.django_db
def restaurantViewSet_get_single_restaurant(api_client, test_restaurant):
    response = api_client.get(f'/api/restaurants/{test_restaurant.id}/')
    assert response.status_code == 200
    assert response.data['name'] == 'Test Restaurant'


def restaurantViewSet_get_nonexistent_restaurant(api_client):
    response = api_client.get('/api/restaurants/999/')
    assert response.status_code == 404
