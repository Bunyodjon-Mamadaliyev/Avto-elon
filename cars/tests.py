from django.test import TestCase
from django.contrib.auth.models import User
from common.models import Make, CarModel, BodyType, Feature
from cars.models import Car
from django.core.exceptions import ValidationError

class CarModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.make = Make.objects.create(name='Toyota')
        self.model = CarModel.objects.create(make=self.make, name='Camry')
        self.body_type = BodyType.objects.create(name='Sedan')
        self.feature1 = Feature.objects.create(name='Bluetooth')
        self.feature2 = Feature.objects.create(name='Sunroof')

    def test_create_car(self):
        car = Car.objects.create(
            make=self.make,
            model=self.model,
            year=2020,
            body_type=self.body_type,
            fuel_type='petrol',
            transmission='automatic',
            color='Qora',
            mileage=45000,
            engine_size=2.5,
            power=203,
            drive_type='fwd',
            vin='123456789ABCDEFGH',
            owner=self.user
        )
        car.features.set([self.feature1, self.feature2])
        car.save()

        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(car.make.name, 'Toyota')
        self.assertEqual(car.model.name, 'Camry')
        self.assertIn(self.feature1, car.features.all())
        self.assertEqual(str(car), '2020 Toyota Camry')

    def test_required_fields(self):
        with self.assertRaises(ValidationError):
            car = Car(
                make=self.make,
                model=self.model,
                year=2022,
                fuel_type='diesel',
                transmission='manual',
                color='Oq',
                mileage=10000,
                engine_size=2.0,
                power=150,
                drive_type='rwd',
                vin='VINMISSINGBODY'
            )
            car.full_clean()

    def test_unique_vin(self):
        Car.objects.create(
            make=self.make,
            model=self.model,
            year=2020,
            body_type=self.body_type,
            fuel_type='petrol',
            transmission='automatic',
            color='Qizil',
            mileage=30000,
            engine_size=2.0,
            power=150,
            drive_type='fwd',
            vin='UNIQUEVIN123456789',
            owner=self.user
        )

        with self.assertRaises(Exception):
            Car.objects.create(
                make=self.make,
                model=self.model,
                year=2021,
                body_type=self.body_type,
                fuel_type='diesel',
                transmission='manual',
                color='Oq',
                mileage=25000,
                engine_size=2.0,
                power=160,
                drive_type='rwd',
                vin='UNIQUEVIN123456789',
                owner=self.user
            )
