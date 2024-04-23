from django.utils import timezone

from api.models import Reservation
from django.contrib.auth.models import User


def reservation_checker(user_id, reservation_datetime):

    user = User.objects.get(id=user_id)
    reservations = Reservation.objects.filter(user=user)
    reservations = reservations.filter(date=reservation_datetime.date())

    if reservations.count() > 1:
        return False

    # Check if there is a reservation within 4 hours of the current time
    reservations = reservations.filter(time__range=(
        (reservation_datetime - timezone.timedelta(hours=4)).time(),
        (reservation_datetime + timezone.timedelta(hours=4)).time(),
    ))

    if reservations.count() > 0:
        return False
    else:
        return True
