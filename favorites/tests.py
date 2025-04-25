from django.test import TestCase
from django.contrib.auth.models import User
from listings.models import Listing
from common.models import Make, CarModel
from cars.models import Car
from .models import SavedListing, ComparisonList

class SavedAndComparisonListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.make = Make.objects.create(name='Chevrolet')
        self.car_model = CarModel.objects.create(name='Cobalt', make=self.make)
        self.car = Car.objects.create(make=self.make, model=self.car_model, year=2020)

        self.listing = Listing.objects.create(
            car=self.car,
            seller=self.user,
            owner=self.user,
            title='Cobalt 2020',
            description='Sotiladi tezda',
            price=8000,
            currency='USD',
            location='Samarqand',
            condition='used'
        )

    def test_save_listing(self):
        saved = SavedListing.objects.create(user=self.user, listing=self.listing)
        self.assertEqual(SavedListing.objects.count(), 1)
        self.assertEqual(saved.user, self.user)
        self.assertEqual(saved.listing, self.listing)
        self.assertIn(saved, self.user.saved_listings.all())
        self.assertEqual(str(saved), f"{self.user.username} saved {self.listing.title}")

    def test_unique_saved_listing(self):
        SavedListing.objects.create(user=self.user, listing=self.listing)
        with self.assertRaises(Exception):
            SavedListing.objects.create(user=self.user, listing=self.listing)

    def test_comparison_list_create_and_add_listings(self):
        comparison = ComparisonList.objects.create(user=self.user)
        comparison.listings.add(self.listing)
        self.assertEqual(ComparisonList.objects.count(), 1)
        self.assertIn(self.listing, comparison.listings.all())
        self.assertEqual(str(comparison), f"{self.user.username}'s comparison list")

    def test_comparison_list_multiple_listings(self):
        listing2 = Listing.objects.create(
            car=self.car,
            seller=self.user,
            owner=self.user,
            title='Cobalt 2021',
            description='Yangi holat',
            price=9000,
            currency='USD',
            location='Toshkent',
            condition='used'
        )
        comparison = ComparisonList.objects.create(user=self.user)
        comparison.listings.set([self.listing, listing2])
        self.assertEqual(comparison.listings.count(), 2)
