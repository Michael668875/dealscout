from django.db import models
from django.utils import timezone

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
    flat_name = models.CharField(max_length=100, db_index=True, null=True)

    class Meta:
        db_table = "brands"

    def __str__(self):
        return self.name


class CanonModel(models.Model):
    brand = models.ForeignKey(
        CanonBrand,
        on_delete=models.CASCADE,
        related_name="models",
    )

    name = models.CharField(max_length=255)
    flat_name = models.CharField(max_length=100, db_index=True, null=True)
    slug = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "models"
        constraints = [
            models.UniqueConstraint(
                fields=["brand", "name"],
                name="uq_brand_model",
            )
        ]
        
    def __str__(self):
        return f"{self.brand.name} {self.name}"

    @property
    def display_name(self):
        return f"{self.brand.name} {self.name}"



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
        db_index=True,
        choices=STATUS_CHOICES,
    )

    affiliate_url = models.TextField(blank=True, null=True)

    last_seen = models.DateTimeField(default=timezone.now)

    miss_count = models.IntegerField(default=0, blank=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    last_updated = models.DateTimeField(auto_now=True)

    model = models.ForeignKey(
        CanonModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listings",
    )

    class Meta:
        db_table = "listings"
        indexes = [
            models.Index(
                fields=["status", "marketplace"],
                name="ix_listings_marketplace_setnum",
            ),
        ]

    def __str__(self):
        return self.title or self.ebay_item_id


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

