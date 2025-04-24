from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing

class SavedListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_listings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')

    def __str__(self):
        return f"{self.user.username} saved {self.listing.title}"


class ComparisonList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comparison_lists')
    listings = models.ManyToManyField(Listing)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s comparison list"