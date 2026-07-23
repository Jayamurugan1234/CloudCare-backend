[33mcommit 11add5e77391c1f3b3600644fdff80a0dea985df[m
Author: Jayamurugan1234 <jayamuruganvenkatachalam27@gmail.com>
Date:   Wed Jul 22 13:27:56 2026 +0530

    Remove duplicate email validator that blocked role-scoped registration

[1mdiff --git a/accounts/serializers.py b/accounts/serializers.py[m
[1mindex 240fe53..2fb4204 100644[m
[1m--- a/accounts/serializers.py[m
[1m+++ b/accounts/serializers.py[m
[36m@@ -1,80 +1,3 @@[m
[31m-# from rest_framework import serializers[m
[31m-# from django.contrib.auth import get_user_model[m
[31m-# from doctors.models import DoctorProfile[m
[31m-# from staff.models import StaffProfile[m
[31m-# from pharmacy.models import PharmacyProfile[m
[31m-# from core.utils import send_doctor_pending_email, send_staff_email, send_pharmacy_email[m
[31m-[m
[31m-# User = get_user_model()[m
[31m-[m
[31m-# class RegisterSerializer(serializers.Serializer):[m
[31m-#     role = serializers.ChoiceField(choices=["doctor", "staff", "pharmacy"])[m
[31m-#     name = serializers.CharField()[m
[31m-#     email = serializers.EmailField()[m
[31m-#     password = serializers.CharField(write_only=True)[m
[31m-#     phone = serializers.CharField()[m
[31m-[m
[31m-#     specialist = serializers.CharField(required=False, allow_blank=True)[m
[31m-#     staff_role = serializers.ChoiceField(choices=["receptionist", "nurse"], required=False)[m
[31m-#     degree_certificate = serializers.FileField(required=False)[m
[31m-[m
[31m-#     def validate_email(self, value):[m
[31m-#         if User.objects.filter(email=value).exists():[m
[31m-#             raise serializers.ValidationError("An account with this email already exists.")[m
[31m-#         return value[m
[31m-[m
[31m-#     def validate_specialist(self, value):[m
[31m-#         if value and DoctorProfile.objects.filter([m
[31m-#             specialist__iexact=value, status__in=["pending", "approved"][m
[31m-#         ).exists():[m
[31m-#             raise serializers.ValidationError([m
[31m-#                 f"A doctor for {value} is already registered or pending approval."[m
[31m-#             )[m
[31m-#         return value[m
[31m-[m
[31m-#     def validate(self, data):[m
[31m-#         if data["role"] == "doctor":[m
[31m-#             if not data.get("specialist"):[m
[31m-#                 raise serializers.ValidationError({"specialist": "Specialist is required for doctors."})[m
[31m-#             if not data.get("degree_certificate"):[m
[31m-#                 raise serializers.ValidationError({"degree_certificate": "Degree certificate is required."})[m
[31m-#         return data[m
[31m-[m
[31m-#     def create(self, validated):[m
[31m-#         role = validated["role"][m
[31m-#         user = User.objects.create_user([m
[31m-#             username=validated["email"],[m
[31m-#             email=validated["email"],[m
[31m-#             password=validated["password"],[m
[31m-#             phone=validated["phone"],[m
[31m-#             first_name=validated["name"],[m
[31m-#             role=role,[m
[31m-#         )[m
[31m-#         if role == "doctor":[m
[31m-#             profile = DoctorProfile.objects.create([m
[31m-#                 user=user, name=validated["name"],[m
[31m-#                 specialist=validated["specialist"],[m
[31m-#                 phone=validated["phone"],[m
[31m-#                 degree_certificate=validated["degree_certificate"],[m
[31m-#             )[m
[31m-#             send_doctor_pending_email(user.email, profile.name)[m
[31m-#         elif role == "staff":[m
[31m-#             profile = StaffProfile.objects.create([m
[31m-#                 user=user, name=validated["name"],[m
[31m-#                 staff_role=validated.get("staff_role", "receptionist"),[m
[31m-#                 phone=validated["phone"],[m
[31m-#             )[m
[31m-#             send_staff_email(user.email, profile.name, profile.staff_role, profile.staff_id)[m
[31m-#         elif role == "pharmacy":[m
[31m-#             profile = PharmacyProfile.objects.create([m
[31m-#                 user=user, name=validated["name"], phone=validated["phone"],[m
[31m-#             )[m
[31m-#             send_pharmacy_email(user.email, profile.name, profile.pharmacy_id)[m
[31m-#         return user[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
 import uuid[m
 from rest_framework import serializers[m
 from django.contrib.auth import get_user_model[m
[36m@@ -96,11 +19,6 @@[m [mclass RegisterSerializer(serializers.Serializer):[m
     staff_role = serializers.ChoiceField(choices=["receptionist", "nurse"], required=False)[m
     degree_certificate = serializers.FileField(required=False)[m
 [m
[31m-    def validate_email(self, value):[m
[31m-        if User.objects.filter(email=value).exists():[m
[31m-            raise serializers.ValidationError("An account with this email already exists.")[m
[31m-        return value[m
[31m-[m
     def validate_specialist(self, value):[m
         if value and DoctorProfile.objects.filter([m
             specialist__iexact=value, status__in=["pending", "approved"][m
