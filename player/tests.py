import random

from django.test import TestCase
from django.core.management import call_command

from .models import Player
from property.models import Property
from account.models import User


class PlayerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "data.json")

    def setUp(self):
        self.bank = Player.objects.get(user_id=User.objects.get(username="bank").id)
        self.player = Player.objects.get(user_id=User.objects.get(username="player_1").id)
        self.property = Property.objects.get(name="Pall Mall")

    def test_pay(self):
        amount = 50
        self.player.cash -= amount
        self.player.save()

        self.assertEqual(self.player.cash, 1450)

    def test_earn(self):
        amount = 50
        self.player.cash += amount
        self.player.save()

        self.assertEqual(self.player.cash, 1550)

    def test_imprison(self):
        self.player.imprisoned = True

        self.assertEqual(self.player.imprisoned, True)

    def test_own(self):
        if self.property.owner != User.objects.get(username="bank"):
            print('Not under bank\'s ownership')
        
        self.property.owner = User.objects.get(username="player_1")
        self.player.cash -= self.property.price
        self.bank.cash += self.property.price
        self.property.save()
        self.player.save()
        self.bank.save()

        self.assertEqual(self.property.owner, User.objects.get(username="player_1"))
        self.assertEqual(self.player.cash, 1500 - self.property.price)
        self.assertEqual(self.bank.cash, 1500 + self.property.price)
