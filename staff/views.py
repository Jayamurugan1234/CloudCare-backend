from django.utils import timezone
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import CallLog, Room
from .serializers import CallLogSerializer, RoomSerializer
from patients.models import Patient
from patients.serializers import PatientSerializer


class StaffCheckInsTodayView(ListAPIView):
    """Everyone with a preferred appointment date of today, across all specialties."""
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(preferred_date=timezone.localdate()).order_by("preferred_time")


class CallLogListView(ListCreateAPIView):
    """Static list for now — POST support included so logging can be wired in later
    without another migration."""
    serializer_class = CallLogSerializer
    permission_classes = [IsAuthenticated]
    queryset = CallLog.objects.all()


class RoomListView(ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()


class RoomToggleView(APIView):
    """Flip a room's occupied status."""
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        room = get_object_or_404(Room, id=id)
        room.is_occupied = not room.is_occupied
        room.save()
        return Response(RoomSerializer(room).data)