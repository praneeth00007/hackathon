from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import UserProfile, Payment
from PublisherApp.models import Doctor, Tutor
import razorpay
import qrcode
from io import BytesIO
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings

# Utility function to send emails
def send_user_email(subject, message, recipient_email):
    send_mail(
        subject=subject,
        message=message,
        from_email='gamingwithsunny27@gmail.com',  # Replace with your email
        recipient_list=[recipient_email],
        fail_silently=False,
    )

# Function to generate UPI QR Code
def generate_upi_qr(doctor_or_tutor):
    upi_id = "9121378516@ybl"  # Replace with the actual UPI ID
    amount = 10  # Replace with the actual amount
    upi_url = f"upi://pay?pa={upi_id}&pn={doctor_or_tutor.name}&mc=0000&tid=123456&amount={amount}"
    qr = qrcode.make(upi_url)
    qr_io = BytesIO()
    qr.save(qr_io, 'PNG')
    qr_io.seek(0)
    return qr_io

@login_required
def user_home(request):
    doctors = Doctor.objects.all()
    tutors = Tutor.objects.all()
    success_message = None
    qr_code_image = None

    if request.method == 'POST':
        if 'register_doctor' in request.POST:
            doctor_id = request.POST.get('doctor')
            doctor = Doctor.objects.get(id=doctor_id)
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.doctor = doctor
            profile.save()

            # Handle UPI QR Code generation
            payment_method = request.POST.get('payment')
            if payment_method == 'upi':
                qr_code_image = generate_upi_qr(doctor)

            success_message = f"Successfully registered for Doctor: {doctor.name}. Please complete the payment."

        if 'register_tutor' in request.POST:
            tutor_id = request.POST.get('tutor')
            tutor = Tutor.objects.get(id=tutor_id)
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.tutor = tutor
            profile.save()

            # Handle UPI QR Code generation
            payment_method = request.POST.get('payment')
            if payment_method == 'upi':
                qr_code_image = generate_upi_qr(tutor)

            success_message = f"Successfully registered for Tutor: {tutor.name}. Please complete the payment."

    return render(request, 'UserApp/user_home.html', {
        'success_message': success_message,
        'doctors': doctors,
        'tutors': tutors,
        'qr_code_image': qr_code_image,
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    try:
        # Fetch the user profile
        profile = UserProfile.objects.get(user=request.user)
        doctor = profile.doctor
        tutor = profile.tutor
        payment_status = Payment.objects.filter(user=request.user).first()  # Fetch payment status
    except UserProfile.DoesNotExist:
        profile = None
        doctor = None
        tutor = None
        payment_status = None

    if request.method == 'POST':
        if profile:  # Ensure the profile exists before modifying it
            # Cancel Doctor Registration
            if 'cancel_doctor' in request.POST:
                profile.doctor = None
                profile.save()
                doctor = None  # Update local variable

            # Cancel Tutor Registration
            if 'cancel_tutor' in request.POST:
                profile.tutor = None
                profile.save()
                tutor = None  # Update local variable

        # Reload the page to reflect changes
        return redirect('UserApp:profile')

    # Render the profile page
    return render(request, 'UserApp/profile.html', {
        'user': request.user,
        'doctor': doctor,
        'tutor': tutor,
        'payment_status': payment_status,  # Include payment status
    })

# Razorpay Payment Integration
def initiate_payment(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

    amount = 10  # 10 INR in paise
    payment = client.order.create({
        'amount': amount,  # Amount in paise
        'currency': 'INR',
        'payment_capture': '1',
    })

    # Create a new Payment record in the database
    payment_obj = Payment(user=request.user, amount=10, paid=False, order_id=payment['id'])
    payment_obj.save()

    # Return the payment object to be used in the front end
    return render(request, 'payment.html', {'payment': payment, 'user': request.user})


def verify_payment(request):
    payment_id = request.POST['razorpay_payment_id']
    order_id = request.POST['razorpay_order_id']
    signature = request.POST['razorpay_signature']

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
    try:
        # Verify payment signature
        client.utility.verify_payment_signature({
            'razorpay_payment_id': payment_id,
            'razorpay_order_id': order_id,
            'razorpay_signature': signature
        })

        # Mark payment as successful
        payment = Payment.objects.get(order_id=order_id)
        payment.paid = True
        payment.save()

        # Handle successful registration after payment
        profile = UserProfile.objects.get(user=request.user)
        profile.is_registered = True  # Assuming you have this field to track registration status
        profile.save()

        messages.success(request, "Payment successful! You are now fully registered.")
        return redirect('UserApp:profile')

    except razorpay.errors.SignatureVerificationError:
        messages.error(request, "Payment verification failed.")
        return redirect('failure_url')


# Custom 404 error view
def page_not_found(request, page):
    return HttpResponseNotFound(f"Page '{page}' not found.")
