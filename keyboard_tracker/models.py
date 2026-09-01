from django.db import models
from django.utils import timezone
from .managers import (
    PriceHistoryManager, 
    ListingManager, 
    CanonBrandManager, 
    SpecsManager,
    )

CURRENCY_SYMBOLS = {
    "USD": "$",
    "AUD": "$",
    "GBP": "£",
    "EUR": "€",
}

# Create your models here.


class TempSummary(models.Model):
    ebay_item_id = models.CharField(max_length=255, unique=True)

    title = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10)

    condition = models.CharField(max_length=255, blank=True, null=True)
    buying_options = models.JSONField(blank=True, null=True)

    image_urls = models.JSONField(blank=True, null=True)

    item_url = models.TextField(blank=True, null=True)
    affiliate_url = models.TextField(blank=True, null=True)

    seller_username = models.CharField(max_length=100, blank=True, null=True)
    seller_feedback_score = models.IntegerField(blank=True, null=True)
    seller_feedback_percent = models.FloatField(blank=True, null=True)

    categories = models.JSONField(blank=True, null=True)

    marketplace = models.CharField(max_length=100, blank=True, null=True)

    item_country = models.CharField(max_length=2, blank=True, null=True)
    item_city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    item_created_at = models.DateTimeField(blank=True, null=True)

    first_seen = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    sold_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "temp_summaries"

    def __str__(self):
        return self.title or self.ebay_item_id


class CanonBrand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    objects = CanonBrandManager()

    class Meta:
        db_table = "brands"

    def __str__(self):
        return self.name


class Listing(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("ENDED", "Ended"),
        ("SOLD", "Sold"),
    ]

    ebay_item_id = models.CharField(max_length=255, unique=True)

    title = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10)

    image_urls = models.JSONField(blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)

    marketplace = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        default="ACTIVE",
        choices=STATUS_CHOICES,
    )

    affiliate_url = models.TextField(blank=True, null=True)

    last_seen = models.DateTimeField(default=timezone.now)

    miss_count = models.IntegerField(default=0)
    ended_at = models.DateTimeField(blank=True, null=True)

    last_updated = models.DateTimeField(auto_now=True)

    objects = ListingManager()

    class Meta:
        db_table = "listings"
        indexes = [
            models.Index(
                fields=["status", "country", "-last_updated"],
                name="ix_status_country_updated",
            ),
        ]

    def __str__(self):
        return self.title or self.ebay_item_id

    @property
    def currency_symbol(self):
        return CURRENCY_SYMBOLS.get(self.currency, self.currency)


class PriceHistory(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="price_history",
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)

    recorded_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    objects = PriceHistoryManager()

    class Meta:
        db_table = "price_history"
        indexes = [
            models.Index(
                fields=["listing", "recorded_at", "id"],
                name="ix_pricehistory_listing_time",
            ),
        ]

    def __str__(self):
        return f"{self.listing.ebay_item_id}: {self.price}"


class Specification(models.Model):

    CATEGORY_CHOICES = (
        ("feature", "Feature"),
        ("size", "Size"),
        ("switch", "Switch"),
    )

    slug = models.SlugField(
        max_length=100
    )

    name = models.CharField(
        max_length=100
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["slug", "category"],
                name="unique_specification_slug_category"
            )
        ]

        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"


class Specs(models.Model):

    listing = models.OneToOneField(
        "Listing",
        on_delete=models.CASCADE,
        related_name="specs"
    )

    brand = models.ForeignKey(
        "CanonBrand",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="specs"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    objects = SpecsManager()
    
    class Meta:
        db_table = "specs"

    def get_features(self):

        return (
            self.values
            .filter(
                specification__category="feature"
            )
            .select_related(
                "specification"
            )
        )


    def get_sizes(self):

        return (
            self.values
            .filter(
                specification__category="size"
            )
            .select_related(
                "specification"
            )
        )


    def get_switches(self):

        return (
            self.values
            .filter(
                specification__category="switch"
            )
            .select_related(
                "specification"
            )
        )

    def __str__(self):
        return (
            f"Specs for ID: {self.listing.id} "
            f"Title: {self.listing.title}"
        )

class SpecValue(models.Model):

    specs = models.ForeignKey(
        Specs,
        on_delete=models.CASCADE,
        related_name="values"
    )

    specification = models.ForeignKey(
        Specification,
        on_delete=models.CASCADE,
        related_name="values"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["specs", "specification"],
                name="unique_specs_specification"
            )
        ]

    def __str__(self):
        return (
            f"{self.specs.listing.title}: "
            f"{self.specification.name}"
        )
