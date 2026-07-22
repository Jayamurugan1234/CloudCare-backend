from django.contrib import admin
from .models import StaffProfile, CallLog, Room

admin.site.register(StaffProfile)
admin.site.register(CallLog)
admin.site.register(Room)