from django.test import TestCase
from django.contrib.auth.models import User
from .models import Dealer

class DealerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='dealeruser', password='testpass123')
        self.dealer = Dealer.objects.create(
            user=self.user,
            company_name='Test Company',
            description='A trusted car dealer.',
            website='https://www.testcompany.com',
            address='123 Main St, Test City',
            is_verified=True,
            rating=4.5
        )

    def test_dealer_creation(self):
        self.assertEqual(self.dealer.company_name, 'Test Company')
        self.assertEqual(self.dealer.user.username, 'dealeruser')
        self.assertTrue(self.dealer.is_verified)
        self.assertEqual(self.dealer.rating, 4.5)
        self.assertIsNotNone(self.dealer.created_at)
        self.assertIsNotNone(self.dealer.updated_at)

    def test_dealer_str(self):
        self.assertEqual(str(self.dealer), 'Test Company')
