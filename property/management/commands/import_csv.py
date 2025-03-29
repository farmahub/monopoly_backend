from django.core.management.base import BaseCommand
import csv
from property.models import Property
from account.models import User


class Command(BaseCommand):
    help = "Imports a csv file into model"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to csv file")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        try:
            with open(csv_file, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    Property.objects.create(
                        name=row["name"],
                        position=int(row["index"]),
                        color=row["color"],
                        type=row["type"],
                        price=int(row["price"]),
                        rent_single=int(row["rentSingle"]),
                        rent_set=int(row["rentSet"]),
                        rent_1=int(row["rent1"]),
                        rent_2=int(row["rent2"]),
                        rent_3=int(row["rent3"]),
                        rent_4=int(row["rent4"]),
                        rent_5=int(row["rent5"]),
                        loan_amount=int(row["loan"]),
                        loan_back_amount=int(row["loanBack"]),
                        house_price=int(row["housePrice"]),
                        hotel_price=int(row["hotelPrice"]),
                        owner=User.objects.get(email="admin@example.com"),
                    ),
            self.stdout.write(self.style.SUCCESS("Data imported successfully!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing data: {e}"))
