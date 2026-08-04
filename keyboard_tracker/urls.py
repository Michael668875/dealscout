from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="index"),
    path("listings/", views.ListingView.as_view(), name="listings"),
    path("pricedrops/", views.PriceDropsView.as_view(), name="pricedrops"),
    path("brands/", views.BrandsView.as_view(), name="brands"),    
    path("brands/<slug:slug>/", views.SingleBrandView.as_view(), name="brand"),    
    path("features/", views.FeaturesView.as_view(), name="features"),    
    path("features/<slug:slug>/", views.FeaturesView.as_view(), name="feature"),    
    path("sizes/", views.SizesView.as_view(), name="sizes"),    
    path("sizes/<slug:slug>/", views.SizesView.as_view(), name="size"),    
    path("switches/", views.SwitchesView.as_view(), name="switches"),    
    path("switches/<slug:slug>/", views.SwitchesView.as_view(), name="switch"),
    path("search/", views.SearchView.as_view(), name="search"),  
]