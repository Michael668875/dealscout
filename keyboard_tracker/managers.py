from django.db import models
from django.db.models import Window, ExpressionWrapper, FloatField, F
from django.db.models.functions import Lag

class PriceHistoryManager(models.Manager):

    def drops(self):
        return (
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
            .order_by("-discount_percent")
        )
