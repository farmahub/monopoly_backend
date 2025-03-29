import uuid

from django.db import models

from account.models import User


class Property(models.Model):
    TYPE_CHOICES = [
        ("residential", "Residential"),
        ("station", "Station"),
        ("utility", "Utility"),
        ("public", "Public"),
    ]

    COLOR_CHOICES = [
        ("brown", "Brown"),
        ("blue", "Blue"),
        ("pink", "Pink"),
        ("orange", "Orange"),
        ("red", "Red"),
        ("yellow", "Yellow"),
        ("green", "Green"),
        ("violet", "Violet"),
        ("white", "White"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    position = models.IntegerField(default=0)
    color = models.CharField(max_length=6, choices=COLOR_CHOICES, blank=True)
    type = models.CharField(max_length=11, choices=TYPE_CHOICES)
    price = models.IntegerField(default=0)
    rent_single = models.IntegerField(default=0)
    rent_set = models.IntegerField(default=0)
    rent_1 = models.IntegerField(default=0, blank=True, null=True)
    rent_2 = models.IntegerField(default=0, blank=True, null=True)
    rent_3 = models.IntegerField(default=0, blank=True, null=True)
    rent_4 = models.IntegerField(default=0, blank=True, null=True)
    rent_5 = models.IntegerField(default=0, blank=True, null=True)
    loan_amount = models.IntegerField(default=0)
    loan_back_amount = models.IntegerField(default=0)
    house_price = models.IntegerField(default=0, blank=True, null=True)
    hotel_price = models.IntegerField(default=0, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.position}. {self.name} - {self.owner}'s property"
