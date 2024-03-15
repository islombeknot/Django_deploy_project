from django.urls import path
from .views import *

app_name = 'patient'

urlpatterns = [
    # Page urls
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('service/', service, name='service'),
    path('price/', price, name='price'),
    path('team/', team, name='team'),
    path('testimonial/', testimonial, name='testimonial'),
    path('appointment/', appointment, name='appointment'),
    path('contact/', contact, name='contact'),

    # Authentication urls
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', ProfileUserView.as_view(), name='profile'),

    # Main url(Make Appointment)
    path('make_appointment/', make_appointment, name='make_appointment'),
    path('appointment_history/', appointment_history, name='appointment_history'),
]
