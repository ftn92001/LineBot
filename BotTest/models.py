from django.db import models

# Create your models here.
class Photo(models.Model):
    image_src = models.URLField()
    name = models.CharField(max_length=255, default='')