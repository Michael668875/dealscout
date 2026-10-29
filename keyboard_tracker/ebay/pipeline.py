from django.db import transaction

from keyboard_tracker.services.spec_parser import parse_keyboard_specs

import logging
import time

logger = logging.getLogger(__name__)

from .sql import (
    insert_listings,
    update_listing_prices,
    insert_price_history,
    update_seen_listings,
    mark_sold_listings,
    increment_miss_count,
    mark_ended_listings,
)


def run_pipeline():
    """
    Synchronise temp_summaries with the permanent tables.
    """

    with transaction.atomic():

        insert_listings()

        update_listing_prices()

        insert_price_history()

        update_seen_listings()

        mark_sold_listings()

        increment_miss_count()

        mark_ended_listings()

        start = time.perf_counter()
        parse_keyboard_specs()
        logger.info(
            "Parsed keyboard specs in %.2f seconds",
            time.perf_counter() - start,
        )
