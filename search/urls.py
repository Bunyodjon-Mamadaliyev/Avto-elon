from django.urls import path
from .views import ListingSearchView, DealerSearchView, CarSearchView, SimilarListingsView

urlpatterns = [
    path('listings/', ListingSearchView.as_view(), name='search-listings'),
    path('dealers/', DealerSearchView.as_view(), name='search-dealers'),
    path('cars/', CarSearchView.as_view(), name='search-cars'),
    path('similar/<int:listing_id>/', SimilarListingsView.as_view(), name='search-similar'),
]
