# publisher/urls.py
from django.urls import path
from . import views
app_name = 'PublisherApp'
urlpatterns = [
    # '' indicates this is the homepage
    path('', views.home, name='home'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('tutors/', views.tutor_list, name='tutor_list'),
    path('delete_doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('delete_tutor/<int:tutor_id>/', views.delete_tutor, name='delete_tutor'),
]

