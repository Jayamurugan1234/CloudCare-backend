from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import DoctorProfile, DoctorAvailability, WEEKDAYS
from .serializers import (
    DoctorProfileSerializer, DoctorAvailabilitySerializer, DoctorWithAvailabilitySerializer,
)


class DoctorListView(ListAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = DoctorProfile.objects.all()


class AvailableSpecialistsView(APIView):
    """Public — lets the booking form show real specialties, so patients
    can't type something that doesn't match any doctor's profile."""
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        specialists = (
            DoctorProfile.objects.filter(is_available=True)
            .values_list("specialist", flat=True)
        )
        return Response(sorted(set(specialists)))


class DoctorBySpecialistView(APIView):
    """Public — used by the patient booking form to show doctor name/ID
    and live availability (based on the doctor's real weekly schedule)."""
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        specialist = request.GET.get("specialist", "").strip()
        if not specialist:
            return Response({"error": "specialist query param required"}, status=400)

        doctor = DoctorProfile.objects.filter(
            specialist__iexact=specialist, status="approved"
        ).first()

        if not doctor:
            return Response({"found": False, "message": "No approved doctor for this specialist yet."})

        now = timezone.localtime()
        weekday = now.weekday()
        today_slot = DoctorAvailability.objects.filter(doctor=doctor, weekday=weekday).first()

        is_available_now = doctor.is_available
        status_message = "Available"

        if today_slot:
            if today_slot.is_off:
                is_available_now = False
                status_message = "Off today"
            elif today_slot.start_time and today_slot.end_time:
                current_time = now.time()
                if not (today_slot.start_time <= current_time <= today_slot.end_time):
                    is_available_now = False
                    status_message = (
                        f"Available {today_slot.start_time.strftime('%I:%M %p')} - "
                        f"{today_slot.end_time.strftime('%I:%M %p')}"
                    )
        elif not doctor.is_available:
            is_available_now = False
            status_message = "Currently unavailable"

        return Response({
            "found": True,
            "doctor_id": doctor.doctor_id,
            "name": doctor.name,
            "specialist": doctor.specialist,
            "is_available_now": is_available_now,
            "status_message": status_message,
        })


class MyAvailabilityView(APIView):
    """The logged-in doctor views/edits their own weekly schedule."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctor = get_object_or_404(DoctorProfile, user=request.user)
        self._ensure_week_exists(doctor)
        rows = DoctorAvailability.objects.filter(doctor=doctor)
        return Response(DoctorAvailabilitySerializer(rows, many=True).data)

    def put(self, request):
        doctor = get_object_or_404(DoctorProfile, user=request.user)
        self._ensure_week_exists(doctor)

        for entry in request.data:
            weekday = entry.get("weekday")
            row = DoctorAvailability.objects.filter(doctor=doctor, weekday=weekday).first()
            if row is None:
                continue
            row.is_off = entry.get("is_off", False)
            row.start_time = entry.get("start_time") or None
            row.end_time = entry.get("end_time") or None
            row.save()

        rows = DoctorAvailability.objects.filter(doctor=doctor)
        return Response(DoctorAvailabilitySerializer(rows, many=True).data)

    def _ensure_week_exists(self, doctor):
        existing = set(DoctorAvailability.objects.filter(doctor=doctor).values_list("weekday", flat=True))
        for day_num, _ in WEEKDAYS:
            if day_num not in existing:
                DoctorAvailability.objects.create(doctor=doctor, weekday=day_num, is_off=True)


class DoctorAvailabilityDetailView(RetrieveAPIView):
    """Staff (or anyone authenticated) views one doctor's profile + weekly schedule."""
    serializer_class = DoctorWithAvailabilitySerializer
    permission_classes = [IsAuthenticated]
    queryset = DoctorProfile.objects.all()
    lookup_field = "id"