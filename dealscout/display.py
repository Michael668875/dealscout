import re
from keyboard_tracker.models import CanonBrand, CanonModel, Product, Listing

def flatten(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '', text)
    return text


def match_title(ebay_title):
    
    ebay_title = Listing.title

    flat_title = flatten(ebay_title)

    for brand in CanonBrand.objects.all():

        if brand.flat_name not in flat_title:
            continue

        models = CanonModel.objects.filter(brand=brand)

        for model in models:

            if model.flat_name in flat_title:
                product = Product.objects.get(model=model)

                Listing.product = product
                break



# preload db query

brands = {
    brand.flat_name: brand
    for brand in CanonBrand.objects.all()
}

models = (
    CanonModel.objects
    .select_related("brand")
)


# can skip matching brand and just look for model

for model in CanonModel.objects.select_related("brand"):

    if model.flat_name in flat_title:
        return Product.objects.get(model=model)
    

# even better create a parser class

class CanonParser:

    def __init__(self):
        self.models = (
            CanonModel.objects
            .select_related("brand", "product")
        )

    def parse(self, ebay_title):
        flat_title = flatten(ebay_title)

        for model in self.models:
            if model.flat_name in flat_title:
                return model.product

        return None
    
# scraper becomes clean

parser = CanonParser()

for listing in listings:

    product = parser.parse(listing.title)

    if product:
        listing.product = product
        listing.display_name = product.display_name