from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import User
from accounts.utils import role_required
from notifications.models import NotificationLog

from .forms import WasteReportForm
from .models import WasteReport


@role_required(User.Role.CITIZEN)
def create_report(request):
    if request.method == "POST":
        form = WasteReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.citizen = request.user
            report.sector = request.user.sector
            report.cell = request.user.cell
            report.save()
            NotificationLog.objects.create(
                user=request.user,
                channel=NotificationLog.Channel.IN_APP,
                message=f"Report '{report.title}' submitted successfully.",
                delivery_status=NotificationLog.DeliveryStatus.SENT,
            )
            messages.success(request, "Waste report submitted.")
            return redirect("reports:my_reports")
    else:
        form = WasteReportForm()
    return render(request, "reports/create_report.html", {"form": form})


@login_required
def my_reports(request):
    if request.user.role == User.Role.CITIZEN:
        reports = WasteReport.objects.filter(citizen=request.user)
    elif request.user.role == User.Role.CONTRACTOR:
        reports = WasteReport.objects.filter(status__in=[WasteReport.Status.PENDING, WasteReport.Status.IN_PROGRESS])
    else:
        reports = WasteReport.objects.all()
    return render(request, "reports/my_reports.html", {"reports": reports[:100]})


@role_required(User.Role.CONTRACTOR, User.Role.ADMIN)
def update_status(request, report_id, status):
    report = get_object_or_404(WasteReport, pk=report_id)
    valid_status = {s[0] for s in WasteReport.Status.choices}
    if status in valid_status:
        report.status = status
        if status == WasteReport.Status.RESOLVED:
            report.resolved_at = timezone.now()
        report.save(update_fields=["status", "resolved_at", "updated_at"])
        NotificationLog.objects.create(
            user=report.citizen,
            channel=NotificationLog.Channel.IN_APP,
            message=f"Your report '{report.title}' is now {report.get_status_display()}.",
            delivery_status=NotificationLog.DeliveryStatus.SENT,
        )
    return redirect("reports:my_reports")
