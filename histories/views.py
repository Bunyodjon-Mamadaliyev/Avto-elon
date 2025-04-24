from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.db.models import Avg, Min, Max, Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from datetime import datetime, timedelta
from django.utils import timezone
from cars.models import Make, CarModel
from listings.models import Listing
from histories.models import PriceHistory
from .serializers import ( PriceAnalyticsSerializer, MakePriceAnalyticsSerializer,
                           PriceEstimateSerializer, MarketTrendsSerializer)


class PriceAnalyticsView(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        cache_key = 'overall_price_stats'
        data = cache.get(cache_key)

        if not data:
            active_listings = Listing.objects.filter(is_active=True)
            if not active_listings.exists():
                return Response(
                    {"detail": "No active listings found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            price_ranges = [
                (0, 10000),
                (10000, 20000),
                (20000, 30000),
                (30000, 50000),
                (50000, 100000),
                (100000, None)]
            price_distribution = []
            for price_min, price_max in price_ranges:
                q_filter = Q(price__gte=price_min)
                if price_max:
                    q_filter &= Q(price__lt=price_max)
                else:
                    q_filter &= Q(price__gte=price_min)
                count = active_listings.filter(q_filter).count()
                percentage = round((count / active_listings.count()) * 100, 2)
                range_name = f"{price_min}-{price_max}" if price_max else f"{price_min}+"
                price_distribution.append({
                    "range": range_name,
                    "count": count,
                    "percentage": percentage
                })

            popular_makes = active_listings.values('car__make__name').annotate(
                count=Count('id'),average_price=Avg('price')).order_by('-count')[:5]

            data = {
                "average_price": active_listings.aggregate(avg=Avg('price'))['avg'],
                "min_price": active_listings.aggregate(min=Min('price'))['min'],
                "max_price": active_listings.aggregate(max=Max('price'))['max'],
                "price_distribution": price_distribution,
                "popular_makes": [
                    {
                        "make": item['car__make__name'],
                        "count": item['count'],
                        "average_price": item['average_price']
                    }
                    for item in popular_makes
                ],
                "total_listings": active_listings.count()
            }
            cache.set(cache_key, data, 60 * 60 * 2)
        serializer = PriceAnalyticsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class MakePriceAnalyticsView(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, make_id):
        try:
            make = Make.objects.get(pk=make_id)
        except Make.DoesNotExist:
            return Response(
                {"detail": "Make not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cache_key = f'make_price_stats_{make_id}'
        data = cache.get(cache_key)

        if not data:
            listings = Listing.objects.filter(is_active=True, car__make=make)
            if not listings.exists():
                return Response({"detail": "No active listings for this make"},
                    status=status.HTTP_404_NOT_FOUND)
            price_ranges = [
                (0, 10000),
                (10000, 20000),
                (20000, 30000),
                (30000, 50000),
                (50000, 100000),
                (100000, None)
            ]
            price_distribution = []
            for price_min, price_max in price_ranges:
                q_filter = Q(price__gte=price_min)
                if price_max:
                    q_filter &= Q(price__lt=price_max)
                else:
                    q_filter &= Q(price__gte=price_min)
                count = listings.filter(q_filter).count()
                percentage = round((count / listings.count()) * 100, 2) if listings.count() > 0 else 0
                range_name = f"{price_min}-{price_max}" if price_max else f"{price_min}+"
                price_distribution.append({ "range": range_name, "count": count, "percentage": percentage})

            popular_models = listings.values('car__model__name').annotate(
                count=Count('id'), average_price=Avg('price')).order_by('-count')[:5]

            data = {
                "make": { "id": make.id, "name": make.name, "country": make.country},
                "average_price": listings.aggregate(avg=Avg('price'))['avg'],
                "min_price": listings.aggregate(min=Min('price'))['min'],
                "max_price": listings.aggregate(max=Max('price'))['max'],
                "price_distribution": price_distribution,
                "popular_models": [
                    {
                        "model": item['car__model__name'],
                        "count": item['count'],
                        "average_price": item['average_price']
                    }
                    for item in popular_models
                ],
                "total_listings": listings.count()
            }
            cache.set(cache_key, data, 60 * 60 * 2)
        serializer = MakePriceAnalyticsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class PriceEstimateView(APIView):
    def post(self, request):
        response_data = {
            "estimated_price": 24500.00,
            "price_range": { "min": 23000.00, "max": 26000.00},
            "confidence_score": 0.85, "similar_listings": [
                {
                    "id": 5,
                    "title": "Toyota Camry 2020, ideal holatda",
                    "price": 24000.00,
                    "currency": "USD",
                    "mileage": 45000,
                    "similarity_score": 0.95
                },
                {
                    "id": 12,
                    "title": "Toyota Camry 2019, ideal holatda",
                    "price": 22000.00,
                    "currency": "USD",
                    "mileage": 35000,
                    "similarity_score": 0.85
                }
            ],
            "factors": [
                {
                    "factor": "year",
                    "impact": "+2000.00",
                    "description": "2020 yil modellari o'rtacha 2000 USD qimmatroq"
                },
                {
                    "factor": "mileage",
                    "impact": "-500.00",
                    "description": "45000 km yurgan avtomobillar o'rtacha 500 USD arzonroq"
                },
                {
                    "factor": "features",
                    "impact": "+1000.00",
                    "description": "Qo'shimcha xususiyatlar narxni 1000 USD oshiradi"
                }
            ]
        }
        serializer = PriceEstimateSerializer(data=response_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class MarketTrendsView(APIView):
    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request):
        cache_key = 'market_trends'
        data = cache.get(cache_key)

        if not data:
            now = timezone.now()
            price_trends = {
                "last_month": "+2.5%",
                "last_3_months": "+5.8%",
                "last_6_months": "+8.2%",
                "last_year": "+12.5%"}

            popular_makes = Listing.objects.filter(is_active=True).values('car__make__name'
            ).annotate(
                count=Count('id')
            ).order_by('-count')[:5]
            total_listings = Listing.objects.filter(is_active=True).count()
            monthly_listings = []
            for month in range(1, 8):
                month_name = datetime(2023, month, 1).strftime('%B')
                monthly_listings.append({"month": month_name, "count": (300 - (7 - month) * 20)})
            data = {
                "price_trends": price_trends,
                "popular_makes": [
                    {
                        "make": item['car__make__name'],
                        "percentage": round((item['count'] / total_listings) * 100, 2),
                        "trend": "+3.2%"
                    }
                    for item in popular_makes
                ],
                "popular_body_types": [
                    {
                        "body_type": "Sedan",
                        "percentage": 35,
                        "trend": "-1.5%"
                    },
                ],
                "fuel_type_distribution": [
                    {
                        "fuel_type": "Petrol",
                        "percentage": 65,
                        "trend": "-2.5%"
                    },
                ],
                "monthly_listings": monthly_listings
            }
            cache.set(cache_key, data, 60 * 60 * 24)
        serializer = MarketTrendsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)