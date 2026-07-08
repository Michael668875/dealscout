from django.contrib import admin

from .models import CanonBrand, Listing, PriceHistory, TempSummary, Specs

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_filter = ["country"]

class SpecsAdmin(admin.ModelAdmin):
    list_display = (
        "listing",
        "brand",
        "layout_size",
        "wireless",
        "hall_effect",
        "low_profile",
    )

    search_fields = (
        "listing__title",
        "brand__name",
    )

    list_filter = (
        "brand",
        "layout_size",
        "wireless",
        "hall_effect",
        "low_profile",
    )


admin.site.register(Listing, ListingAdmin)
admin.site.register(CanonBrand)
admin.site.register(PriceHistory)
admin.site.register(TempSummary)
admin.site.register(Specs, SpecsAdmin)
