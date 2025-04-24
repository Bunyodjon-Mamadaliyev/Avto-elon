from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.fields import DateTimeField
from .models import Dealer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class DealerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = DateTimeField(format="%Y-%m-%d %H:%M:%S")


    class Meta:
        model = Dealer
        fields = [
            'id', 'user', 'company_name', 'description', 'logo',
            'website', 'address', 'is_verified', 'rating',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['is_verified', 'rating', 'created_at', 'updated_at']

    def get_logo(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(obj.logo.url)
        return None


class DealerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = [
            'company_name', 'description', 'logo',
            'website', 'address',
        ]
        extra_kwargs = {
            'logo': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        if Dealer.objects.filter(user=user).exists():
            raise serializers.ValidationError("Siz allaqachon Dealer profiliga egasiz.")
        return Dealer.objects.create(user=user, **validated_data)

class DealerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = [
            'company_name', 'description', 'logo',
            'website', 'address'
        ]
        extra_kwargs = {
            'logo': {'required': False, 'allow_null': True},
        }