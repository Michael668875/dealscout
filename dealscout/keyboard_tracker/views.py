from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from .models import Listing, PriceHistory, CanonBrand
from django.db.models import Count, Min, Max, Avg, F, OuterRef, Subquery, ExpressionWrapper, FloatField, Window
from django.db.models.functions import Lag
from collections import defaultdict

# Create your views here.


def index(request):
    return HttpResponseRedirect("listings/")

#def listings(request):
#    listings = Listing.objects.all()
#    return render(request, "keyboard_tracker/listings.html", {
#        "listings": listings,
#    })

class ListingView(generic.ListView):
    template_name = "keyboard_tracker/listings.html"
    context_object_name = "listings"

    def get_queryset(self):
        return Listing.objects.all()


class OverView(generic.ListView):
    template_name = "keyboard_tracker/overview.html"
    context_object_name = "models"

    def get_queryset(self):
        return (
            Listing.objects
            .filter(
                status="ACTIVE",
               # model__isnull=False,
            )
            .values(
                "title",
                "image_urls",
               # "model_id",
               # "model__name",
               # "model__brand__name",
               # "model__slug",
            )
            .annotate(
                listing_count=Count("id"),
                lowest_price=Min("price"),
            )
           # .order_by("model__brand__name", "model__name")
        )


class BestDealsView(generic.ListView):
    model = Listing
    template_name = "keyboard_tracker/bestdeals.html"
    context_object_name = "listings"

    def get_queryset(self):
        avg_price_subquery = (
            Listing.objects
            .filter(
               # model=OuterRef("model"),
                status="ACTIVE",
            )
          #  .values("model")
            .annotate(avg_price=Avg("price"))
            .values("avg_price")[:1]
        )

        return (
            Listing.objects
            .filter(status="ACTIVE")
            .annotate(
                avg_price=Subquery(avg_price_subquery)
            )
            .annotate(
                discount=ExpressionWrapper(
                    (F("avg_price") - F("price")) * 100 / F("avg_price"),
                    output_field=FloatField(),
                )
            )
            .filter(price__lte=F("avg_price") * 0.75)
            .order_by("-discount")
        )
    
class PriceDropsView(generic.ListView):
    model = PriceHistory
    template_name = "keyboard_tracker/pricedrops.html"
    context_object_name = "drops"

    def get_queryset(self):
        return (
            PriceHistory.objects
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
    
    
class ModelsView(generic.ListView):
    model = CanonBrand
    template_name = "keyboard_tracker/models.html"
    context_object_name = "brands"

    def get_queryset(self):
        return CanonBrand.objects.all()

        # rows = (
        #     Listing.objects
        #     .filter(
        #         status="ACTIVE",
        #         model__isnull=False,
        #     )
        #     .values(
        #         "model__id",
        #         "model__name",
        #         "model__brand__name",
        #     )
        #     .annotate(
        #         count=Count("id"),
        #         last_seen=Max("last_seen"),
        #     )
        #     .order_by("-count")
        # )

        # grouped = defaultdict(list)

        # for row in rows:
        #     grouped[row["model__brand__name"]].append(row)

        # return [
        #     {
        #         "name": brand,
        #         "models": models,
        #     }
        #     for brand, models in grouped.items()
        # ]
