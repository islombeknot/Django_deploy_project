from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    image = models.ImageField(max_length=255, upload_to='service', null=True)
    class_name = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name
    

class Doctor(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    image = models.ImageField(max_length=255, upload_to='doctor')
    special_name = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="doctor_speciality")
    class_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

class Date(models.Model):
    day = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.day

class Time(models.Model):
    time = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.time

class Appointment(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor")
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True, blank=True)
    app_date = models.ForeignKey(Date, on_delete=models.CASCADE, related_name="app_date", max_length=255)
    app_time = models.ForeignKey(Time, on_delete=models.CASCADE, related_name="app_time", max_length=255)

    def __str__(self):
        return f"{self.user_name}-{self.name}"
    