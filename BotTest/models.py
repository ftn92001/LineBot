from django.db import models

# Create your models here.

class LineUser(models.Model):
    line_id = models.CharField(max_length=255)
    money = models.IntegerField()

class Photo(models.Model):
    image_src = models.URLField()
    name = models.CharField(max_length=255, default='')
    url = models.URLField(blank=True)

class DailyAttendance(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    line_user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name="daily_attendance")