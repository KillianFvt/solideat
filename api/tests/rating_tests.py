import pytest
from rest_framework.test import APIClient
from api.factories import UserFactory, RestaurantFactory, RatingFactory


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
def test_rating(test_user, test_restaurant):
    return RatingFactory(user=test_user, restaurant=test_restaurant)


@pytest.mark.django_db
def test_ratingViewSet_get_all_ratings(api_client, test_rating):
    response = api_client.get('/api/ratings/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == test_rating.id


@pytest.mark.django_db
def test_ratingViewSet_get_single_rating(api_client, test_rating):
    response = api_client.get(f'/api/ratings/{test_rating.id}/')
    assert response.status_code == 200
    assert response.data['id'] == test_rating.id


@pytest.mark.django_db
def test_ratingViewSet_get_nonexistent_rating(api_client):
    response = api_client.get('/api/ratings/55545646/')
    assert response.status_code == 404
