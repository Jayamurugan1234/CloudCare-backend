from django.contrib import admin
from .models import Patient, Consultation, PharmacyOrder

admin.site.register(Patient)
admin.site.register(Consultation)
admin.site.register(PharmacyOrder)