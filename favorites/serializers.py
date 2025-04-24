from rest_framework import serializers
from .models import SavedListing, ComparisonList
from listings.models import Listing
from listings.serializers import ListingSerializer

class SavedListingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), write_only=True, source='listing'
    )

    class Meta:
        model = SavedListing
        fields = ['id', 'listing', 'listing_id', 'created_at']


class ComparisonListSerializer(serializers.ModelSerializer):
    listings = ListingSerializer(many=True, read_only=True)

    class Meta:
        model = ComparisonList
        fields = ['id', 'listings', 'created_at', 'updated_at']
