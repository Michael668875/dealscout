from django.db import transaction

from .sql import (
    insert_listings,
    update_listing_prices,
    insert_price_history,
    update_seen_listings,
    mark_sold_listings,
    increment_miss_count,
    mark_ended_listings,
)

from keyboard_tracker.management.commands.parse_specs import parse_keyboard_specs

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

        parse_keyboard_specs()
