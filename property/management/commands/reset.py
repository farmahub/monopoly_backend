from django.core.management.base import BaseCommand

from property.models import Property
from account.models import User
from player.models import Player


class Command(BaseCommand):
    help = (
        "resets cash for every player "
        "to initail amount and sets the owner "
        "for every property the Bank"
    )

    def handle(self, *args, **options):
        try:
            users = User.objects.all()
            properties = Property.objects.all()

            for user in users:
                player = Player.objects.get(user_id=user.id)
                if user.username == "bank":
                    player.cash = 1000000
                    player.save()
                else:
                    player.cash = 1500
                    player.save()

            for property in properties:
                property.owner = User.objects.get(username="bank")
                property.save()

            self.stdout.write(
                self.style.SUCCESS("RESET SITUATION IS HANDLED SUCCESSFULLY")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR("RESET SITUATION IS FAILED"))
