from django.db import models


class CollectionSchedule(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 1, "Monday"
        TUESDAY = 2, "Tuesday"
        WEDNESDAY = 3, "Wednesday"
        THURSDAY = 4, "Thursday"
        FRIDAY = 5, "Friday"
        SATURDAY = 6, "Saturday"
        SUNDAY = 7, "Sunday"

    sector = models.ForeignKey("locations.Sector", on_delete=models.CASCADE, related_name="schedules")
    cell = models.ForeignKey(
        "locations.Cell",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="schedules",
    )
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sector__name", "weekday", "start_time"]

    def __str__(self):
        return f"{self.sector.name} - {self.get_weekday_display()}"
# Create your models here.
