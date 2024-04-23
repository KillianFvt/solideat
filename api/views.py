from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

from .reservation_check import reservation_checker
from .serializers import *


@api_view(['GET'])
def index(request):
    return Response({"message": "API root"})


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantImageViewSet(viewsets.ModelViewSet):
    queryset = RestaurantImage.objects.all()
    serializer_class = RestaurantImageSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


@csrf_exempt
@api_view(['POST'])
def make_reservation(request):
    """
    This view makes a reservation
    It has several checks to ensure that a user can make a reservation
    User has to be authenticated

    :param request: WSGI request object
    :return: Response object
    """
    data = request.data
    user = request.user

    if request.user.is_anonymous:
        return Response({"error": "User is not authenticated"}, status=400)

    date = data.get('date')
    time = data.get('time')
    str_datetime = f"{date} {time}"
    if len(str(time)) == 5:
        str_datetime = f"{date} {time}:00"

    reservation_datetime = datetime.strptime(str_datetime, '%Y-%m-%d %H:%M:%S')

    if not reservation_checker(user.id, reservation_datetime):
        return Response({"error": "Reservation not allowed"}, status=403)

    restaurant_id = data.get('restaurant_id')

    restaurant = Restaurant.objects.get(id=restaurant_id)

    if restaurant.available_meals > 0:
        new_reservation = Reservation.objects.create(
            restaurant=restaurant,
            user=user,
            date=date,
            time=time
        )
        new_reservation.save()

        restaurant.available_meals -= 1
        restaurant.save()
    else:
        return Response({"error": "No more available meals"}, status=400)

    return Response({"message": "Make a reservation"}, status=201)


@csrf_exempt
@api_view(['GET'])
def get_user_reservations(request):
    """
    This view gets all reservations for the current user

    :param request: WSGI request object
    :return: Response object
    """
    user = request.user

    if user.is_anonymous:
        return Response({"error": "User is not authenticated"}, status=400)

    reservations = Reservation.objects.filter(user=user)

    return Response({
        "reservations": ReservationSerializer(reservations, many=True).data
    })


@csrf_exempt
@api_view(['GET'])
def get_restaurant_reservations(request):
    """
    This view gets all reservations for the current restaurant owner
    :param request: WSGI request object
    :return: Response object
    """
    user = request.user

    if user.is_anonymous:
        return Response({"error": "User is not authenticated"}, status=400)

    if user.groups.filter(name='RestaurantOwners').exists():
        reservations = Reservation.objects.filter(restaurant__owner=user)

        return Response({
            "reservations": ReservationSerializer(reservations, many=True).data
        })

    else:
        return Response({"error": "User is not a restaurant owner"}, status=400)
