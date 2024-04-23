from django.utils import timezone
from api.models import Reservation
from django.contrib.auth.models import User


def reservation_checker(user_id, reservation_datetime):
    """
    This function checks if a user can make a reservation

    If a user has already made 2 reservations for the same day, they cannot make another reservation
    If a user has already made a reservation within 4 hours of the current time, they cannot make another reservation

    :param user_id:
    :param reservation_datetime:
    :return:
    """

    # Get all reservations for the user on the same day
    user = User.objects.get(id=user_id)
    reservations = Reservation.objects.filter(user=user)
    reservations = reservations.filter(date=reservation_datetime.date())

    # Check if the user has already made 2 reservations for the same day
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
