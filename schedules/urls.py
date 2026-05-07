from django.urls import path

from .views import my_schedule

app_name = "schedules"

urlpatterns = [
    path("my/", my_schedule, name="my_schedule"),
]
