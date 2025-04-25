from django.urls import path
from .views import (SavedListingListCreateView, SavedListingDeleteView,
    ComparisonListListCreateView, ComparisonListAddView, ComparisonListRemoveView
)

urlpatterns = [
    path('saved-listings/', SavedListingListCreateView.as_view()),
    path('saved-listings/<int:id>/', SavedListingDeleteView.as_view()),
    path('comparison-lists/', ComparisonListListCreateView.as_view()),
    path('comparison-lists/<int:id>/add/', ComparisonListAddView.as_view()),
    path('comparison-lists/<int:id>/remove/', ComparisonListRemoveView.as_view()),
]
