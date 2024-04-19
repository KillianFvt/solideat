from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
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
    data = request.data
    user = request.user

    date = data.get('date')
    time = data.get('time')
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
    user = request.user
    reservations = Reservation.objects.filter(user=user)

    return Response({
        "reservations": ReservationSerializer(reservations, many=True).data
    })
