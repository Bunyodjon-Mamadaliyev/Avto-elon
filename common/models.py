from django.db import models

class Make(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='make_logos/')

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=50)
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name='models')

    def __str__(self):
        return f"{self.make.name} {self.name}"


class BodyType(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='body_types/', null=True, blank=True)

    def __str__(self):
        return self.name


class Feature(models.Model):
    CATEGORY_CHOICES = [
        ('interior', 'Ichki jihozlar'),
        ('exterior', 'Tashqi jihozlar'),
        ('safety', 'Xavfsizlik'),
        ('comfort', 'Qulaylik'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name