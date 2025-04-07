from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Ticket

# to get worked, connect via "def ready" in app's config
@receiver(pre_save, sender=Ticket)
def set_issued_to(sender, instance, **kwargs):
    if instance.room and not instance.issued_to:
        instance.issued_to = instance.room.admin
        print("issued to room's admin")