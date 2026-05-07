from django.contrib import admin

from .models import Cell, District, Sector

admin.site.register(District)
admin.site.register(Sector)
admin.site.register(Cell)
