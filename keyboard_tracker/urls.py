from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/", views.ListingView.as_view(), name="listings"),
    path("pricedrops/", views.PriceDropsView.as_view(), name="pricedrops"),
    path("brands/", views.BrandsView.as_view(), name="brands"),    
    path("brands/<slug:slug>/", views.BrandsView.as_view(), name="brand"),    
    path("features/", views.FeaturesView.as_view(), name="features"),    
    path("sizes/", views.SizesView.as_view(), name="sizes"),    
    path("switches/", views.SwitchesView.as_view(), name="switches"),    
]