from django.test import TestCase

from .models import Ticket, Room
from .signals import set_issued_to
from account.models import User
from django.db.models.signals import pre_save


class RoomTest(TestCase):
    @classmethod
    def setUpTestData(
        cls,
    ):  # to prevent setup data for each "def test()" once, use this !
        cls.players = {}
        for i in range(1, 8):
            cls.players[f"player_{i}"] = User.objects.create(
                email=f"player_{i}@example.com"
            )
        cls.room = Room.objects.create(name="test_room", admin=cls.players["player_1"])

    # def setUp(self):  # sets up data for each "def test(self) once and causes duplicated datas"

    def test_start_game(self):
        self.room.is_closed = False
        self.room.start_game()
        self.assertIs(self.room.is_running, False)

        self.room.is_closed = True
        self.room.start_game()
        self.assertIs(self.room.is_running, True)

    def test_pause_game(self):
        self.room.is_running = True
        self.room.pause_game()
        self.assertIs(self.room.is_running, False)

    def test_close_room(self):
        self.room.players.set(
            [
                self.players["player_1"],
            ]
        )
        self.room.close_room()
        self.assertIs(self.room.is_closed, False)

        self.room.players.set(
            [
                self.players["player_1"],
                self.players["player_2"],
            ]
        )
        self.room.close_room()
        self.assertIs(self.room.is_closed, True)

        self.room.players.set(
            [
                self.players["player_1"],
                self.players["player_2"],
                self.players["player_3"],
            ]
        )
        self.room.close_room()
        self.assertIs(self.room.is_closed, True)

        self.room.players.set(
            [
                self.players["player_1"],
                self.players["player_2"],
                self.players["player_3"],
                self.players["player_4"],
            ]
        )
        self.room.close_room()
        self.assertIs(self.room.is_closed, True)

        self.room.players.set(
            [
                self.players["player_1"],
                self.players["player_2"],
                self.players["player_3"],
                self.players["player_4"],
                self.players["player_5"],
            ]
        )
        self.room.close_room()
        self.assertIs(self.room.is_closed, True)

        self.room.players.set(
            [
                self.players["player_1"],
                self.players["player_2"],
                self.players["player_3"],
                self.players["player_4"],
                self.players["player_5"],
                self.players["player_6"],
            ]
        )
        self.room.close_room()
        self.assertIs(self.room.is_closed, True)

        self.room.players.set(
            [
                self.players["player_1"],
                self.players["player_2"],
                self.players["player_3"],
                self.players["player_4"],
                self.players["player_5"],
                self.players["player_6"],
                self.players["player_7"],
            ]
        )
        self.room.close_room()
        self.assertIs(self.room.is_closed, False)

    def test_next_turn(self):
        self.room.players.set(
            [
                self.players["player_1"],
                self.players["player_2"],
                self.players["player_3"],
            ]
        )
        
        self.room.current_turn_player = self.players["player_1"]
        self.room.save()

        self.room.next_turn()
        self.assertEqual(self.room.current_turn_player, self.players["player_2"])

        self.room.next_turn()
        self.assertEqual(self.room.current_turn_player, self.players["player_3"])

        self.room.next_turn()
        self.assertEqual(self.room.current_turn_player, self.players["player_1"])