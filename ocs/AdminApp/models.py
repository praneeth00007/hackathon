from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.password = make_password(self.password)
        super(CustomUser, self).save(*args, **kwargs)

    def clean(self):
        # Add any additional validations if needed
        if not self.username:
            raise ValidationError('Username is required')
        if not self.email:
            raise ValidationError('Email is required')

    def _str_(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'