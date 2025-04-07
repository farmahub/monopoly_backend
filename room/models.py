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
        plaintext_message = f"Hi,\n\nYou've been invited to join a room on Farma!\n\nUse this link to register and join: http://localhost:8000/account/\n\nThis link will expire in five minutes."
        from_email = "farmamailbox@gmail.com"
        recipient_list = [recipient_email]
        html_message = format_html(
            f"""
            <html>
            <body>
            <p>Hi,</p>
            <p>You've been invited to join a room on Farma!</p>
            <p>Click the link below to register and join:</p>
            <p><a href='http://localhost:8000/account/'>Join using this link</a></p>
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
