from rest_framework import serializers

class PriceDistributionSerializer(serializers.Serializer):
    range = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.FloatField()

class PopularMakeSerializer(serializers.Serializer):
    make = serializers.CharField()
    count = serializers.IntegerField()
    average_price = serializers.FloatField()

class PriceAnalyticsSerializer(serializers.Serializer):
    average_price = serializers.FloatField()
    min_price = serializers.FloatField()
    max_price = serializers.FloatField()
    price_distribution = PriceDistributionSerializer(many=True)
    popular_makes = PopularMakeSerializer(many=True)
    total_listings = serializers.IntegerField()

class MakePriceAnalyticsSerializer(serializers.Serializer):
    make = serializers.DictField(child=serializers.CharField())
    average_price = serializers.FloatField()
    min_price = serializers.FloatField()
    max_price = serializers.FloatField()
    price_distribution = PriceDistributionSerializer(many=True)
    popular_models = serializers.ListField(child=serializers.DictField())
    total_listings = serializers.IntegerField()

class SimilarListingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    price = serializers.FloatField()
    currency = serializers.CharField()
    mileage = serializers.IntegerField()
    similarity_score = serializers.FloatField()

class FactorSerializer(serializers.Serializer):
    factor = serializers.CharField()
    impact = serializers.CharField()
    description = serializers.CharField()

class PriceEstimateSerializer(serializers.Serializer):
    estimated_price = serializers.FloatField()
    price_range = serializers.DictField(child=serializers.FloatField())
    confidence_score = serializers.FloatField()
    similar_listings = SimilarListingSerializer(many=True)
    factors = FactorSerializer(many=True)

class TrendValueSerializer(serializers.Serializer):
    last_month = serializers.CharField()
    last_3_months = serializers.CharField()
    last_6_months = serializers.CharField()
    last_year = serializers.CharField()

class PopularItemSerializer(serializers.Serializer):
    name = serializers.CharField(source='make')
    percentage = serializers.FloatField()
    trend = serializers.CharField()

class BodyTypeTrendSerializer(serializers.Serializer):
    body_type = serializers.CharField()
    percentage = serializers.FloatField()
    trend = serializers.CharField()

class FuelTypeTrendSerializer(serializers.Serializer):
    fuel_type = serializers.CharField()
    percentage = serializers.FloatField()
    trend = serializers.CharField()

class MonthlyListingSerializer(serializers.Serializer):
    month = serializers.CharField()
    count = serializers.IntegerField()

class MarketTrendsSerializer(serializers.Serializer):
    price_trends = TrendValueSerializer()
    popular_makes = PopularItemSerializer(many=True)
    popular_body_types = BodyTypeTrendSerializer(many=True)
    fuel_type_distribution = FuelTypeTrendSerializer(many=True)
    monthly_listings = MonthlyListingSerializer(many=True)