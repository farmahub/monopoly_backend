from rest_framework import serializers

from .models import Room, Ticket


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "name",
            "admin",
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "room",
        ]