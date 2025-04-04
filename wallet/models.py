import uuid
import random

from django.db import models
from django.shortcuts import get_object_or_404
from account.models import User


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position = models.IntegerField(default=0)
    cash = models.IntegerField(default=1500)
    house = models.IntegerField(default=0)
    hotel = models.IntegerField(default=0)
    imprisoned = models.BooleanField(default=False)
    jail_free_card = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")  # user.wallet

    def __str__(self):
        return f"{self.user}"
    