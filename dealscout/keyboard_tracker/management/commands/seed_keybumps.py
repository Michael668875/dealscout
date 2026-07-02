import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from keyboard_tracker.models import CanonBrand, CanonModel


class Command(BaseCommand):
    help = "Seed CanonBrand and CanonModel from Keybumps CSV"

    def handle(self, *args, **options):

        csv_path = os.path.join(settings.BASE_DIR, "keyboard_models.csv")

        with open(csv_path, newline="", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for row in reader:
                brand_name = row["brand"].strip()
                model_name = row["model"].strip()

                brand, _ = CanonBrand.objects.get_or_create(
                    name=brand_name
                )

                CanonModel.objects.get_or_create(
                    brand=brand,
                    name=model_name,
                )

        self.stdout.write(self.style.SUCCESS("Seeding complete"))