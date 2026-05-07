from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Operational profile", {"fields": ("role", "phone_number", "sector", "cell")}),
    )
    list_display = ("username", "email", "role", "sector", "cell", "is_active")
