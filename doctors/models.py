from django.db import models
from django.conf import settings


STATUS_CHOICES = [
    ("pending", "Pending Approval"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
]


class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doctor_id = models.CharField(max_length=12, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    specialist = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    degree_certificate = models.FileField(upload_to="doctor_certificates/")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.specialist})"


WEEKDAYS = [
    (0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"),
    (4, "Friday"), (5, "Saturday"), (6, "Sunday"),
]


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="availability")
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_off = models.BooleanField(default=False)

    class Meta:
        unique_together = ("doctor", "weekday")
        ordering = ["weekday"]

    def __str__(self):
        return f"{self.doctor.name} - {self.get_weekday_display()}"