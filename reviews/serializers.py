from rest_framework import serializers
from .models import Review
from django.contrib.auth.models import User
from listings.models import Listing

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class ListingShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['id', 'title']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserShortSerializer(read_only=True)
    reviewed_user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
        source='reviewed_user', write_only=True)
    reviewed_user = UserShortSerializer(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all(),
        source='listing', write_only=True, allow_null=True, required=False)
    listing = ListingShortSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'reviewed_user', 'reviewed_user_id',
                  'listing', 'listing_id', 'rating', 'comment', 'created_at']

