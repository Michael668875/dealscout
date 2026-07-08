from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/", views.ListingView.as_view(), name="listings"),
    path("pricedrops/", views.PriceDropsView.as_view(), name="pricedrops"),
    path("models/", views.ModelsView.as_view(), name="models"),    
    path("brands/", views.BrandsView.as_view(), name="brands"),    
    path("features/", views.FeaturesView.as_view(), name="features"),    
    path("sizes/", views.SizesView.as_view(), name="sizes"),    
    path("switches/", views.SwitchesView.as_view(), name="switches"),    
]