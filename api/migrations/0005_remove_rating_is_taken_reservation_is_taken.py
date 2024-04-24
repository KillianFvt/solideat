# Generated by Django 5.0.4 on 2024-04-22 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rating_is_taken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='is_taken',
        ),
        migrations.AddField(
            model_name='reservation',
            name='is_taken',
            field=models.BooleanField(default=False),
        ),
    ]
