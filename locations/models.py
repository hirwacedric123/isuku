from django.db import models


class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Sector(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="sectors")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("district", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.district.name})"


class Cell(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="cells")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("sector", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.sector.name})"

# Create your models here.
