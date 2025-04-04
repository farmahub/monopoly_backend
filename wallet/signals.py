from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import User
from .models import Wallet


# should been imported in AppConfig

@receiver(post_save, sender=User)
def wallet_handler(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
        print(f"Wallet for {instance} is created successfully")