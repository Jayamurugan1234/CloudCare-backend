from django.db import models
from django.conf import settings
from core.utils import generate_staff_id

class StaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=12, unique=True, default=generate_staff_id)
    name = models.CharField(max_length=100)
    staff_role = models.CharField(
        max_length=20, choices=[("receptionist", "Receptionist"), ("nurse", "Nurse")]
    )
    phone = models.CharField(max_length=15)

def generate_staff_id():
    return "STF" + "".join(random.choices(string.digits, k=6))

class CallLog(models.Model):
    caller_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    note = models.CharField(max_length=255, blank=True)
    handled_by = models.ForeignKey(StaffProfile, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Room(models.Model):
    room_number = models.CharField(max_length=20, unique=True)
    ward = models.CharField(max_length=50, blank=True)
    is_occupied = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["room_number"]