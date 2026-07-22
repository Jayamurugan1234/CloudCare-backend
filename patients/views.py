from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .models import Patient, Consultation, PharmacyOrder
from .serializers import (
    PatientSerializer, ConsultationSerializer, PharmacyOrderSerializer, CompletedConsultationSerializer,
)
from doctors.models import DoctorProfile, DoctorAvailability
from core.utils import send_patient_email


class PatientRegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

        doctor = DoctorProfile.objects.filter(
            specialist__iexact=patient.specialist_wanted, status="approved"
        ).first()

        availability_line = "Doctor availability could not be determined.\n"

        if doctor:
            weekday = patient.preferred_date.weekday()
            slot = DoctorAvailability.objects.filter(doctor=doctor, weekday=weekday).first()

            if slot:
                if slot.is_off:
                    availability_line = (
                        f"Note: Dr. {doctor.name} is off on {patient.preferred_date.strftime('%A, %d %b %Y')}. "
                        f"The clinic will contact you to reschedule if needed.\n"
                    )
                elif slot.start_time and slot.end_time:
                    availability_line = (
                        f"Dr. {doctor.name}'s availability on {patient.preferred_date.strftime('%A, %d %b %Y')}: "
                        f"{slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}\n"
                    )
                else:
                    availability_line = (
                        f"Dr. {doctor.name} has no fixed hours set for "
                        f"{patient.preferred_date.strftime('%A, %d %b %Y')}.\n"
                    )
            else:
                availability_line = (
                    f"Availability schedule for Dr. {doctor.name} on this day hasn't been set yet.\n"
                )

        send_patient_email(
            patient.email,
            patient.name,
            patient.specialist_wanted,
            doctor.name if doctor else None,
            doctor.doctor_id if doctor else None,
            patient.patient_id,
            patient.preferred_date,
            patient.preferred_time,
            availability_line,
        )

        return Response({
            "message": "Registered successfully. Email sent.",
            "patient_id": patient.patient_id,
        }, status=201)



class DoctorPatientListView(ListAPIView):
    """Full list for this doctor's specialty (kept for backward compatibility)."""
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor = DoctorProfile.objects.get(user=self.request.user)
        return Patient.objects.filter(specialist_wanted__iexact=doctor.specialist)


class DoctorTodayAppointmentsView(ListAPIView):
    """Today's appointments for the logged-in doctor's specialty."""
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor = DoctorProfile.objects.get(user=self.request.user)
        return Patient.objects.filter(
            specialist_wanted__iexact=doctor.specialist,
            preferred_date=timezone.localdate(),
        ).order_by("preferred_time")


class DoctorWaitingPatientsView(ListAPIView):
    """Today's appointments not yet consulted."""
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor = DoctorProfile.objects.get(user=self.request.user)
        return Patient.objects.filter(
            specialist_wanted__iexact=doctor.specialist,
            preferred_date=timezone.localdate(),
            is_viewed_by_doctor=False,
        ).order_by("preferred_time")


class DoctorCompletedTodayView(ListAPIView):
    """Consultations this doctor finished today."""
    serializer_class = CompletedConsultationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor = DoctorProfile.objects.get(user=self.request.user)
        return Consultation.objects.filter(
            doctor=doctor, created_at__date=timezone.localdate(),
        ).select_related("patient").order_by("-created_at")


class DoctorAvgConsultTimeView(APIView):
    """Average consult duration for this doctor, today."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctor = DoctorProfile.objects.get(user=request.user)
        qs = Consultation.objects.filter(
            doctor=doctor, created_at__date=timezone.localdate(), duration_minutes__isnull=False,
        )
        avg = qs.aggregate(avg=Avg("duration_minutes"))["avg"]
        return Response({
            "avg_minutes": round(avg, 1) if avg else None,
            "consultations_counted": qs.count(),
        })


class StartConsultationView(APIView):
    """Doctor opens a patient's record — starts the consult timer."""
    permission_classes = [IsAuthenticated]

    def post(self, request, patient_id):
        patient = get_object_or_404(Patient, patient_id=patient_id)
        patient.consultation_started_at = timezone.now()
        patient.save()
        return Response({"message": "Consultation started", "started_at": patient.consultation_started_at})


# class SubmitConsultationView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, patient_id):
#         patient = get_object_or_404(Patient, patient_id=patient_id)
#         doctor = DoctorProfile.objects.get(user=request.user)

#         duration_minutes = None
#         if patient.consultation_started_at:
#             delta = timezone.now() - patient.consultation_started_at
#             duration_minutes = round(delta.total_seconds() / 60, 1)

#         consultation = Consultation.objects.create(
#             patient=patient,
#             doctor=doctor,
#             height_cm=request.data.get("height_cm") or None,
#             weight_kg=request.data.get("weight_kg") or None,
#             blood_pressure=request.data.get("blood_pressure", ""),
#             pulse_bpm=request.data.get("pulse_bpm") or None,
#             diagnosis=request.data.get("diagnosis", ""),
#             prescription_notes=request.data.get("prescription_notes", ""),
#             lab_test=request.data.get("lab_test", ""),
#             duration_minutes=duration_minutes,
#         )
#         PharmacyOrder.objects.create(consultation=consultation)

#         patient.is_viewed_by_doctor = True
#         patient.save()

#         return Response({"message": "Consultation saved and sent to pharmacy"}, status=201)


class SubmitConsultationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        """Fetch existing consultation details for a patient, if any."""
        patient = get_object_or_404(Patient, patient_id=patient_id)
        consultation = getattr(patient, "consultation", None)
        if not consultation:
            return Response({"exists": False})
        serializer = ConsultationSerializer(consultation)
        return Response({"exists": True, **serializer.data})

    def post(self, request, patient_id):
        """Create a new consultation, or update it if one already exists (edit)."""
        patient = get_object_or_404(Patient, patient_id=patient_id)
        doctor = DoctorProfile.objects.get(user=request.user)

        duration_minutes = None
        if patient.consultation_started_at:
            delta = timezone.now() - patient.consultation_started_at
            duration_minutes = round(delta.total_seconds() / 60, 1)

        defaults = dict(
            doctor=doctor,
            height_cm=request.data.get("height_cm") or None,
            weight_kg=request.data.get("weight_kg") or None,
            blood_pressure=request.data.get("blood_pressure", ""),
            pulse_bpm=request.data.get("pulse_bpm") or None,
            diagnosis=request.data.get("diagnosis", ""),
            prescription_notes=request.data.get("prescription_notes", ""),
            lab_test=request.data.get("lab_test", ""),
        )
      
        if duration_minutes is not None:
            defaults["duration_minutes"] = duration_minutes

        consultation, created = Consultation.objects.update_or_create(
            patient=patient, defaults=defaults,
        )
        if created:
            PharmacyOrder.objects.create(consultation=consultation)

        patient.is_viewed_by_doctor = True
        patient.save()

        return Response({"message": "Consultation saved", "created": created}, status=201)


class StaffPatientListView(ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    queryset = Patient.objects.all().order_by("-created_at")


class PharmacyOrderListView(ListAPIView):
    serializer_class = PharmacyOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = PharmacyOrder.objects.select_related("consultation__doctor", "consultation__patient")


class PharmacyOrderUpdateView(RetrieveUpdateAPIView):
    serializer_class = PharmacyOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = PharmacyOrder.objects.all()
    lookup_field = "id"