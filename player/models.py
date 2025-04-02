import uuid
import random

from django.db import models
from django.shortcuts import get_object_or_404
from account.models import User


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position = models.IntegerField(default=0)
    cash = models.IntegerField(default=1500)
    house = models.IntegerField(default=0)
    hotel = models.IntegerField(default=0)
    imprisoned = models.BooleanField(default=False)
    jail_free_card = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="player")  # user.player

    def __str__(self):
        return f"{self.user}"
    
    def pay(self, amount:int):
        self.cash -= amount
        self.save()
    
    def earn(self, amount:int):
        self.cash += amount
        self.save()


    def imprison(self):
        self.imprisoned = True
        self.save()

    def own(self, property):
        bank = get_object_or_404(User, username="bank")

        if property.owner != bank:
            return f"{property} is not under bank's ownership"
        
        if self.cash < property.price:
            return f"{property}'s price is greater than your balance"
        
        property.owner = self.user
        self.cash -= property.price
        bank_player = Player.objects.get(user_id=bank.id)
        bank_player.cash += property.price

        property.save()
        self.save()
        bank_player.save()

        return True