from django.urls import path
from .views import StaffCheckInsTodayView, CallLogListView, RoomListView, RoomToggleView

urlpatterns = [
    path("check-ins-today/", StaffCheckInsTodayView.as_view()),
    path("calls/", CallLogListView.as_view()),
    path("rooms/", RoomListView.as_view()),
    path("rooms/<int:id>/toggle/", RoomToggleView.as_view()),
]