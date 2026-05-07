from django.db import models


class NotificationLog(models.Model):
    class Channel(models.TextChoices):
        IN_APP = "IN_APP", "In App"
        EMAIL = "EMAIL", "Email"
        SMS = "SMS", "SMS"

    class DeliveryStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SENT = "SENT", "Sent"
        FAILED = "FAILED", "Failed"

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="notifications")
    channel = models.CharField(max_length=12, choices=Channel.choices, default=Channel.IN_APP)
    message = models.CharField(max_length=255)
    delivery_status = models.CharField(
        max_length=12, choices=DeliveryStatus.choices, default=DeliveryStatus.PENDING
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-sent_at"]
# Create your models here.
