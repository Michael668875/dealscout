import logging

from django.core.management.base import BaseCommand, CommandError

from keyboard_tracker.ebay.fetch import fetch_summaries
from keyboard_tracker.ebay.importer import save_temp_summaries
from keyboard_tracker.ebay.pipeline import run_pipeline
from keyboard_tracker.ebay.sql import truncate_temp_summaries
from keyboard_tracker.ebay.transformations import create_price_drops

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    help = "Fetch latest eBay listings"

    def handle(self, *args, **options):
        logger.info("Starting eBay import...")

        try:
#            logger.info("Clearing temp tables...")
#            truncate_temp_summaries()
#
#            logger.info("Fetching from eBay...")
#            items = fetch_summaries()
#
#            logger.info(
#                f"Fetched {len(items)} listings."
#            )
#
#            logger.info("Saving temp summaries...")
#            save_temp_summaries(items)

            logger.info("Running pipeline...")
            run_pipeline()

            logger.info("Making transformations...")
            create_price_drops()

        except Exception as e:
            raise CommandError(str(e))


        logger.info(
            self.style.SUCCESS(
                "Import completed successfully."
            )
        )
