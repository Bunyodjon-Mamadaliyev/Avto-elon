from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from listings.models import Listing, Image
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from listings.serializers import (ListingSerializer, ListingCreateSerializer,
                        ImageSerializer, ImageCreateSerializer)

User = get_user_model()

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.select_related(
        'car', 'car__make', 'car__model', 'car__body_type', 'seller'
    ).prefetch_related('images').filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ListingCreateSerializer
        return ListingSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsListingOwner()]
        return [permissions.AllowAny()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_listings = self.get_queryset().filter(is_featured=True)
        page = self.paginate_queryset(featured_listings)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(featured_listings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my(self, request):
        user_listings = self.get_queryset().filter(seller=request.user)
        serializer = self.get_serializer(user_listings, many=True)
        return Response(serializer.data)


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer

    def get_queryset(self):
        listing_id = self.kwargs.get('listing_id')
        return Image.objects.filter(listing_id=listing_id)

    def get_serializer_class(self):
        if self.action in ['create']:
            return ImageCreateSerializer
        return ImageSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            listing = get_object_or_404(Listing, id=self.kwargs.get('listing_id'))
            if listing.seller != self.request.user:
                return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class IsListingOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user


class SearchListView(generics.ListAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        queryset = Listing.objects.select_related(
            'car', 'car__make', 'car__model', 'car__body_type', 'seller'
        ).prefetch_related('images').filter(is_active=True)

        make = self.request.query_params.get('make')
        model = self.request.query_params.get('model')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        year_from = self.request.query_params.get('year_from')
        year_to = self.request.query_params.get('year_to')
        condition = self.request.query_params.get('condition')
        location = self.request.query_params.get('location')

        if make:
            queryset = queryset.filter(car__make__name__icontains=make)
        if model:
            queryset = queryset.filter(car__model__name__icontains=model)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if year_from:
            queryset = queryset.filter(car__year__gte=year_from)
        if year_to:
            queryset = queryset.filter(car__year__lte=year_to)
        if condition:
            queryset = queryset.filter(condition=condition)
        if location:
            queryset = queryset.filter(location__icontains=location)
        return queryset