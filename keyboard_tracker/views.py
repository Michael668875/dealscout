from django.views.generic import ListView, RedirectView, TemplateView
from .models import Listing, PriceHistory, CanonBrand, Specs

# Create your views here.

class Home(RedirectView):
    pattern_name = "listings"
    permanent = True

class ListingView(ListView):
    template_name = "keyboard_tracker/listings.html"
    paginate_by = 50

    def get_queryset(self):
        country = self.request.GET.get("country")
        return Listing.objects.listings(country)
    
    
class PriceDropsView(ListView):
    template_name = "keyboard_tracker/pricedrops.html"
    #context_object_name = "drops"

    def get_queryset(self):
        country = self.request.GET.get("country")
        return PriceHistory.objects.drops(country)    
    
    
class BrandsView(ListView):
    template_name = "keyboard_tracker/brands.html"

    def get_queryset(self):
        country = self.request.GET.get("country")
        return CanonBrand.objects.all_brands(country)

class SingleBrandView(ListView):
    template_name = "keyboard_tracker/brand.html"

    def get_queryset(self):
            return Specs.objects.brand_list(
                slug=self.kwargs["slug"],
                country=self.request.GET.get("country"),
            )

class AdvancedSearchView(TemplateView):
    template_name = "keyboard_tracker/advanced_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        country = self.request.GET.get("country")

        specs = Specs.objects.filter(
            listing__status="ACTIVE"
        )

        context["country"] = country

        context["switches"] = (
            specs
            .filter(switch_type__isnull=False)
            .exclude(switch_type="")
            .values_list("switch_type", flat=True)
            .distinct()
            .order_by("switch_type")
        )

        context["sizes"] = (
            specs
            .filter(layout_size__isnull=False)
            .exclude(layout_size="")
            .values_list("layout_size", flat=True)
            .distinct()
            .order_by("layout_size")
        )

        context["features"] = [
            ("low_profile", "Low Profile"),
            ("hall_effect", "Hall Effect"),
            ("optical", "Optical"),
            ("hot_swap", "Hot Swap"),
            ("gasket_mount", "Gasket Mount"),
            ("knob", "Knob"),
            ("wireless", "Wireless"),
            ("bluetooth", "Bluetooth"),
            ("qmk", "QMK"),
            ("via", "VIA"),
            ("iso", "ISO"),
            ("ansi", "ANSI"),
            ("barebones", "Barebones"),
            ("rgb", "RGB"),
        ]

        return context

class SearchResultsView(ListView):
    template_name = "keyboard_tracker/search_results.html"
    context_object_name = "specs"
    paginate_by = 50

    def get_queryset(self):
        country = self.request.GET.get("country")

        switches = self.request.GET.getlist("switches")
        sizes = self.request.GET.getlist("sizes")
        features = self.request.GET.getlist("features")

        return Specs.objects.advanced_search(
            country=country,
            switches=switches,
            sizes=sizes,
            features=features,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        params = self.request.GET.copy()
        params.pop("page", None)

        context["search_params"] = params.urlencode()

        return context
    
    
class SearchView(ListView):
    model = Listing
    template_name = "keyboard_tracker/search.html"
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()

        queryset = Listing.objects.listings(
            country = self.request.GET.get("country")
        )

        if queryset:
            queryset = queryset.filter(title__icontains=query)

        return queryset

