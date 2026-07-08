from django.core.management.base import BaseCommand, CommandError

from keyboard_tracker.ebay.fetch import fetch_summaries
from keyboard_tracker.ebay.importer import save_temp_summaries
from keyboard_tracker.ebay.pipeline import run_pipeline
from keyboard_tracker.ebay.sql import truncate_temp_summaries


class Command(BaseCommand):

    help = "Fetch latest eBay listings"

    def handle(self, *args, **options):

        try:
            self.stdout.write("Clearing temp tables...")
            truncate_temp_summaries()

            self.stdout.write("Fetching from eBay...")
            items = fetch_summaries()

            self.stdout.write(
                f"Fetched {len(items)} listings."
            )

            self.stdout.write("Saving temp summaries...")
            save_temp_summaries(items)

            self.stdout.write("Running pipeline...")
            run_pipeline()

        except Exception as e:
            raise CommandError(str(e))


        self.stdout.write(
            self.style.SUCCESS(
                "Import completed successfully."
            )
        )