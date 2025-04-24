from rest_framework import generics, permissions, status, serializers
from .permissions import IsDealerOwner
from django.shortcuts import get_object_or_404
from .models import Dealer
from .serializers import DealerSerializer, DealerCreateSerializer, DealerUpdateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class DealerListView(generics.ListCreateAPIView):
    queryset = Dealer.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DealerCreateSerializer
        return DealerSerializer

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'dealer_profile'):
            raise serializers.ValidationError("Siz allaqachon dealer profilga egasiz.")


class DealerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dealer.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return DealerUpdateSerializer
        return DealerSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsDealerOwner()]
        return super().get_permissions()


class DealerListingsView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        dealer = get_object_or_404(Dealer, id=self.kwargs['pk'])
        return []


class DealerReviewsView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        dealer = get_object_or_404(Dealer, id=self.kwargs['pk'])
        return []

class MyDealerProfileView(generics.RetrieveAPIView):
    serializer_class = DealerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.dealer_profile

