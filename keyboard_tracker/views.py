from django.http import HttpResponseRedirect
from django.views import generic
from .models import Listing, PriceHistory, CanonBrand, Specs

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
    paginate_by = 50

    def get_queryset(self):
        country = self.request.GET.get("country")
        return Listing.objects.listings(country)
    
class PriceDropsView(generic.ListView):
    template_name = "keyboard_tracker/pricedrops.html"
    context_object_name = "drops"

    def get_queryset(self):
        country = self.request.GET.get("country")
        return PriceHistory.objects.drops(country)    
    
class BrandsView(generic.ListView):
    template_name = "keyboard_tracker/brands.html"
    context_object_name = "brands"

    def get_queryset(self):
        country = self.request.GET.get("country")
        return CanonBrand.objects.all_brands(country)

class BrandView(generic.ListView):
    template_name = "keyboard_tracker/brand.html"
    context_object_name = "listings"

    def get_queryset(self):
        country = self.request.GET.get("country")
        slug = self.kwargs["slug"]
        return Specs.objects.brand_list(slug=slug, country=country)
    
    

    
class FeaturesView(generic.ListView):
    template_name = "keyboard_tracker/features.html"
    context_object_name = "features"

    def get_queryset(self):
        country = self.request.GET.get("country")
        return Listing.objects.all()
    
class SizesView(generic.ListView):
    model = Specs
    template_name = "keyboard_tracker/sizes.html"
    context_object_name = "sizes"

    def get_queryset(self):
        country = self.request.GET.get("country")
        return Specs.objects.all()
    
class SwitchesView(generic.ListView):
    model = Specs
    template_name = "keyboard_tracker/switches.html"
    context_object_name = "switches"

    def get_queryset(self):
        country = self.request.GET.get("country")
        return Specs.objects.all()
    
