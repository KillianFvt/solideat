import csv
import random

from api.models import Restaurant


def get_gouv_data():
    with open('restaurants-casvp.csv', newline='') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')

        headers = spamreader.__next__()

        for row in spamreader:
            postal_code = row[0]
            name = string_capitalize(row[1])
            address = string_capitalize(row[2].replace(',', ''))
            city = string_capitalize(row[3])
            coordinates = row[4]
            can_takeout = random.choice([True, False])
            can_dine_in = random.choice([True, False])
            available_meals = random.randint(5, 50)
            available_meals_max = available_meals

            new_restaurant = Restaurant.objects.create(
                name=name,
                coordinates=coordinates,
                address=address,
                postal_code=postal_code,
                city=city,
                can_takeout=can_takeout,
                can_dine_in=can_dine_in,
                available_meals=available_meals,
                available_meals_max=available_meals_max,
                owner_id=1
            )

            new_restaurant.save()


def string_capitalize(string):
    result = ''
    string = string.replace("'", " ' ")
    words = string.split(' ')
    for word in words:
        result += word.capitalize() + ' '

    result = result.strip().replace(" ' ", "'")
    return result
