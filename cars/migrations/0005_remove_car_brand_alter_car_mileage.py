# Generated by Django 5.2 on 2025-04-25 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_alter_car_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='brand',
        ),
        migrations.AlterField(
            model_name='car',
            name='mileage',
            field=models.IntegerField(default=0),
        ),
    ]
