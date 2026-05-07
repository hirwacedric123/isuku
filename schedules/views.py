from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from schedules.models import CollectionSchedule


@login_required
def my_schedule(request):
    schedules = CollectionSchedule.objects.filter(active=True)
    if request.user.sector:
        schedules = schedules.filter(sector=request.user.sector)
    if request.user.cell:
        schedules = schedules.filter(Q(cell=request.user.cell) | Q(cell__isnull=True))
    schedules = schedules.select_related("sector", "cell")
    return render(request, "schedules/my_schedule.html", {"schedules": schedules})
