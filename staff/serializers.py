from rest_framework import serializers
from .models import StaffProfile, CallLog, Room


class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = "__all__"


class CallLogSerializer(serializers.ModelSerializer):
    handled_by_name = serializers.CharField(source="handled_by.name", read_only=True)

    class Meta:
        model = CallLog
        fields = ["id", "caller_name", "phone", "note", "handled_by_name", "created_at"]


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_number", "ward", "is_occupied", "updated_at"]