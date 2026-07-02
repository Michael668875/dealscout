from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/", views.ListingView.as_view(), name="listings"),
]