from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect


# Create your views here.
def project_homepage(request):

    return render(request, 'AdminApp/Projecthomepage.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User  # Ensure you have the User model imported

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['confirm-password']

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'OOPS! Username already taken.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'OOPS! Email already registered.')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                    email=email
                )
                user.save()
                messages.success(request, 'Account created successfully! You can now log in.')
                print("Redirecting to login page")  # Debugging statement
                return redirect('auth_login')  # Ensure 'auth_login' is defined in your URLs
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'AdminApp/register.html')



from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages


from django.shortcuts import redirect

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def auth_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log the user in after authentication

            if len(username) == 10:
                messages.success(request, 'Login successful as user!')
                return redirect('UserApp:user_home')  # Correct name from UserApp
            elif len(username) == 4:
                messages.success(request, 'Login successful as publisher!')
                return redirect('PublisherApp:home')  # Correct name from PublisherApp
            else:
                messages.error(request, 'Username length does not match user or publisher criteria.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'AdminApp/auth_login.html')



from django.http import JsonResponse

def chat_endpoint(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        # Placeholder response; customize as needed.
        bot_reply = f"I see you said: {user_message}"
        return JsonResponse({"reply": bot_reply})







from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect

def auth_logout(request):
    if request.user.is_authenticated:  # Check if the user is logged in
        django_logout(request)  # Log out the user
        messages.success(request, 'You have been logged out successfully.')  # Provide feedback to the user
    else:
        messages.warning(request, 'You were not logged in.')  # Inform if no user was logged in
    return redirect('project_homepage')  # Redirect to the homepage after logoutt
