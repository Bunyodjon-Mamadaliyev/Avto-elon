from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('regular', 'Oddiy foydalanuvchi'),
        ('dealer', 'Diler'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='regular')
    phone = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='user_avatars/', null=True, blank=True)
    location = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} profile"