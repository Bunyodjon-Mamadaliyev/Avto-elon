from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing
from django.utils import timezone
from datetime import timedelta

def default_expiry():
    return timezone.now() + timedelta(days=30)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    expires_at = models.DateTimeField(default=default_expiry)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
