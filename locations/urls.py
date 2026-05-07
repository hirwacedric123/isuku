from django.urls import path

from .views import location_overview

app_name = "locations"

urlpatterns = [
    path("overview/", location_overview, name="overview"),
]
