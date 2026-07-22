# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from doctors.models import DoctorProfile
# from staff.models import StaffProfile
# from pharmacy.models import PharmacyProfile
# from core.utils import send_doctor_pending_email, send_staff_email, send_pharmacy_email

# User = get_user_model()

# class RegisterSerializer(serializers.Serializer):
#     role = serializers.ChoiceField(choices=["doctor", "staff", "pharmacy"])
#     name = serializers.CharField()
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#     phone = serializers.CharField()

#     specialist = serializers.CharField(required=False, allow_blank=True)
#     staff_role = serializers.ChoiceField(choices=["receptionist", "nurse"], required=False)
#     degree_certificate = serializers.FileField(required=False)

#     def validate_email(self, value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("An account with this email already exists.")
#         return value

#     def validate_specialist(self, value):
#         if value and DoctorProfile.objects.filter(
#             specialist__iexact=value, status__in=["pending", "approved"]
#         ).exists():
#             raise serializers.ValidationError(
#                 f"A doctor for {value} is already registered or pending approval."
#             )
#         return value

#     def validate(self, data):
#         if data["role"] == "doctor":
#             if not data.get("specialist"):
#                 raise serializers.ValidationError({"specialist": "Specialist is required for doctors."})
#             if not data.get("degree_certificate"):
#                 raise serializers.ValidationError({"degree_certificate": "Degree certificate is required."})
#         return data

#     def create(self, validated):
#         role = validated["role"]
#         user = User.objects.create_user(
#             username=validated["email"],
#             email=validated["email"],
#             password=validated["password"],
#             phone=validated["phone"],
#             first_name=validated["name"],
#             role=role,
#         )
#         if role == "doctor":
#             profile = DoctorProfile.objects.create(
#                 user=user, name=validated["name"],
#                 specialist=validated["specialist"],
#                 phone=validated["phone"],
#                 degree_certificate=validated["degree_certificate"],
#             )
#             send_doctor_pending_email(user.email, profile.name)
#         elif role == "staff":
#             profile = StaffProfile.objects.create(
#                 user=user, name=validated["name"],
#                 staff_role=validated.get("staff_role", "receptionist"),
#                 phone=validated["phone"],
#             )
#             send_staff_email(user.email, profile.name, profile.staff_role, profile.staff_id)
#         elif role == "pharmacy":
#             profile = PharmacyProfile.objects.create(
#                 user=user, name=validated["name"], phone=validated["phone"],
#             )
#             send_pharmacy_email(user.email, profile.name, profile.pharmacy_id)
#         return user




import uuid
from rest_framework import serializers
from django.contrib.auth import get_user_model
from doctors.models import DoctorProfile
from staff.models import StaffProfile
from pharmacy.models import PharmacyProfile
from core.utils import send_doctor_pending_email, send_staff_email, send_pharmacy_email

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=["doctor", "staff", "pharmacy"])
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField()

    specialist = serializers.CharField(required=False, allow_blank=True)
    staff_role = serializers.ChoiceField(choices=["receptionist", "nurse"], required=False)
    degree_certificate = serializers.FileField(required=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def validate_specialist(self, value):
        if value and DoctorProfile.objects.filter(
            specialist__iexact=value, status__in=["pending", "approved"]
        ).exists():
            raise serializers.ValidationError(
                f"A doctor for {value} is already registered or pending approval."
            )
        return value

    def validate(self, data):
        email = data.get("email")
        role = data.get("role")

        if User.objects.filter(email=email, role=role).exists():
            raise serializers.ValidationError(
                {"email": f"An account with this email already exists for the {role} role."}
            )

        if role == "doctor":
            if not data.get("specialist"):
                raise serializers.ValidationError({"specialist": "Specialist is required for doctors."})
            if not data.get("degree_certificate"):
                raise serializers.ValidationError({"degree_certificate": "Degree certificate is required."})
        return data

    def create(self, validated):
        role = validated["role"]

        unique_username = f"{validated['email']}-{role}-{uuid.uuid4().hex[:6]}"

        user = User.objects.create_user(
            username=unique_username,
            email=validated["email"],
            password=validated["password"],
            phone=validated["phone"],
            first_name=validated["name"],
            role=role,
        )
        if role == "doctor":
            profile = DoctorProfile.objects.create(
                user=user, name=validated["name"],
                specialist=validated["specialist"],
                phone=validated["phone"],
                degree_certificate=validated["degree_certificate"],
            )
            send_doctor_pending_email(user.email, profile.name)
        elif role == "staff":
            profile = StaffProfile.objects.create(
                user=user, name=validated["name"],
                staff_role=validated.get("staff_role", "receptionist"),
                phone=validated["phone"],
            )
            send_staff_email(user.email, profile.name, profile.staff_role, profile.staff_id)
        elif role == "pharmacy":
            profile = PharmacyProfile.objects.create(
                user=user, name=validated["name"], phone=validated["phone"],
            )
            send_pharmacy_email(user.email, profile.name, profile.pharmacy_id)
        return user