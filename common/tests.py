from django.test import TestCase
from .serializers import FeatureSerializer
from common.models import Make, CarModel, BodyType, Feature


class MakeModelTest(TestCase):
    def test_create_make(self):
        make = Make.objects.create(name="Toyota", country="Japan", logo="make_logos/toyota.png")
        self.assertEqual(make.name, "Toyota")
        self.assertEqual(str(make), "Toyota")


class CarModelTest(TestCase):
    def setUp(self):
        self.make = Make.objects.create(name="Honda", country="Japan", logo="make_logos/honda.png")

    def test_create_car_model(self):
        car_model = CarModel.objects.create(name="Civic", make=self.make)
        self.assertEqual(car_model.name, "Civic")
        self.assertEqual(car_model.make.name, "Honda")
        self.assertEqual(str(car_model), "Honda Civic")


class BodyTypeTest(TestCase):
    def test_create_body_type(self):
        body_type = BodyType.objects.create(name="Sedan", image="body_types/sedan.png")
        self.assertEqual(body_type.name, "Sedan")
        self.assertEqual(str(body_type), "Sedan")


class FeatureTest(TestCase):
    def test_create_feature(self):
        feature = Feature.objects.create(name="Sunroof", category="exterior")
        self.assertEqual(feature.name, "Sunroof")
        self.assertEqual(feature.category, "exterior")
        self.assertEqual(str(feature), "Sunroof")

    def test_invalid_category(self):
        data = {"name": "Sunroof", "category": "invalid_category"}
        serializer = FeatureSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("category", serializer.errors)

