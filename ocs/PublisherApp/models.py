from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    email = models.EmailField(max_length=254,default="example@example.com")  # Field for Gmail
    timing = models.CharField(max_length=100,default="9:00 AM - 5:00 PM")  # Field for timing (e.g., "10:00 AM - 4:00 PM")

    def __str__(self):
        return self.name


class Tutor(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    email = models.EmailField(max_length=254,default="example@example.com")  # Field for Gmail
    timing = models.CharField(max_length=100,default="9:00 AM - 5:00 PM")  # Field for timing (e.g., "2:00 PM - 6:00 PM")

    def __str__(self):
        return self.name
