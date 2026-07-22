from django.contrib import admin
from .models import DoctorProfile, DoctorAvailability
from core.utils import generate_doctor_id, send_doctor_email


@admin.action(description="Approve selected doctors (generates ID + sends email)")
def approve_doctors(modeladmin, request, queryset):
    approved_count = 0
    for doctor in queryset.filter(status="pending"):
        doctor.status = "approved"
        doctor.doctor_id = generate_doctor_id()
        doctor.save()
        send_doctor_email(doctor.user.email, doctor.name, doctor.doctor_id)
        approved_count += 1
    modeladmin.message_user(request, f"{approved_count} doctor(s) approved and emailed.")


@admin.action(description="Reject selected doctors")
def reject_doctors(modeladmin, request, queryset):
    queryset.filter(status="pending").update(status="rejected")


class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "specialist", "status", "doctor_id", "is_available")
    list_filter = ("status", "specialist")
    actions = [approve_doctors, reject_doctors]


admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(DoctorAvailability)