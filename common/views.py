from rest_framework import generics
from .models import Make, CarModel, BodyType, Feature
from django.shortcuts import get_object_or_404
from .serializers import (MakeSerializer, CarModelSerializer,
                          BodyTypeSerializer, FeatureSerializer)

class MakeListView(generics.ListAPIView):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer
    permission_classes = []


class CarModelListView(generics.ListAPIView):
    serializer_class = CarModelSerializer
    permission_classes = []

    def get_queryset(self):
        make_id = self.kwargs['id']
        make = get_object_or_404(Make, id=make_id)
        return CarModel.objects.filter(make=make)


class BodyTypeListView(generics.ListAPIView):
    queryset = BodyType.objects.all()
    serializer_class = BodyTypeSerializer
    permission_classes = []


class FeatureListView(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = []