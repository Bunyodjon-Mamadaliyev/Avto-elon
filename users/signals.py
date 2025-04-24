from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from dealers.models import Dealer

@receiver(post_save, sender=User)
def create_dealer_profile(sender, instance, created, **kwargs):
    if created:
        Dealer.objects.create(user=instance, company_name='-', description='-', address='-')
