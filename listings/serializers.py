from rest_framework import serializers
from django.contrib.auth.models import User
from cars.models import Car, Make, CarModel, BodyType
from listings.models import Listing, Image
from dealers.models import Dealer


class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['id', 'name']
        ref_name = "ListingsMake"

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name']

class BodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyType
        fields = ['id', 'name']

class CarSerializer(serializers.ModelSerializer):
    make = MakeSerializer()
    model = ModelSerializer()
    body_type = BodyTypeSerializer()

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'year', 'body_type',
                  'fuel_type', 'transmission', 'color', 'mileage']
        ref_name = "ListingsCarSerializer"

class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'user_type']
        ref_name = "ListingsUser"

    def get_user_type(self, obj):
        if hasattr(obj, 'dealer_profile'):
            return 'dealer'
        return 'individual'


class DealerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Dealer
        fields = ['user', 'company_name', 'description', 'logo',
                  'website', 'address', 'is_verified', 'rating']


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'image_url', 'is_primary', 'order', 'created_at']

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None


class ListingSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    seller = UserSerializer()
    primary_image = serializers.SerializerMethodField()
    images_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price', 'currency',
            'location', 'condition', 'is_negotiable', 'is_active',
            'is_featured', 'views_count', 'created_at', 'updated_at',
            'expires_at', 'car', 'seller', 'primary_image', 'images_count'
        ]

    def get_primary_image(self, obj):
        if obj.primary_image:
            return self.context['request'].build_absolute_uri(obj.primary_image.url)

        first_image = obj.images.first()
        if first_image and first_image.image:
            return self.context['request'].build_absolute_uri(first_image.image.url)
        return None


class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'car', 'title', 'description', 'price', 'currency',
            'location', 'condition', 'is_negotiable', 'primary_image'
        ]

    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image', 'is_primary', 'order']

    def create(self, validated_data):
        listing_id = self.context['view'].kwargs.get('listing_id')
        validated_data['listing_id'] = listing_id
        return super().create(validated_data)