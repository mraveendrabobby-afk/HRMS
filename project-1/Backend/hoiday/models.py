from django.db import models
from django.conf import settings

class LeaveRequest(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_APPROVED = "Approved"
    STATUS_REJECTED = "Rejected"
    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    )

    LEAVE_ANNUAL = "Annual"
    LEAVE_SICK = "Sick"
    LEAVE_CASUAL = "Casual"
    LEAVE_OTHER = "Other"
    LEAVE_TYPE_CHOICES = (
        (LEAVE_ANNUAL, "Annual"),
        (LEAVE_SICK, "Sick"),
        (LEAVE_CASUAL, "Casual"),
        (LEAVE_OTHER, "Other"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.CharField(max_length=32, choices=LEAVE_TYPE_CHOICES, default=LEAVE_ANNUAL)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Leave Request"
        verbose_name_plural = "Leave Requests"

    def __str__(self):
        return f"{self.user} — {self.leave_type} ({self.from_date} → {self.to_date}) [{self.status}]"
