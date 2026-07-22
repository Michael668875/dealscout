from django.db import models
from django.db.models import Window, ExpressionWrapper, FloatField, F
from django.db.models.functions import Lag
from django.utils.text import slugify

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
            .order_by("id")
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
    
    def all_sizes(self, country=None):

        filters = {"listing__status": "ACTIVE",}

        if country:
            filters["listing__country"] = country

        return (
            self.get_queryset()
            .filter(**filters)
            .exclude(layout_size="")
            .exclude(layout_size__isnull=True)
            .values_list("layout_size", flat=True)
            .distinct()
            .order_by("layout_size")
        )
        
    def size_list(self, slug, country=None):
        filters = {"listing__status": "ACTIVE"}

        if country:
            filters["listing__country"] = country

        queryset = self.get_queryset().filter(**filters)

        for value in queryset.values_list("layout_size", flat=True).distinct():
            if slugify(value) == slug:
                return queryset.filter(layout_size=value)

        return queryset.none()