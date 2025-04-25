from django.test import TestCase
from django.contrib.auth.models import User
from cars.models import Car
from common.models import Make, CarModel
from listings.models import Listing, Image
from datetime import timedelta

class ListingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.make = Make.objects.create(name='Chevrolet')
        self.model = CarModel.objects.create(name='Malibu', make=self.make)
        self.car = Car.objects.create(make=self.make, model=self.model, year=2020)

        self.listing = Listing.objects.create(
            car=self.car,
            seller=self.user,
            owner=self.user,
            title='Malibu 2020',
            description='Chevrolet Malibu 2020, juda yaxshi holat.',
            price=20000,
            currency='USD',
            location='Toshkent',
            condition='new'
        )

    def test_create_listing(self):
        listing = Listing.objects.create(
            car=self.car,
            seller=self.user,
            owner=self.user,
            title='Malibu 2021',
            description='Chevrolet Malibu 2021 model.',
            price=22000,
            currency='USD',
            location='Samarqand',
            condition='new'
        )
        self.assertEqual(Listing.objects.count(), 2)
        self.assertEqual(listing.title, 'Malibu 2021')
        self.assertEqual(listing.price, 22000)

    def test_str_method(self):
        self.assertEqual(str(self.listing), 'Malibu 2020')

    def test_images_count(self):
        image1 = Image.objects.create(listing=self.listing, image='images/test1.jpg', is_primary=True)
        image2 = Image.objects.create(listing=self.listing, image='images/test2.jpg')
        self.assertEqual(self.listing.images_count, 2)

    def test_listing_owner_related_name(self):
        self.assertEqual(self.listing.owner.listings_as_owner.count(), 1)

    def test_default_expiry(self):
        expiry = self.listing.expires_at
        expected_expiry = self.listing.created_at + timedelta(days=30)
        self.assertAlmostEqual(expiry, expected_expiry, delta=timedelta(seconds=5))

class ImageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.make = Make.objects.create(name='Chevrolet')
        self.model = CarModel.objects.create(name='Malibu', make=self.make)
        self.car = Car.objects.create(make=self.make, model=self.model, year=2020)
        self.listing = Listing.objects.create(
            car=self.car,
            seller=self.user,
            owner=self.user,
            title='Malibu 2020',
            description='Chevrolet Malibu 2020, juda yaxshi holat.',
            price=20000,
            currency='USD',
            location='Toshkent',
            condition='new'
        )
    def test_create_image(self):
        image = Image.objects.create(
            listing=self.listing,
            image='images/test.jpg',
            is_primary=True
        )
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(image.listing, self.listing)
        self.assertTrue(image.is_primary)

    def test_primary_image_property(self):
        non_primary_image = Image.objects.create(listing=self.listing, is_primary=False, order=1)
        primary_image = Image.objects.create(listing=self.listing, is_primary=True, order=0)
        primary_image_from_listing = self.listing.images.filter(is_primary=True).first()
        self.assertEqual(primary_image_from_listing.id, primary_image.id)
