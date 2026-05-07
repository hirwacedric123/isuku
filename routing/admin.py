from django.contrib import admin

from .models import RoutePlan, RouteStop, Vehicle

admin.site.register(Vehicle)
admin.site.register(RoutePlan)
admin.site.register(RouteStop)
