import factory
from api.models import *
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@test.com")


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant

    name = factory.Sequence(lambda n: f"Restaurant{n}")
    address = factory.Faker('address')
    postal_code = factory.Faker('postcode')
    city = factory.Faker('city')
    owner = factory.SubFactory(UserFactory)


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation

    date = factory.Faker('future_date')
    time = factory.Faker('time')
    is_taken = factory.Faker('boolean')
    restaurant = factory.SubFactory(RestaurantFactory)
    user = factory.SubFactory(UserFactory)


class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rating

    rating = factory.Iterator([1, 2, 3, 4, 5])
    comment = factory.Faker('sentence')
    restaurant = factory.SubFactory(RestaurantFactory)
    user = factory.SubFactory(UserFactory)