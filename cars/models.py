from django.db import models
from django.contrib.auth.models import User
from common.models import Make, CarModel, BodyType, Feature


class Car(models.Model):
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Benzin'),
        ('diesel', 'Dizel'),
        ('hybrid', 'Gibrid'),
        ('electric', 'Elektro'),
        ('lpg', 'Gaz'),
    ]

    TRANSMISSION_CHOICES = [
        ('manual', 'Mexanika'),
        ('automatic', 'Avtomat'),
        ('semi-auto', 'Yarim avtomat'),
    ]

    DRIVE_TYPE_CHOICES = [
        ('fwd', 'Old g\'ildirak'),
        ('rwd', 'Orqa g\'ildirak'),
        ('awd', 'To\'liq g\'ildirak'),
        ('4wd', '4 g\'ildirak'),
    ]
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    body_type = models.ForeignKey(BodyType, on_delete=models.SET_NULL, null=True)
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPE_CHOICES)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    color = models.CharField(max_length=50)
    mileage = models.PositiveIntegerField()
    engine_size = models.FloatField()
    power = models.PositiveIntegerField()
    drive_type = models.CharField(max_length=5, choices=DRIVE_TYPE_CHOICES)
    features = models.ManyToManyField(Feature, blank=True)
    vin = models.CharField(max_length=17, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make.name} {self.model.name}"

