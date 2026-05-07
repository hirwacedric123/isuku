from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CITIZEN = "CITIZEN", "Citizen"
        CONTRACTOR = "CONTRACTOR", "Contractor"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CITIZEN)
    phone_number = models.CharField(max_length=20, blank=True)
    sector = models.ForeignKey(
        "locations.Sector",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    cell = models.ForeignKey(
        "locations.Cell",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    def is_citizen(self):
        return self.role == self.Role.CITIZEN

    def is_contractor(self):
        return self.role == self.Role.CONTRACTOR

    def is_municipal_admin(self):
        return self.role == self.Role.ADMIN

# Create your models here.
