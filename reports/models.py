from django.db import models


class WasteReport(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"

    class Category(models.TextChoices):
        OVERFLOW = "OVERFLOW", "Overflowing Bin"
        MISSED_PICKUP = "MISSED_PICKUP", "Missed Pickup"
        ILLEGAL_DUMP = "ILLEGAL_DUMP", "Illegal Dumping"
        HAZARDOUS = "HAZARDOUS", "Hazardous Waste"

    citizen = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="waste_reports")
    sector = models.ForeignKey("locations.Sector", on_delete=models.CASCADE, related_name="waste_reports")
    cell = models.ForeignKey(
        "locations.Cell",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="waste_reports",
    )
    category = models.CharField(max_length=20, choices=Category.choices)
    title = models.CharField(max_length=120)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    photo = models.ImageField(upload_to="reports/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    resolved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
# Create your models here.
