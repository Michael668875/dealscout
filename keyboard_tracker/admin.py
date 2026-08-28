from django.contrib import admin

from .models import CanonBrand, Listing, PriceHistory, TempSummary, Specs, Specification, SpecValue

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_filter = ["country"]


admin.site.register(Listing, ListingAdmin)
admin.site.register(PriceHistory)
admin.site.register(TempSummary)

@admin.register(CanonBrand)
class CanonBrandAdmin(admin.ModelAdmin):

    search_fields = (
        "name",
    )

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "category",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "slug",
    )

    ordering = (
        "category",
        "name",
    )

class SpecValueInline(admin.TabularInline):

    model = SpecValue

    extra = 0

    autocomplete_fields = (
        "specification",
    )

@admin.register(Specs)
class SpecsAdmin(admin.ModelAdmin):

    list_display = (
        "listing",
        "brand",
        "get_specifications",
        "created_at",
    )

    list_filter = (
        "brand",
    )

    search_fields = (
        "listing__title",
        "brand__name",
    )

    autocomplete_fields = (
        "brand",
    )

    inlines = (
        SpecValueInline,
    )


    @admin.display(
        description="Specifications"
    )
    def get_specifications(self, obj):

        return ", ".join(
            obj.values
            .select_related(
                "specification"
            )
            .values_list(
                "specification__name",
                flat=True
            )
        )
