from django.urls import path
from .views import (
    DoctorListView, MyAvailabilityView, DoctorAvailabilityDetailView,
    AvailableSpecialistsView, DoctorBySpecialistView,
)

urlpatterns = [
    path("list/", DoctorListView.as_view()),
    path("specialists/", AvailableSpecialistsView.as_view()),
    path("available/", DoctorBySpecialistView.as_view()),
    path("availability/", MyAvailabilityView.as_view()),
    path("availability/<int:id>/", DoctorAvailabilityDetailView.as_view()),
]