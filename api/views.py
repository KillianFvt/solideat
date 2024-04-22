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

    def get_queryset(self):
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')

        if lat and lng:
            return Restaurant.objects.filter(
                lat__range=(float(lat) - 0.1, float(lat) + 0.1),
                lng__range=(float(lng) - 0.1, float(lng) + 0.1)
            )
            return
        else:
            return Rating.objects.all()


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

    if user.is_anonymous:
        return Response({"error": "User is not authenticated"}, status=400)

    reservations = Reservation.objects.filter(user=user)

    return Response({
        "reservations": ReservationSerializer(reservations, many=True).data
    })


@csrf_exempt
@api_view(['GET'])
def get_restaurant_reservations(request):
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
