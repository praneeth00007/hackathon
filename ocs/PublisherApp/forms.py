from django import forms
from .models import Doctor, Tutor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization','email', 'timing']

class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['name', 'subject','email', 'timing']
