from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from .models import SavedListing, ComparisonList
from listings.models import Listing
from .serializers import SavedListingSerializer, ComparisonListSerializer
from django.shortcuts import get_object_or_404

class SavedListingListCreateView(ListCreateAPIView):
    serializer_class = SavedListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedListing.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavedListingDeleteView(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SavedListing.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ComparisonListListCreateView(ListCreateAPIView):
    serializer_class = ComparisonListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ComparisonList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ComparisonListAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        comp_list = get_object_or_404(ComparisonList, id=id, user=request.user)
        listing_id = request.data.get('listing_id')
        listing = get_object_or_404(Listing, id=listing_id)
        comp_list.listings.add(listing)
        return Response({'detail': 'Listing added to comparison list'}, status=status.HTTP_200_OK)


class ComparisonListRemoveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        comp_list = get_object_or_404(ComparisonList, id=id, user=request.user)
        listing_id = request.data.get('listing_id')
        listing = get_object_or_404(Listing, id=listing_id)
        comp_list.listings.remove(listing)
        return Response({'detail': 'Listing removed from comparison list'}, status=status.HTTP_200_OK)
