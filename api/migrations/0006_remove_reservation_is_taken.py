# Generated by Django 5.0.4 on 2024-04-22 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_rating_is_taken_reservation_is_taken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='is_taken',
        ),
    ]
