from django.db import models


class Vehicle(models.Model):
    contractor = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="vehicles")
    plate_number = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.plate_number


class RoutePlan(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        ASSIGNED = "ASSIGNED", "Assigned"
        COMPLETED = "COMPLETED", "Completed"

    contractor = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="route_plans")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name="routes")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    estimated_distance_km = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    generated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Route {self.pk} - {self.get_status_display()}"


class RouteStop(models.Model):
    route = models.ForeignKey(RoutePlan, on_delete=models.CASCADE, related_name="stops")
    report = models.ForeignKey("reports.WasteReport", on_delete=models.CASCADE, related_name="route_stops")
    sequence = models.PositiveIntegerField()
    eta = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["sequence"]
        unique_together = ("route", "sequence")

    def __str__(self):
        return f"Route {self.route_id} stop {self.sequence}"
# Create your models here.
