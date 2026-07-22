from rest_framework import serializers
from .models import DoctorProfile, DoctorAvailability


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    weekday_label = serializers.CharField(source="get_weekday_display", read_only=True)

    class Meta:
        model = DoctorAvailability
        fields = ["weekday", "weekday_label", "start_time", "end_time", "is_off"]


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = "__all__"


class DoctorWithAvailabilitySerializer(serializers.ModelSerializer):
    """Used by staff to view a doctor's profile + full weekly schedule together."""
    availability = DoctorAvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ["id", "name", "specialist", "phone", "is_available", "availability"]