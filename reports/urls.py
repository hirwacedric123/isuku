from django.urls import path

from .views import create_report, my_reports, update_status

app_name = "reports"

urlpatterns = [
    path("new/", create_report, name="create_report"),
    path("my/", my_reports, name="my_reports"),
    path("<int:report_id>/status/<str:status>/", update_status, name="update_status"),
]
