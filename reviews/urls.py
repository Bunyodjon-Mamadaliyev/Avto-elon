from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/users/<int:user_id>/', views.UserReviewsView.as_view(), name='user-reviews'),
    path('reviews/listings/<int:listing_id>/', views.ListingReviewsView.as_view(), name='listing-reviews'),
]
