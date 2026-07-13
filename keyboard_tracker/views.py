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
        queryset = Listing.objects.order_by("id")

        country = self.request.GET.get("country")
        if country:
            queryset = queryset.filter(country=country)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_country"] = self.request.GET.get("country", "")
        context["countries"] = [
            ("AU", "Australia"),
            ("US", "United States"),
            ("GB", "United Kingdom"),
            ("DE", "Germany"),
        ]
        return context

    
class PriceDropsView(generic.ListView):
    model = PriceHistory
    template_name = "keyboard_tracker/pricedrops.html"
    context_object_name = "drops"
    queryset = PriceHistory.objects.drops()
    
    
class ModelsView(generic.ListView):
    model = CanonBrand
    template_name = "keyboard_tracker/models.html"
    context_object_name = "models"

    def get_queryset(self):
        return CanonBrand.objects.all()

class BrandsView(generic.ListView):
    model = CanonBrand
    template_name = "keyboard_tracker/brands.html"
    context_object_name = "brands"

    def get_queryset(self):
        return CanonBrand.objects.all()
    
class FeaturesView(generic.ListView):
    template_name = "keyboard_tracker/features.html"
    context_object_name = "features"

    def get_queryset(self):
        return Listing.objects.all()
    
class SizesView(generic.ListView):
    model = Specs
    template_name = "keyboard_tracker/sizes.html"
    context_object_name = "sizes"

    def get_queryset(self):
        return Specs.objects.all()
    
class SwitchesView(generic.ListView):
    model = Specs
    template_name = "keyboard_tracker/switches.html"
    context_object_name = "switches"

    def get_queryset(self):
        return Specs.objects.all()
    
