from rest_framework import serializers
from listings.models import Listing
from common.models import Make, BodyType
from dealers.models import Dealer
from common.models import CarModel
from cars.models import Car

class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['id', 'name']

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
        fields = [
            'id', 'make', 'model', 'year', 'body_type',
            'fuel_type', 'transmission', 'color', 'mileage',
            'engine_size', 'power', 'drive_type'
        ]

class ListingSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'price', 'currency', 'location',
            'condition', 'views_count', 'created_at',
            'car', 'primary_image'
        ]

    def get_primary_image(self, obj):
        if obj.primary_image:
            return obj.primary_image.url
        return None

class SimilarListingSerializer(ListingSerializer):
    similarity_score = serializers.FloatField()

    class Meta(ListingSerializer.Meta):
        fields = ListingSerializer.Meta.fields + ['similarity_score']

class UserShortSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

class DealerSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    class Meta:
        model = Dealer
        fields = [
            'id', 'user', 'company_name', 'description', 'logo',
            'website', 'address', 'is_verified', 'rating',
            'created_at', 'updated_at'
        ]
