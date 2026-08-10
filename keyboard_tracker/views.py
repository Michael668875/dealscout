from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, RedirectView, TemplateView
from django.utils.text import slugify
from .models import Listing, PriceHistory, CanonBrand, Specs

# Create your views here.

class Home(RedirectView):
    pattern_name = "listings"
    permanent = True

# def index(request):
    # return HttpResponseRedirect("listings/")

#def listings(request):
#    listings = Listing.objects.all()
#    return render(request, "keyboard_tracker/listings.html", {
#        "listings": listings,
#    })

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

# class AdvancedSearchView(TemplateView):
#     template_name = "keyboard_tracker/advanced_search.html"

#     def get_queryset(self):
#         country = self.request.GET.get("country")
#         return Specs.objects.all_features(country)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         country = self.request.GET.get("country")

#         context["features"] = Specs.objects.get()
        
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
    
    
# class FeaturesView(ListView):
#     template_name = "keyboard_tracker/features.html"
#     #context_object_name = "features"

#     def get_queryset(self):
#         country = self.request.GET.get("country")
#         return Specs.objects.all_features(country)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         country = self.request.GET.get("country")
#         slug = self.kwargs.get("slug")

#         # Dictionary is already created in all_features. Just call it.
#         # no need to use slugify as the dictionary already stores slug
#         context["features"] = Specs.objects.all_features(country)

#         if slug:
#             context["listings"] = Specs.objects.feature_list(
#                 slug=slug,
#                 country=country,
#             )
#         else:
#             context["listings"] = Specs.objects.none()

#         return context
    
    
# class SizesView(ListView):
#     template_name = "keyboard_tracker/sizes.html"
#     #context_object_name = "sizes"

#     def get_queryset(self):
#         country = self.request.GET.get("country")
#         return Specs.objects.all_sizes(country)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         country = self.request.GET.get("country")
#         slug = self.kwargs.get("slug")

#         context["sizes"] = [
#             {
#                 "name": size,
#                 "slug": slugify(size),
#             }
#             for size in Specs.objects.all_sizes(
#                 self.request.GET.get("country")
#             )
#         ]

#         if slug:
#             context["listings"] = Specs.objects.size_list(
#                 slug=slug,
#                 country=country,
#             )
#         else:
#             context["listings"] = Specs.objects.none()


#         return context
    

# class SwitchesView(ListView):
#     template_name = "keyboard_tracker/switches.html"
#     #context_object_name = "switches"

#     def get_queryset(self):
#         country = self.request.GET.get("country")
#         return Specs.objects.all_switches(country)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         country = self.request.GET.get("country")
#         slug = self.kwargs.get("slug")

#         context["switches"] = [
#             {
#                 "name": switch,
#                 "slug": slugify(switch),
#             }
#             for switch in Specs.objects.all_switches(
#                 self.request.GET.get("country")
#             )
#         ]

#         if slug:
#             context["listings"] = Specs.objects.switches_list(
#                 slug=slug,
#                 country=country,
#             )
#         else:
#             context["listings"] = Specs.objects.none()

#         return context

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

