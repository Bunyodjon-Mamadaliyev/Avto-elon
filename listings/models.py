from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from cars.models import Car

def get_default_owner():
    user = User.objects.first()
    return user.id if user else None

def default_expiry():
    return timezone.now() + timedelta(days=30)

class Listing(models.Model):
    CURRENCY_CHOICES = [
        ('UZS', 'So\'m'),
        ('USD', 'Dollar'),
    ]

    CONDITION_CHOICES = [
        ('new', 'Yangi'),
        ('used', 'Ishlatilgan'),
    ]
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='listings')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_owner, related_name='listings_as_owner')
    primary_image = models.ImageField(upload_to='images/', default='default_listing.jpg')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UZS')
    location = models.CharField(max_length=100)
    condition = models.CharField(max_length=5, choices=CONDITION_CHOICES)
    is_negotiable = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=default_expiry)

    def __str__(self):
        return self.title

    @property
    def images_count(self):
        return self.images.count()


class Image(models.Model):
    image = models.ImageField(upload_to='listing_images/')
    is_primary = models.BooleanField(default=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.listing.title}"

    @property
    def primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.image.url
        first_image = self.images.first()
        return first_image.image.url if first_image else None