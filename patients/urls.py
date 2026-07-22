from django.urls import path
from .views import (
    PatientRegisterView, DoctorPatientListView, SubmitConsultationView, StartConsultationView,
    StaffPatientListView, PharmacyOrderListView, PharmacyOrderUpdateView,
    DoctorTodayAppointmentsView, DoctorWaitingPatientsView, DoctorCompletedTodayView,
    DoctorAvgConsultTimeView,
)

urlpatterns = [
    path("register/", PatientRegisterView.as_view()),
    path("doctor/list/", DoctorPatientListView.as_view()),
    path("doctor/appointments-today/", DoctorTodayAppointmentsView.as_view()),
    path("doctor/waiting/", DoctorWaitingPatientsView.as_view()),
    path("doctor/completed-today/", DoctorCompletedTodayView.as_view()),
    path("doctor/avg-consult-time/", DoctorAvgConsultTimeView.as_view()),
    path("doctor/consult/start/<str:patient_id>/", StartConsultationView.as_view()),
    path("doctor/consult/<str:patient_id>/", SubmitConsultationView.as_view()),
    path("staff/list/", StaffPatientListView.as_view()),
    path("pharmacy/orders/", PharmacyOrderListView.as_view()),
    path("pharmacy/orders/<int:id>/", PharmacyOrderUpdateView.as_view()),
]