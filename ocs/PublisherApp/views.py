from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Tutor
from .forms import DoctorForm, TutorForm

# Home page that shows the doctor and tutor lists, and allows adding new ones
def home(request):
    doctors = Doctor.objects.all()
    tutors = Tutor.objects.all()

    if request.method == 'POST':
        if 'add_doctor' in request.POST:
            doctor_form = DoctorForm(request.POST)
            if doctor_form.is_valid():
                doctor_form.save()
                return redirect('PublisherApp:home')  # Redirect back to the home page
        elif 'add_tutor' in request.POST:
            tutor_form = TutorForm(request.POST)
            if tutor_form.is_valid():
                tutor_form.save()
                return redirect('PublisherApp:home')  # Redirect back to the home page
    else:
        doctor_form = DoctorForm()
        tutor_form = TutorForm()

    return render(request, 'PublisherApp/Publisherhomepage.html', {
        'doctors': doctors,
        'tutors': tutors,
        'doctor_form': doctor_form,
        'tutor_form': tutor_form
    })

# List of doctors
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'PublisherApp/doctor_list.html', {'doctors': doctors})

# List of tutors
def tutor_list(request):
    tutors = Tutor.objects.all()
    return render(request, 'PublisherApp/tutor_list.html', {'tutors': tutors})

# Delete a doctor by ID
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    return redirect('PublisherApp:home')

# Delete a tutor by ID
def delete_tutor(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    tutor.delete()
    return redirect('PublisherApp:home')
