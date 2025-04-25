from django.urls import path
from .views import MakeListView, CarModelListView, BodyTypeListView, FeatureListView

urlpatterns = [
    path('makes/', MakeListView.as_view(), name='make-list'),
    path('makes/<int:id>/models/', CarModelListView.as_view(), name='model-list'),
    path('body-types/', BodyTypeListView.as_view(), name='body-type-list'),
    path('features/', FeatureListView.as_view(), name='feature-list'),
]