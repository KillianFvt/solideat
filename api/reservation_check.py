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

    min_time = (reservation_datetime - timezone.timedelta(hours=4)).time()
    if reservation_datetime.time().hour <= 4:
        min_time = timezone.datetime.strptime('00:00:00', '%H:%M:%S').time()

    max_time = (reservation_datetime + timezone.timedelta(hours=4)).time()
    if reservation_datetime.time().hour >= 20:
        max_time = timezone.datetime.strptime('23:59:59', '%H:%M:%S').time()

    # Check if there is a reservation within 4 hours of the current time
    reservations = reservations.filter(time__range=(min_time, max_time))

    print(min_time)
    print(max_time)

    print(reservations.count())
    print(reservations)

    if reservations.count() > 0:
        return False
    else:
        return True
