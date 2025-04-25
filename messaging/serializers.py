from rest_framework import serializers
from .models import Message
from listings.models import Listing
from django.contrib.auth import get_user_model

User = get_user_model()

class SUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class SListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['id', 'title']

class MessageSerializer(serializers.ModelSerializer):
    sender = SUserSerializer(read_only=True)
    receiver = SUserSerializer(read_only=True)
    listing = SListingSerializer(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True, required=True)
    listing_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = [ 'id', 'sender', 'receiver', 'listing', 'content', 'is_read',
                   'created_at', 'receiver_id', 'listing_id']
        read_only_fields = ['id', 'sender', 'receiver', 'listing', 'is_read', 'created_at']