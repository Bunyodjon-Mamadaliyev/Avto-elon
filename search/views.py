from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from listings.models import Listing, Car
from dealers.models import Dealer
from listings.serializers import ListingSerializer
from search.serializers import SimilarListingSerializer, DealerSerializer, CarSerializer
from listings.utils import get_similar_listings

class ListingSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        listings = Listing.objects.all()
        make = request.GET.get('make')
        model = request.GET.get('model')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        location = request.GET.get('location')

        if make:
            listings = listings.filter(car__make__name__icontains=make)
        if model:
            listings = listings.filter(car__model__name__icontains=model)
        if min_price:
            listings = listings.filter(price__gte=min_price)
        if max_price:
            listings = listings.filter(price__lte=max_price)
        if location:
            listings = listings.filter(location__icontains=location)
        serializer = ListingSerializer(listings, many=True, context={'request': request})
        return Response(serializer.data)

class DealerSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        dealers = Dealer.objects.all()
        name = request.GET.get('name')
        company = request.GET.get('company')

        if name:
            dealers = dealers.filter(user__first_name__icontains=name) | dealers.filter(user__last_name__icontains=name)
        if company:
            dealers = dealers.filter(company_name__icontains=company)

        serializer = DealerSerializer(dealers, many=True, context={'request': request})
        return Response(serializer.data)


class CarSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cars = Car.objects.all()
        make = request.GET.get('make')
        model = request.GET.get('model')
        year = request.GET.get('year')

        if make:
            cars = cars.filter(make__name__icontains=make)
        if model:
            cars = cars.filter(model__name__icontains=model)
        if year:
            cars = cars.filter(year=year)

        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)


class SimilarListingsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, listing_id):
        base_listing = get_object_or_404(Listing, id=listing_id)
        similar_listings = get_similar_listings(base_listing)

        serializer = SimilarListingSerializer(similar_listings, many=True, context={'request': request})
        return Response(serializer.data)
