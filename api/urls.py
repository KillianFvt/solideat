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
]
