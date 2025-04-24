from django.urls import path
from .views import (
    DealerListView,
    DealerDetailView,
    DealerListingsView,
    DealerReviewsView
)

urlpatterns = [
    path('dealers/', DealerListView.as_view(), name='dealer-list'),
    path('dealers/<int:id>/', DealerDetailView.as_view(), name='dealer-detail'),
    path('dealers/<int:id>/listings/', DealerListingsView.as_view(), name='dealer-listings'),
    path('dealers/<int:id>/reviews/', DealerReviewsView.as_view(), name='dealer-reviews'),
]