from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/", views.ListingView.as_view(), name="listings"),
    path("overview/", views.OverView.as_view(), name="overview"),
    path("bestdeals/", views.BestdealsView.as_view(), name="bestdeals"),
    path("pricedrops/", views.PricedropsView.as_view(), name="pricedrops"),
    path("models/", views.ModelsView.as_view(), name="models"),    
]