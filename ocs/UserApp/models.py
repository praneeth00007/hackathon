# In UserApp.models

from django.db import models
from django.contrib.auth.models import User
from PublisherApp.models import Doctor, Tutor  # Import the models from PublisherApp

class UserDoctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.doctor.name}"

class UserTutor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.tutor.name}"
# UserApp/models.py

from django.db import models
from django.contrib.auth.models import User
from PublisherApp.models import Doctor, Tutor

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True, blank=True, on_delete=models.SET_NULL)
    tutor = models.ForeignKey(Tutor, null=True, blank=True, on_delete=models.SET_NULL)
    payment_status = models.BooleanField(default=False)  # Payment status (True for paid, False for unpaid)

    def __str__(self):
        return self.user.username

class UserRegistrationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entity_type = models.CharField(max_length=20, choices=[('doctor', 'Doctor'), ('tutor', 'Tutor')])
    entity_id = models.PositiveIntegerField()  # ID of the doctor or tutor
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} registered for {self.entity_type} ID {self.entity_id}"

# In models.py
from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username} - {'Paid' if self.paid else 'Pending'}"

from django.db import models
from django.contrib.auth.models import User
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, default="DEFAULT_ORDER_ID")  # Static default value
    upi_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    upi_payment_reference = models.CharField(max_length=255, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username} - {'Paid' if self.paid else 'Pending'}"
