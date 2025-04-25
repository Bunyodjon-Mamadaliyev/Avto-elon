from django.urls import path
from .views import (MessageListCreateView, MessageDetailView, ConversationListView,
                    UserConversationView, ListingConversationView)

urlpatterns = [
    path('messages/', MessageListCreateView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('messages/conversations/', ConversationListView.as_view(), name='conversation-list'),
    path('messages/conversations/<int:user_id>/', UserConversationView.as_view(), name='user-conversation'),
    path('messages/listings/<int:listing_id>/', ListingConversationView.as_view(), name='listing-conversation'),
]