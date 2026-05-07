from django.urls import path

from .views import complete_route, contractor_dashboard, generate_route, route_detail

app_name = "routing"

urlpatterns = [
    path("dashboard/", contractor_dashboard, name="dashboard"),
    path("generate/", generate_route, name="generate_route"),
    path("<int:route_id>/", route_detail, name="route_detail"),
    path("<int:route_id>/complete/", complete_route, name="complete_route"),
]
