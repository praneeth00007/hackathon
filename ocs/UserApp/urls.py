# UserApp/urls.py
from django.urls import path
from . import views

app_name = 'UserApp'  # Define app_name for namespacing

urlpatterns = [
    path('', views.user_home, name='user_home'),  # Home page for UserApp (doctor/tutor registration)
    path('profile/', views.profile, name='profile'),  # User profile page (with registration and cancellation)
    path('payment/', views.initiate_payment, name='initiate_payment'),  # Initiates payment (Razorpay)
    path('verify_payment/', views.verify_payment, name='verify_payment'),  # Verifies payment (Razorpay)
    path('<str:page>/', views.page_not_found, name='page_not_found'),  # Catch-all for undefined pages (custom 404)
]
