from django.urls import path
from .views import (PriceAnalyticsView, MakePriceAnalyticsView,
    PriceEstimateView, MarketTrendsView)

urlpatterns = [
    path('analytics/price/', PriceAnalyticsView.as_view(), name='price-analytics'),
    path('analytics/price/makes/<int:make_id>/', MakePriceAnalyticsView.as_view(), name='make-price-analytics'),
    path('analytics/price/estimate/', PriceEstimateView.as_view(), name='price-estimate'),
    path('analytics/trends/', MarketTrendsView.as_view(), name='market-trends'),
]