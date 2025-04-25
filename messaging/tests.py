from django.test import TestCase
from django.contrib.auth.models import User
from cars.models import Car
from common.models import Make, CarModel
from listings.models import Listing
from messaging.models import Message
from django.utils import timezone
from datetime import timedelta


class MessageModelTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='password')
        self.receiver = User.objects.create_user(username='receiver', password='password')
        self.make = Make.objects.create(name='Chevrolet')
        self.model = CarModel.objects.create(name='Malibu', make=self.make)
        self.car = Car.objects.create(make=self.make, model=self.model, year=2022)
        self.listing = Listing.objects.create(
            car=self.car,
            seller=self.sender,
            owner=self.sender,
            title='Sotiladi Malibu 2022',
            description='Ideal holatda, yangi',
            price=25000,
            currency='USD',
            location='Toshkent',
            condition='new'
        )

    def test_message_creation(self):
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            listing=self.listing,
            content="Salom, Malibu hali bormi?"
        )
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(msg.sender, self.sender)
        self.assertEqual(msg.receiver, self.receiver)
        self.assertEqual(msg.content, "Salom, Malibu hali bormi?")
        self.assertFalse(msg.is_read)
        self.assertEqual(msg.listing, self.listing)

    def test_default_expiry(self):
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Default expiry tekshirish"
        )
        expected_expiry = timezone.now() + timedelta(days=30)
        self.assertTrue(abs((msg.expires_at - expected_expiry).total_seconds()) < 5)

    def test_str_method(self):
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test string"
        )
        self.assertEqual(str(msg), f"Message from {self.sender} to {self.receiver}")

    def test_ordering(self):
        msg1 = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="1-xabar"
        )
        msg2 = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="2-xabar"
        )
        messages = Message.objects.all()
        self.assertEqual(messages[0], msg2)
        self.assertEqual(messages[1], msg1)
