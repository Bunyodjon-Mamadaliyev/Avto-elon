from django.test import TestCase
from django.contrib.auth.models import User
from reviews.models import Review
from listings.models import Listing
from cars.models import Make, CarModel, Car

class ReviewModelTest(TestCase):
    def setUp(self):
        self.reviewer = User.objects.create_user(username='reviewer', password='pass')
        self.reviewed_user = User.objects.create_user(username='reviewed', password='pass')
        self.make = Make.objects.create(name='Chevrolet')
        self.model = CarModel.objects.create(name='Malibu', make=self.make)
        self.car = Car.objects.create(make=self.make, model=self.model, year=2022)
        self.listing = Listing.objects.create(
            car=self.car,
            seller=self.reviewed_user,
            owner=self.reviewed_user,
            title='Sotiladi Malibu 2022',
            description='Yangi, ideal holatda',
            price=25000,
            currency='USD',
            location='Toshkent',
            condition='new'
        )
        self.review = Review.objects.create(
            reviewer=self.reviewer,
            reviewed_user=self.reviewed_user,
            listing=self.listing,
            rating=4,
            comment='Yaxshi sotuvchi edi.'
        )

    def test_str_method(self):
        expected_str = f"{self.review.rating} star review by {self.reviewer}"
        self.assertEqual(str(self.review), expected_str)

    def test_review_fields(self):
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, 'Yaxshi sotuvchi edi.')
        self.assertEqual(self.review.listing, self.listing)
        self.assertEqual(self.review.reviewer, self.reviewer)
