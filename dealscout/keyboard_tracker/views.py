from django.shortcuts import render
from django.http import HttpResponse
from .models import Listing

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def listings(request):
    listings = Listing.objects.all()
    return render(request, "keyboard_tracker/listings.html", {
        "listings": listings,
    })