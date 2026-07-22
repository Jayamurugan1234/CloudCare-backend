from django.db import models
from core.utils import generate_patient_id
from doctors.models import DoctorProfile

class Patient(models.Model):
    patient_id = models.CharField(max_length=12, unique=True, default=generate_patient_id)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    issue = models.TextField()
    specialist_wanted = models.CharField(max_length=100)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    place = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    is_viewed_by_doctor = models.BooleanField(default=False)  # staff sees this
    consultation_started_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Consultation(models.Model):
    """Created when a doctor opens + submits a patient's record."""
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name="consultation")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True)

    # Vitals — NEW
    height_cm = models.FloatField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    blood_pressure = models.CharField(max_length=20, blank=True)   # e.g. "120/80"
    pulse_bpm = models.IntegerField(null=True, blank=True)
    lab_test = models.TextField(blank=True)   # NEW

    diagnosis = models.TextField(blank=True)             # "Description" on the form
    prescription_notes = models.TextField(blank=True)    # "Medicine" on the form
    duration_minutes = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PharmacyOrder(models.Model):
    PAYMENT_CHOICES = [("cash", "Cash"), ("card", "Card"), ("upi", "UPI"), ("insurance", "Insurance")]

    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, related_name="order")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, blank=True)
    is_bought = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)