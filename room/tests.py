from django.test import TestCase

from .models import Ticket, Room
from account.models import User


class TicketTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create(email="admin@example.com")
        self.room = Room.objects.create(name="test_room", admin=self.admin)
        self.ticket = Ticket.objects.create(room=self.room)

    def test_query(self):
        print(self.ticket.share_link)
        self.assertIsNotNone(self.ticket)