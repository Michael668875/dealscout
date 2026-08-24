
from django.core.management.base import BaseCommand
from keyboard_tracker.services.spec_parser import parse_keyboard_specs


class Command(BaseCommand):
    help = "Parse keyboard specs from listing titles"

    def handle(self, *args, **options):
        parse_keyboard_specs()
        self.stdout.write(
            self.style.SUCCESS("Specs parsed successfully")
        )

