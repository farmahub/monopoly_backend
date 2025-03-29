import uuid

from django.db import models
from account.models import User


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position = models.IntegerField(default=0)
    cash = models.IntegerField(default=1500)
    jail_free_card = models.IntegerField(default=0)
    house = models.IntegerField(default=0)
    hotel = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.position}"

    def buy_property(self, property):
        current_owner_user = property.owner
        current_owner_player = Player.objects.get(user_id=current_owner_user)
        if self.cash >= property.price:
            property.owner = self.user
            property.save()
            self.cash -= property.price
            current_owner_player.cash += property.price
            self.save()
            current_owner_player.save()
            return f"{property.name} successfully bought."

        else:
            return f"Not enough cash to buy {property.name}"
