from rest_framework import serializers
from .models import Patient, Consultation, PharmacyOrder

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ["patient_id", "is_viewed_by_doctor", "consultation_started_at"]

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = "__all__"

class CompletedConsultationSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    patient_id = serializers.CharField(source="patient.patient_id", read_only=True)

    class Meta:
        model = Consultation
        fields = ["id", "patient_name", "patient_id", "diagnosis", "duration_minutes", "created_at"]

class PharmacyOrderSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="consultation.doctor.name", read_only=True)
    specialist = serializers.CharField(source="consultation.doctor.specialist", read_only=True)
    patient_name = serializers.CharField(source="consultation.patient.name", read_only=True)
    patient_id = serializers.CharField(source="consultation.patient.patient_id", read_only=True)
    prescription_notes = serializers.CharField(source="consultation.prescription_notes", read_only=True)

    class Meta:
        model = PharmacyOrder
        fields = "__all__"