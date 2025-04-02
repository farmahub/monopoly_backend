from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import User
from .models import Player


# should been imported in AppConfig

@receiver(post_save, sender=User)
def player_handler(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        print(f"Player for {instance} is created successfully")