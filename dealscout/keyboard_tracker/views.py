from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Listing

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