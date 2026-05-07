import csv

from django.db.models import Avg, Count, DurationField, ExpressionWrapper, F
from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import User
from accounts.utils import role_required
from reports.models import WasteReport


def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, "landing.html")
    if request.user.role == User.Role.CITIZEN:
        return render(request, "analytics/citizen_dashboard.html")
    if request.user.role == User.Role.CONTRACTOR:
        return render(request, "analytics/contractor_dashboard_redirect.html")
    return admin_dashboard(request)


@role_required(User.Role.ADMIN)
def admin_dashboard(request):
    total_reports = WasteReport.objects.count()
    resolved_reports = WasteReport.objects.filter(status=WasteReport.Status.RESOLVED).count()
    response_avg = (
        WasteReport.objects.filter(resolved_at__isnull=False)
        .annotate(turnaround=ExpressionWrapper(F("resolved_at") - F("created_at"), output_field=DurationField()))
        .aggregate(avg_turnaround=Avg("turnaround"))
    )
    reports_by_sector = (
        WasteReport.objects.values("sector__name").annotate(total=Count("id")).order_by("-total")
    )
    context = {
        "total_reports": total_reports,
        "resolved_reports": resolved_reports,
        "resolution_rate": round((resolved_reports / total_reports) * 100, 2) if total_reports else 0,
        "avg_response_time": response_avg["avg_turnaround"],
        "reports_by_sector": reports_by_sector,
    }
    return render(request, "analytics/admin_dashboard.html", context)


@role_required(User.Role.ADMIN)
def export_reports_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="waste_reports.csv"'
    writer = csv.writer(response)
    writer.writerow(["ID", "Title", "Category", "Status", "Sector", "Citizen", "Created At", "Resolved At"])
    for report in WasteReport.objects.select_related("sector", "citizen").all():
        writer.writerow(
            [
                report.id,
                report.title,
                report.get_category_display(),
                report.get_status_display(),
                report.sector.name,
                report.citizen.username,
                report.created_at,
                report.resolved_at,
            ]
        )
    return response
