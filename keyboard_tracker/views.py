from django.views.generic import ListView, RedirectView, TemplateView
from .models import Listing, PriceHistory, CanonBrand, Specs, Specification

# Create your views here.

class Home(RedirectView):
    pattern_name = "listings"
    permanent = True

class ListingView(ListView):
    template_name = "keyboard_tracker/listings.html"
    paginate_by = 40

    def get_queryset(self):
        country = self.request.GET.get("country", "US")
        return Listing.objects.listings(country)
    
    
class PriceDropsView(ListView):
    template_name = "keyboard_tracker/pricedrops.html"
    paginate_by = 40
    #context_object_name = "drops"

    def get_queryset(self):
        country = self.request.GET.get("country", "US")
        return PriceHistory.objects.drops(country)    
    
    
class BrandsView(ListView):
    template_name = "keyboard_tracker/brands.html"

    def get_queryset(self):
        country = self.request.GET.get("country", "US")
        return CanonBrand.objects.all_brands(country)

class SingleBrandView(ListView):
    template_name = "keyboard_tracker/brand.html"
    paginate_by = 40

    def get_queryset(self):
            return Specs.objects.brand_list(
                slug=self.kwargs["slug"],
                country = self.request.GET.get("country", "US"),
            )

class AdvancedSearchView(TemplateView):
    template_name = "keyboard_tracker/advanced_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        country = self.request.GET.get("country", "US")

        context["country"] = country

        context["brands"] = CanonBrand.objects.all_brands(country=country)


        # Switches

        context["switches"] = (
            Specification.objects
            .filter(
                category="switch"
            )
            .order_by("name")
        )


        # Sizes

        context["sizes"] = (
            Specification.objects
            .filter(
                category="size"
            )
            .order_by("name")
        )


        # Features

        context["features"] = (
            Specification.objects
            .filter(
                category="feature"
            )
            .order_by("name")
        )

        return context

class SearchResultsView(ListView):
    template_name = "keyboard_tracker/search_results.html"
    context_object_name = "specs"
    paginate_by = 40

    def get_queryset(self):
        country = self.request.GET.get("country", "US")

        brands = self.request.GET.getlist("brands")
        switches = self.request.GET.getlist("switches")
        sizes = self.request.GET.getlist("sizes")
        features = self.request.GET.getlist("features")

        return Specs.objects.advanced_search(
            country=country,
            brands=brands,
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
    paginate_by = 40

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        country = self.request.GET.get("country", "US")

        queryset = Listing.objects.listings(country=country)

        if query:
            queryset = queryset.filter(title__icontains=query)

        return queryset

# static pages

class AboutView(TemplateView):
    template_name = "keyboard_tracker/about.html"


class HowItWorksView(TemplateView):
    template_name = "keyboard_tracker/how_it_works.html"


class AffiliateDisclosureView(TemplateView):
    template_name = "keyboard_tracker/affiliate_disclosure.html"


class DisclaimerView(TemplateView):
    template_name = "keyboard_tracker/disclaimer.html"


class PrivacyView(TemplateView):
    template_name = "keyboard_tracker/privacy.html"


class TermsView(TemplateView):
    template_name = "keyboard_tracker/terms.html"


class ContactView(TemplateView):
    template_name = "keyboard_tracker/contact.html"