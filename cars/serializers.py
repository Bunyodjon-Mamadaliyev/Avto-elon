from rest_framework import serializers
from .models import Car, Make, CarModel, BodyType, Feature


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name', 'category']
        ref_name = "CarsFeature"


class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['id', 'name', 'country']
        ref_name = "CarsMake"


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name']
        ref_name = "CarsCarModel"


class BodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyType
        fields = ['id', 'name']
        ref_name = "CarsBodyType"


class CarSerializer(serializers.ModelSerializer):
    make = MakeSerializer(read_only=True)
    model = CarModelSerializer(read_only=True)
    body_type = BodyTypeSerializer(read_only=True)
    features = FeatureSerializer(many=True, read_only=True)

    make_id = serializers.PrimaryKeyRelatedField(queryset=Make.objects.all(), source='make', write_only=True)
    model_id = serializers.PrimaryKeyRelatedField(queryset=CarModel.objects.all(), source='model', write_only=True)
    body_type_id = serializers.PrimaryKeyRelatedField(queryset=BodyType.objects.all(), source='body_type', write_only=True, allow_null=True)
    feature_ids = serializers.PrimaryKeyRelatedField(queryset=Feature.objects.all(), write_only=True, many=True, required=False)

    class Meta:
        model = Car
        fields = ['id', 'make', 'make_id', 'model', 'model_id', 'year', 'body_type',
                  'body_type_id', 'fuel_type', 'transmission', 'color', 'mileage',
                  'engine_size', 'power', 'drive_type', 'features', 'feature_ids',
                  'vin', 'created_at', 'updated_at', 'owner']
        ref_name = "CarsCarSerializer"
        read_only_fields = ['created_at', 'updated_at', 'owner']
        extra_kwargs = {
            'vin': {'validators': []}
        }

    def create(self, validated_data):
        feature_ids = validated_data.pop('feature_ids', [])
        validated_data['owner'] = self.context['request'].user
        car = super().create(validated_data)
        car.features.set(feature_ids)
        return car

    def update(self, instance, validated_data):
        feature_ids = validated_data.pop('feature_ids', )
        car = super().update(instance, validated_data)
        if feature_ids is not None:
            car.features.set(feature_ids)
        return car

    def validate_vin(self, value):
        if self.instance and self.instance.vin == value:
            return value
        if Car.objects.filter(vin=value).exists():
            raise serializers.ValidationError("A car with this VIN already exists.")
        return value
