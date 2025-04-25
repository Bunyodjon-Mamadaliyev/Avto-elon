from rest_framework import generics, permissions
from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing
from .models import Message
from .serializers import MessageSerializer

class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            models.Q(sender=self.request.user) |
            models.Q(receiver=self.request.user))

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            models.Q(sender=self.request.user) |
            models.Q(receiver=self.request.user))

class ConversationListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            models.Q(sender=self.request.user) |
            models.Q(receiver=self.request.user)
        ).distinct().order_by('-created_at')

class UserConversationView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        other_user = User.objects.get(id=user_id)
        return Message.objects.filter(
            models.Q(sender=self.request.user, receiver=other_user) |
            models.Q(sender=other_user, receiver=self.request.user)
        ).order_by('-created_at')


class ListingConversationView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        listing_id = self.kwargs['listing_id']
        listing = Listing.objects.get(id=listing_id)
        if self.request.user != listing.owner:
            return Message.objects.none()
        return Message.objects.filter(listing=listing).order_by('-created_at')