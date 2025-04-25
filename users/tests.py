from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            user_type='dealer',
            phone='+998901234567',
            location='Toshkent',
            rating=4.5
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.user_type, 'dealer')
        self.assertEqual(self.profile.phone, '+998901234567')
        self.assertEqual(self.profile.location, 'Toshkent')
        self.assertEqual(self.profile.rating, 4.5)

    def test_str_method(self):
        self.assertEqual(str(self.profile), 'testuser profile')
