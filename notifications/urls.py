from django.urls import path

from .views import my_notifications

app_name = "notifications"

urlpatterns = [
    path("my/", my_notifications, name="my_notifications"),
]
