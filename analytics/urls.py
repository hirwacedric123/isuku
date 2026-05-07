from django.urls import path

from .views import admin_dashboard, export_reports_csv

app_name = "analytics"

urlpatterns = [
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("exports/reports.csv", export_reports_csv, name="export_reports_csv"),
]
