import random

from django.test import TestCase
from django.core.management import call_command

from .models import Wallet
from property.models import Property
from account.models import User


class WalletTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("loaddata", "data.json")

    def setUp(self):
        self.bank_user = User.objects.get(username="wallet_bank")
        self.owner_user = User.objects.get(username="wallet_1")
        self.player_user = User.objects.get(username="wallet_2")

        self.bank_wallet = Wallet.objects.get(user_id=self.bank_user.id)
        self.owner_wallet = Wallet.objects.get(user_id=self.owner_user.id)
        self.player_wallet = Wallet.objects.get(user_id=self.player_user.id)

    def test_forward(self):
        if self.player_wallet.imprisoned:
            return f"{self.player_wallet} is imprisoned and can't move"
        
        dice_1 = random.randint(1, 6)
        dice_2 = random.randint(1, 6)
        # total = dice_1 + dice_2
        total = 27
        self.player_wallet.position = (self.player_wallet.position + total) % 40
        self.player_wallet.save()
        landing = Property.objects.get(position=self.player_wallet.position)

        print(landing)

        if landing.position == 30:
            self.player_wallet.position = 10
            self.player_wallet.imprisoned = True
            self.player_wallet.save()

            self.assertEqual(self.player_wallet.position, 10)
            self.assertEqual(self.player_wallet.imprisoned, True)

        else:
            if landing.type == "public":
                if landing.position == 0:
                    self.player_wallet.cash += landing.price
                    self.bank_wallet.cash -= landing.price
                    self.player_wallet.save()
                    self.bank_wallet.save()

                    self.assertEqual(self.player_wallet.cash, 1500 + landing.price)
                    self.assertEqual(self.bank_wallet.cash, 1500 - landing.price)

                elif landing.position == 4 or landing.position == 38:
                    self.player_wallet.cash -= landing.price
                    self.bank_wallet.cash += landing.price
                    self.player_wallet.save()
                    self.bank_wallet.save()

                    self.assertEqual(self.player_wallet.cash, 1500 - landing.price)
                    self.assertEqual(self.bank_wallet.cash, 1500 + landing.price)

                elif landing.name == "Chance":
                    pass

                elif landing.name == "Community Chest":
                    pass

            else:
                if landing.owner == self.bank_user:
                    # here i need a situation which i could wait for client choice
                    # between buying or go to auction with the base of 10 to maximum offer
                    landing.owner = self.player_user
                    self.player_wallet.cash -= landing.price
                    self.bank_wallet.cash += landing.price
                    landing.save()
                    self.player_wallet.save()
                    self.bank_wallet.save()

                    print(f"was under bank's ownership, now owned by {landing.owner}")

                    self.assertEqual(landing.owner, self.player_user)

                else:
                    print(f"under {landing.owner}'s ownership")

                    if not landing.check_color_set:
                        self.player_wallet.cash -= landing.rent_single
                        self.owner.cash += landing.rent_single
                        self.player_wallet.save()
                        self.owner_wallet.save()

                        self.assertEqual(self.player_wallet.cash, 1500 - landing.rent_single)
                        self.assertEqual(self.owner.cash, 1500 + landing.rent_single)

                    else:
                        if landing.type == "utility":
                            dice_1 = random.randint(1, 6)
                            dice_2 = random.randint(1, 6)
                            total = dice_1 + dice_2
                            self.player_wallet.cash -= total * 10
                            self.owner_wallet.cash += total * 10
                            self.player_wallet.save()
                            self.owner_wallet.save()

                            self.assertEqual(self.player_wallet.cash, 1500 - total * 10)
                            self.assertEqual(self.owner_wallet.cash, 1500 + total * 10)

                        elif landing.type == "station":
                            if landing.check_color_set() == 1:
                                self.player_wallet.cash -= landing.rent_1
                                self.owner_wallet.cash += landing.rent_1
                                self.player_wallet.save()
                                self.owner_wallet.save()

                                self.assertEqual(self.player_wallet.cash, 1500 - landing.rent_1)
                                self.assertEqual(self.owner_wallet.cash, 1500 + landing.rent_1)

                            elif landing.check_color_set() == 2:
                                self.player_wallet.cash -= landing.rent_2
                                self.owner_wallet.cash += landing.rent_2
                                self.player_wallet.save()
                                self.owner_wallet.save()

                                self.assertEqual(self.player_wallet.cash, 1500 - landing.rent_2)
                                self.assertEqual(self.owner_wallet.cash, 1500 + landing.rent_2)
                            
                            elif landing.check_color_set() == 3:
                                self.player_wallet.cash -= landing.rent_3
                                self.owner_wallet.cash += landing.rent_3
                                self.player_wallet.save()
                                self.owner_wallet.save()

                                self.assertEqual(self.player_wallet.cash, 1500 - landing.rent_3)
                                self.assertEqual(self.owner_wallet.cash, 1500 + landing.rent_3)
                            
                            elif landing.check_color_set() == 4:
                                self.player_wallet.cash -= landing.rent_4
                                self.owner_wallet.cash += landing.rent_4
                                self.player_wallet.save()
                                self.owner_wallet.save()

                                self.assertEqual(self.player_wallet.cash, 1500 - landing.rent_4)
                                self.assertEqual(self.owner_wallet.cash, 1500 + landing.rent_4)

                        elif landing.type == "residential":
                            if landing.dwelling_counts == 0:
                                self.player_wallet.cash -= landing.rent_set
                                self.owner_wallet.cash += landing.rent_set
                                self.player_wallet.save()
                                self.owner_wallet.save()

                                self.assertEqual(self.player_wallet.cash, 1500 - landing.rent_set)
                                self.assertEqual(self.owner_wallet.cash, 1500 + landing.rent_set)

                            elif landing.dwelling_counts == 1:
                                self.player_wallet.cash -= landing.rent_1
                                self.owner.cash += landing.rent_1
                                self.player_wallet.save()
                                self.owner_wallet.save()

                                self.assertEqual(self.player_wallet.cash, 1500 - landing.rent_1)
                                self.assertEqual(self.owner_wallet.cash, 1500 + landing.rent_1)

                            elif landing.dwelling_counts == 2:
                                self.player_wallet.cash -= landing.rent_2
                                self.owner_wallet.cash += landing.rent_2
                                self.player_wallet.save()
                                self.owner_wallet.save()

                                self.assertEqual(self.player_wallet.cash, 1500 - landing.rent_2)
                                self.assertEqual(self.owner_wallet.cash, 1500 + landing.rent_2)

                            elif landing.dwelling_counts == 3:
                                self.player_wallet.cash -= landing.rent_3
                                self.owner_wallet.cash += landing.rent_3
                                self.player_wallet.save()
                                self.owner_wallet.save()

                                self.assertEqual(self.player_wallet.cash, 1500 - landing.rent_3)
                                self.assertEqual(self.owner_wallet.cash, 1500 + landing.rent_3)

                            elif landing.dwelling_counts == 4:
                                self.player_wallet.cash -= landing.rent_4
                                self.owner_wallet.cash += landing.rent_4
                                self.player_wallet.save()
                                self.owner_wallet.save()

                                self.assertEqual(self.player_wallet.cash, 1500 - landing.rent_4)
                                self.assertEqual(self.owner_wallet.cash, 1500 + landing.rent_4)

                            elif landing.dwelling_counts == 5:
                                self.player_wallet.cash -= landing.rent_5
                                self.owner_wallet.cash += landing.rent_5
                                self.player_wallet.save()
                                self.owner_wallet.save()

                                self.assertEqual(self.player_wallet.cash, 1500 - landing.rent_5)
                                self.assertEqual(self.owner_wallet.cash, 1500 + landing.rent_5)