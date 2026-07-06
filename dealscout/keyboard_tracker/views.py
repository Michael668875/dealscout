from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from .models import Listing
from django.db.models import Count, Min

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
        
    
class BestdealsView(generic.ListView):
    template_name = "keyboard_tracker/bestdeals.html"
    context_object_name = "listings"

    def get_queryset(self):
        return Listing.objects.all()
    
class PricedropsView(generic.ListView):
    template_name = "keyboard_tracker/pricedrops.html"
    context_object_name = "listings"

    def get_queryset(self):
        return Listing.objects.all()
    
    
class ModelsView(generic.ListView):
    template_name = "keyboard_tracker/models.html"
    context_object_name = "listings"

    def get_queryset(self):
        return Listing.objects.all()
