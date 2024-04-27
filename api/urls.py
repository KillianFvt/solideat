from django.urls import path, include
from . import views
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('restaurants', RestaurantViewSet)
router.register('images', RestaurantImageViewSet)
router.register('reservations', ReservationViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', views.index, name='api-root'),
    path('', include(router.urls)),
    path('reservation/new/', views.make_reservation, name='make-reservation'),
    path('reservation/get-user-reservations/', views.get_user_reservations, name='get-user-reservations'),
    path('reservation/get-restaurant-reservations/', views.get_restaurant_reservations, name='get-restaurant-reservations'),
    path('review/new/', views.make_review, name='make-review'),
    path('review/avg/<int:restaurant_id>/', views.get_restaurant_rating_avg, name='get-avg-rating'),
]
