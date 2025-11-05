from django.db import models

class Attendance(models.Model):
    username = models.CharField(max_length=150, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.username or 'Unknown'} - {self.date}"
