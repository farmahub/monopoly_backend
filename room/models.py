import uuid
from datetime import timedelta

from django.utils import timezone
from django.db import models
from django.core.mail import send_mail
from django.utils.html import format_html

from account.models import User


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin")
    players = models.ManyToManyField(User, related_name="players", blank=True)
    min_players = models.IntegerField(default=2, editable=False)
    max_players = models.IntegerField(default=6, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)
    current_turn_player = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
    def close_room(self):
        if 2 <= self.players.count() <=6:
            self.is_closed = True
        else:
            self.is_closed = False
        self.save()
    
    def start_game(self):
        if not self.is_closed:
            return f"{self.room} is not closed"
        else:
            self.is_running = True
        self.save()

    def pause_game(self):
        if self.is_running:
            self.is_running = False
        else:
            self.is_running = True
        self.save()

    def next_turn(self):
        players_list = list(self.players.all())
        if self.current_turn_player in players_list:
            current_index = players_list.index(self.current_turn_player)
            next_index = (current_index + 1) % len(players_list)
            self.current_turn_player = players_list[next_index]
            self.save()


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="room", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    issued_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user", null=True
    )
    is_used = models.BooleanField(default=False)

    @property
    def is_expired(self):
        if self.created_at:
            expiration_time = self.created_at + timedelta(minutes=60)

            return (
                timezone.now() > expiration_time
            )  # returns true when "now" gets passed of expiration_time

    def __str__(self):
        return f"{self.id}"
    
    def send_ticket_email(self, recipient_email):
        subject = "You're Invited to Join a Room!"
        plaintext_message = f"Hi,\n\nYou've been invited to join a room on Farma!\n\nUse this link to register and join: http://localhost:8000/api/room/use-ticket/{self.id}/\n\nThis link will expire in five minutes."
        from_email = "farmamailbox@gmail.com"
        recipient_list = [recipient_email]
        html_message = format_html(
            f"""
            <html>
            <body>
            <p>Hi,</p>
            <p>You've been invited to join a room on Farma!</p>
            <p>Click the link below to register and join:</p>
            <p><a href='http://localhost:8000/api/room/use-ticket/{self.id}/'>Join using this link</a></p>
            <p>This link will expire in five minutes.</p>
            </body>
            </html>
            """
        )

        send_mail(
            subject,
            plaintext_message,
            from_email,
            recipient_list,
            html_message=html_message,
            auth_user="farmamailbox@gmail.com",
            auth_password="wmmh nunx wilp vuii",
        )
