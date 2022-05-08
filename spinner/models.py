from django.db import models

# Create your models here.

class Color(models.Model):
    hex = models.CharField(max_length=7)
    frequency = models.IntegerField(default=0)