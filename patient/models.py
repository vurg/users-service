from django.db import models

# Create your models here.


class Patient(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()
