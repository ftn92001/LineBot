from django.contrib import admin
from .models import LineUser, Photo, DailyAttendance 
# Register your models here.

admin.site.register(LineUser)
admin.site.register(Photo)
admin.site.register(DailyAttendance)