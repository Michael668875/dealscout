from django.contrib import admin

from .models import CanonBrand, CanonModel, Product, Listing, PriceHistory, ModelAlias, TempSummary

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_filter = ["country"]

admin.site.register(Listing, ListingAdmin)
admin.site.register(CanonBrand)
admin.site.register(CanonModel)
admin.site.register(Product)
admin.site.register(PriceHistory)
admin.site.register(ModelAlias)
admin.site.register(TempSummary)
