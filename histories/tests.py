from django.test import TestCase
from django.contrib.auth.models import User
from listings.models import Listing
from cars.models import Car
from common.models import Make, CarModel
from .models import PriceHistory

class PriceHistoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.make = Make.objects.create(name='Chevrolet')
        self.model = CarModel.objects.create(name='Gentra', make=self.make)
        self.car = Car.objects.create(make=self.make, model=self.model, year=2022)
        self.listing = Listing.objects.create(
            car=self.car,
            seller=self.user,
            owner=self.user,
            title='Gentra 2022',
            description='Yangi Gentra',
            price=12000,
            currency='USD',
            location='Andijon',
            condition='new'
        )
    def test_create_price_history(self):
        price_history = PriceHistory.objects.create(
            listing=self.listing,
            price=11500,
            currency='USD'
        )
        self.assertEqual(PriceHistory.objects.count(), 1)
        self.assertEqual(price_history.listing, self.listing)
        self.assertEqual(price_history.price, 11500)
        self.assertEqual(price_history.currency, 'USD')

    def test_price_history_ordering(self):
        PriceHistory.objects.create(listing=self.listing, price=11500, currency='USD')
        PriceHistory.objects.create(listing=self.listing, price=11000, currency='USD')

        history = PriceHistory.objects.all()
        self.assertEqual(history[0].price, 11000)
        self.assertEqual(history[1].price, 11500)

    def test_str_method(self):
        price_history = PriceHistory.objects.create(
            listing=self.listing,
            price=11800,
            currency='USD'
        )
        self.assertEqual(str(price_history), f"Price update for {self.listing.title}")
