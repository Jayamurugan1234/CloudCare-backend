# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import RegisterSerializer

# class RegisterView(APIView):
#     permission_classes = []
#     def post(self, request):
#         s = RegisterSerializer(data=request.data)
#         s.is_valid(raise_exception=True)
#         user = s.save()
#         return Response({"message": "Registered", "role": user.role}, status=201)

# class LoginView(APIView):
#     permission_classes = []
#     def post(self, request):
#         from django.contrib.auth import authenticate
#         email = request.data.get("email")
#         password = request.data.get("password")
#         role = request.data.get("role")
#         login_id = (request.data.get("login_id") or "").strip()

#         user = authenticate(username=email, password=password)
#         if not user or user.role != role:
#             return Response({"detail": "Invalid credentials or role"}, status=400)

#         profile = None
#         expected_id = None

#         if role == "doctor":
#             from doctors.models import DoctorProfile
#             profile = DoctorProfile.objects.filter(user=user).first()

#             if not profile:
#                 return Response({"detail": "No profile found for this account"}, status=400)
#             if profile.status == "pending":
#                 return Response({"detail": "Your account is pending admin approval."}, status=403)
#             if profile.status == "rejected":
#                 return Response({"detail": "Your registration was rejected. Contact admin."}, status=403)

#             expected_id = profile.doctor_id
#         elif role == "staff":
#             from staff.models import StaffProfile
#             profile = StaffProfile.objects.filter(user=user).first()
#             expected_id = profile.staff_id if profile else None
#         elif role == "pharmacy":
#             from pharmacy.models import PharmacyProfile
#             profile = PharmacyProfile.objects.filter(user=user).first()
#             expected_id = profile.pharmacy_id if profile else None

#         if not profile or not expected_id:
#             return Response({"detail": "No profile found for this account"}, status=400)

#         if login_id.upper() != expected_id.upper():
#             return Response({"detail": "ID does not match this account"}, status=400)

#         refresh = RefreshToken.for_user(user)
#         response_data = {
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "role": user.role,
#             "name": user.first_name,
#         }

#         if role == "doctor":
#             response_data["doctor_id"] = expected_id
#         elif role == "staff":
#             response_data["staff_id"] = expected_id
#         elif role == "pharmacy":
#             response_data["pharmacy_id"] = expected_id

#         return Response(response_data)














from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer

User = get_user_model()

class RegisterView(APIView):
    permission_classes = []
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.save()
        return Response({"message": "Registered", "role": user.role}, status=201)


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")
        login_id = (request.data.get("login_id") or "").strip()

        
        candidates = User.objects.filter(email=email, role=role)
        user = None
        for candidate in candidates:
            if candidate.check_password(password):
                user = candidate
                break

        if not user:
            return Response({"detail": "Invalid credentials or role"}, status=400)

        profile = None
        expected_id = None

        if role == "doctor":
            from doctors.models import DoctorProfile
            profile = DoctorProfile.objects.filter(user=user).first()
            if not profile:
                return Response({"detail": "No profile found for this account"}, status=400)
            if profile.status == "pending":
                return Response({"detail": "Your account is pending admin approval."}, status=403)
            if profile.status == "rejected":
                return Response({"detail": "Your registration was rejected. Contact admin."}, status=403)
            expected_id = profile.doctor_id
        elif role == "staff":
            from staff.models import StaffProfile
            profile = StaffProfile.objects.filter(user=user).first()
            expected_id = profile.staff_id if profile else None
        elif role == "pharmacy":
            from pharmacy.models import PharmacyProfile
            profile = PharmacyProfile.objects.filter(user=user).first()
            expected_id = profile.pharmacy_id if profile else None

        if not profile or not expected_id:
            return Response({"detail": "No profile found for this account"}, status=400)

        if login_id.upper() != expected_id.upper():
            return Response({"detail": "ID does not match this account"}, status=400)

        refresh = RefreshToken.for_user(user)
        response_data = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role,
            "name": user.first_name,
        }

        if role == "doctor":
            response_data["doctor_id"] = expected_id
        elif role == "staff":
            response_data["staff_id"] = expected_id
        elif role == "pharmacy":
            response_data["pharmacy_id"] = expected_id

        return Response(response_data)