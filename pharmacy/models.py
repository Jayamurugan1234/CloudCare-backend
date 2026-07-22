from django.db import models
from django.conf import settings
from core.utils import generate_pharmacy_id

class PharmacyProfile(models.Model):
    pharmacy_id = models.CharField(max_length=12, unique=True, default=generate_pharmacy_id)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)


def generate_staff_id():
    return "PHR" + "".join(random.choices(string.digits, k=6))