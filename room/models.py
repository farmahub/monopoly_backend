import uuid
from datetime import timedelta

from django.utils import timezone
from django.db import models

from account.models import User


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin")
    player = models.ManyToManyField(User, related_name="player", blank=True)
    min_players = models.IntegerField(default=2, editable=False)
    max_players = models.IntegerField(default=6, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def share_link(self):
        link = "Ticket" + "-" + str(self.id).split("-")[-1] + "-" + "Farma" + "-" + str(self.room.id).split("-")[-1]
        return link

    @property
    def is_expired(self):
        expiration_time = self.created_at + timedelta(hours=1)

        return (
            timezone.now() > expiration_time
        )  # returns true when "now" gets passed of expiration_time
    
    def __str__(self):
        return self.share_link
