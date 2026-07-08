from keyboard_tracker.models import Listing, Specs, CanonBrand
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Parse keyboard specs from listing titles"

    def handle(self, *args, **options):
        parse_keyboard_specs()
        self.stdout.write(
            self.style.SUCCESS("Specs parsed successfully")
        )

def parse_keyboard_specs(): # SIMPLE PARSING. TO BE UPDATED LATER
    listings = Listing.objects.filter(status="ACTIVE")

    brands = CanonBrand.objects.all()

    for listing in listings:
        title = listing.title.lower()

        specs = Specs(
            listing=listing
        )

        # Brand matching
        for brand in brands:
            if brand.name.lower() in title:
                specs.brand = brand
                break

        # Layout
        if "60%" in title:
            specs.layout_size = "60%"
        elif "65%" in title:
            specs.layout_size = "65%"
        elif "75%" in title:
            specs.layout_size = "75%"
        elif "tkl" in title:
            specs.layout_size = "TKL"
        elif "full size" in title:
            specs.layout_size = "Full Size"

        # Switch type examples
        if "hall effect" in title:
            specs.switch_type = "Hall Effect"
        elif "optical" in title:
            specs.switch_type = "Optical"
        elif "red switch" in title:
            specs.switch_type = "Red"
        elif "brown switch" in title:
            specs.switch_type = "Brown"
        elif "blue switch" in title:
            specs.switch_type = "Blue"

        # Features
        specs.low_profile = "low profile" in title
        specs.hall_effect = "hall effect" in title
        specs.optical = "optical" in title
        specs.hot_swap = "hot swap" in title or "hotswap" in title
        specs.gasket_mount = "gasket" in title
        specs.knob = "knob" in title

        # Connectivity
        specs.wireless = "wireless" in title
        specs.bluetooth = "bluetooth" in title

        # Firmware
        specs.qmk = "qmk" in title
        specs.via = "via" in title

        # Layout standards
        specs.iso = "iso" in title
        specs.ansi = "ansi" in title

        # Build type
        specs.barebones = "barebones" in title

        # Lighting
        specs.rgb = "rgb" in title

        specs.save()
