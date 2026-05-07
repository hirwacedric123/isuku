from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import User
from locations.models import District, Sector
from reports.models import WasteReport


class ReportFlowTests(TestCase):
    def setUp(self):
        district = District.objects.create(name="Gasabo")
        self.sector = Sector.objects.create(name="Remera", district=district)
        self.citizen = User.objects.create_user(
            username="citizen1",
            password="StrongPass123!",
            role=User.Role.CITIZEN,
            sector=self.sector,
        )
        self.contractor = User.objects.create_user(
            username="contractor1",
            password="StrongPass123!",
            role=User.Role.CONTRACTOR,
        )
        self.client = Client()

    def test_citizen_can_submit_report(self):
        self.client.login(username="citizen1", password="StrongPass123!")
        response = self.client.post(
            reverse("reports:create_report"),
            {
                "category": WasteReport.Category.OVERFLOW,
                "title": "Overflowing bin",
                "description": "Needs pickup quickly",
                "latitude": "-1.9441",
                "longitude": "30.0619",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(WasteReport.objects.count(), 1)

    def test_contractor_can_mark_report_resolved(self):
        report = WasteReport.objects.create(
            citizen=self.citizen,
            sector=self.sector,
            category=WasteReport.Category.OVERFLOW,
            title="Overflow",
            description="Test",
            latitude="-1.9441",
            longitude="30.0619",
        )
        self.client.login(username="contractor1", password="StrongPass123!")
        response = self.client.get(reverse("reports:update_status", args=[report.id, WasteReport.Status.RESOLVED]))
        self.assertEqual(response.status_code, 302)
        report.refresh_from_db()
        self.assertEqual(report.status, WasteReport.Status.RESOLVED)

# Create your tests here.
