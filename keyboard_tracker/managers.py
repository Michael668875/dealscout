from django.db import models
from django.db.models import Window, ExpressionWrapper, FloatField, F
from django.db.models.functions import Lag

class PriceHistoryManager(models.Manager):

    def drops(self, country=None):
        queryset = (
            self.get_queryset()
            .filter(
                listing__status="ACTIVE",
            )
            .annotate(
                old_price=Window(
                    expression=Lag("price"),
                    partition_by=[F("listing")],
                    order_by=[
                        F("recorded_at").asc(),
                        F("id").asc(),
                    ],
                )
            )
            .filter(
                old_price__isnull=False,
                price__lt=F("old_price"),
            )
            .annotate(
                discount_percent=ExpressionWrapper(
                    (F("old_price") - F("price")) * 100 / F("old_price"),
                    output_field=FloatField(),
                )
            )
            .select_related("listing")
        )

        if country:
            queryset = queryset.filter(listing__country=country)

        return queryset.order_by("-discount_percent")
    

class ListingQuerySet(models.QuerySet):
    def filter_country(self, country):
        if country:
            return self.filter(country=country)
        return self


class ListingManager(models.Manager):
    def get_queryset(self):
        return ListingQuerySet(self.model, using=self._db)

    def listings(self, country=None):
        return (
            self.get_queryset()
            .filter_country(country)
            .order_by("-last_updated")
        )
    
class CanonBrandManager(models.Manager):
    def all_brands(self, country=None):

        filters = {"specs__listing__status": "ACTIVE",}
        
        if country:
            filters["specs__listing__country"] = country

        return (
            self.get_queryset()
            .filter(**filters)
            .distinct()
            .order_by("name")
        )
        

FEATURES = {    # I don't need this anymore
    "hall-effect": ("Hall Effect", "hall_effect"),
    "hot-swap": ("Hot Swap", "hot_swap"),
    "wireless": ("Wireless", "wireless"),
    "bluetooth": ("Bluetooth", "bluetooth"),
    "rgb": ("RGB", "rgb"),
    "gasket-mount": ("Gasket Mount", "gasket_mount"),
    "low-profile": ("Low Profile", "low_profile"),
    "optical": ("Optical", "optical"),
    "knob": ("Knob", "knob"),
    "qmk": ("QMK", "qmk"),
    "via": ("VIA", "via"),
    "iso": ("ISO", "iso"),
    "ansi": ("ANSI", "ansi"),
    "barebones": ("Barebones", "barebones"),
}


class SpecsManager(models.Manager):

    def brand_list(self, slug, country=None):

        filters = {
            "listing__status": "ACTIVE",
            "brand__slug": slug,
            }

        if country:
            filters["listing__country"] = country

        return (
            self.get_queryset()
            .filter(**filters)
            .select_related("listing")
            .order_by("listing__last_updated")
        )
    
    # advanced search function
    def advanced_search(self, country=None,brands=None, switches=None, sizes=None, features=None):

        queryset = self.get_queryset()

        filters = {
            "listing__status": "ACTIVE",
        }

        if country:
            filters["listing__country"] = country

        if brands:
            filters["brand__slug__in"] = brands

        queryset = queryset.filter(**filters)

        if switches:
            queryset = queryset.filter(
                values__specification__category="switch",
                values__specification__slug__in=switches,
            )

        if sizes:
            queryset = queryset.filter(
                values__specification__category="size",
                values__specification__slug__in=sizes,
            )

        if features:
            queryset = queryset.filter(
                values__specification__category="feature",
                values__specification__slug__in=features,
            )

        return (
            queryset
            .select_related(
                "listing",
                "brand"
            )
            .prefetch_related(
                "values__specification"
            )
            .distinct()
            .order_by(
                "listing__last_updated"
            )
        )