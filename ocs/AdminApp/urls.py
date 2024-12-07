from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_homepage, name='project_homepage'),
    path('register/', views.register, name='register'),
    path('auth_login/', views.auth_login, name='auth_login'),
    path('auth_logout/', views.auth_logout, name='logout'),
    path('chat-endpoint/', views.chat_endpoint, name='chat_endpoint'),
]