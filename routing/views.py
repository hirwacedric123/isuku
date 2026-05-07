from math import sqrt

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import User
from accounts.utils import role_required
from reports.models import WasteReport

from .models import RoutePlan, RouteStop, Vehicle


def _distance(a, b):
    return sqrt((float(a.latitude) - float(b.latitude)) ** 2 + (float(a.longitude) - float(b.longitude)) ** 2)


@role_required(User.Role.CONTRACTOR)
def contractor_dashboard(request):
    open_reports = list(WasteReport.objects.filter(status=WasteReport.Status.PENDING)[:200])
    vehicles = Vehicle.objects.filter(contractor=request.user, is_active=True)
    return render(
        request,
        "routing/contractor_dashboard.html",
        {"open_reports": open_reports, "vehicles": vehicles},
    )


@role_required(User.Role.CONTRACTOR)
def generate_route(request):
    reports = list(WasteReport.objects.filter(status=WasteReport.Status.PENDING)[:30])
    if not reports:
        messages.warning(request, "No open reports to generate route.")
        return redirect("routing:dashboard")

    ordered = [reports.pop(0)]
    while reports:
        last = ordered[-1]
        next_point = min(reports, key=lambda r: _distance(last, r))
        reports.remove(next_point)
        ordered.append(next_point)

    route = RoutePlan.objects.create(contractor=request.user, status=RoutePlan.Status.DRAFT)
    for index, report in enumerate(ordered, start=1):
        RouteStop.objects.create(route=route, report=report, sequence=index)
        report.status = WasteReport.Status.IN_PROGRESS
        report.save(update_fields=["status", "updated_at"])

    messages.success(request, f"Route {route.id} generated with {len(ordered)} stops.")
    return redirect("routing:route_detail", route_id=route.id)


@role_required(User.Role.CONTRACTOR)
def route_detail(request, route_id):
    route = get_object_or_404(RoutePlan.objects.prefetch_related("stops__report"), pk=route_id, contractor=request.user)
    return render(request, "routing/route_detail.html", {"route": route})


@role_required(User.Role.CONTRACTOR)
def complete_route(request, route_id):
    route = get_object_or_404(RoutePlan, pk=route_id, contractor=request.user)
    for stop in route.stops.select_related("report").all():
        report = stop.report
        report.status = WasteReport.Status.RESOLVED
        report.resolved_at = timezone.now()
        report.save(update_fields=["status", "resolved_at", "updated_at"])
    route.status = RoutePlan.Status.COMPLETED
    route.completed_at = timezone.now()
    route.save(update_fields=["status", "completed_at"])
    messages.success(request, "Route completed and all related reports resolved.")
    return redirect("routing:dashboard")
