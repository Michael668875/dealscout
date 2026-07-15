from django.core.management.base import BaseCommand
from django.utils.text import slugify

from keyboard_tracker.models import CanonBrand


class Command(BaseCommand):
    help = "Populate slug field for all brands."

    def handle(self, *args, **options):
        used_slugs = set()

        for brand in CanonBrand.objects.all():
            slug = slugify(brand.name)

            # Ensure uniqueness
            original_slug = slug
            counter = 2
            while slug in used_slugs or CanonBrand.objects.exclude(pk=brand.pk).filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            brand.slug = slug
            brand.save(update_fields=["slug"])
            used_slugs.add(slug)

            self.stdout.write(f"{brand.name} -> {slug}")

        self.stdout.write(self.style.SUCCESS("Brand slugs created successfully."))