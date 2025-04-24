from rest_framework import serializers
from .models import Make, CarModel, BodyType, Feature


class MakeSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Make
        fields = ['id', 'name', 'country', 'logo']

    def get_logo(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(obj.logo.url)
        return None


class CarModelSerializer(serializers.ModelSerializer):
    make = serializers.PrimaryKeyRelatedField(queryset=Make.objects.all())

    class Meta:
        model = CarModel
        fields = ['id', 'name', 'make']


class BodyTypeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = BodyType
        fields = ['id', 'name', 'image']
        ref_name = "CommonBodyType"

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name', 'category']
        ref_name = "CommonFeature"