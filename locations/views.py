from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import District, Sector


@login_required
def location_overview(request):
    return render(
        request,
        "locations/overview.html",
        {"district_count": District.objects.count(), "sector_count": Sector.objects.count()},
    )
