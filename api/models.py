from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    coordinates = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=False, null=False)
    postal_code = models.CharField(max_length=10, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    phone = models.CharField(max_length=100, blank=True, null=True)
    can_takeout = models.BooleanField(default=False, blank=False, null=False)
    can_dine_in = models.BooleanField(default=False, blank=False, null=False)
    schedule = models.CharField(max_length=100, blank=True, null=True)

    available_meals = models.IntegerField(blank=False, null=False, default=0)
    available_meals_max = models.IntegerField(blank=False, null=False, default=0)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.address}, {self.postal_code}, {self.city}"


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_images')

    def __str__(self):
        return f"{self.restaurant.name} - {self.image}"


class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_taken = models.BooleanField(default=False, null=False, blank=False)


class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=False, null=False)
    comment = models.TextField(blank=True, null=True, max_length=250)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.rating} by {self.user.username}"
