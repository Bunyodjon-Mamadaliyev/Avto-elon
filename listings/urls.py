from django.urls import path, include
from rest_framework.routers import DefaultRouter
from listings.views import ListingViewSet, ImageViewSet, SearchListView

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')

urlpatterns = [
    path('', include(router.urls)),
    path('listings/<int:listing_id>/images/', ImageViewSet.as_view({'get': 'list', 'post': 'create'}), name='listing-images'),
    path('listings/<int:listing_id>/images/<int:pk>/', ImageViewSet.as_view({'delete': 'destroy'}), name='listing-image-detail'),
    path('search/listings/', SearchListView.as_view(), name='search-listings'),
]