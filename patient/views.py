from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .forms import *
from django.views.decorators.csrf import requires_csrf_token

data = {
    "services": Service.objects.all(),
    "doctors": Doctor.objects.all(),
    "days": Date.objects.all(),
    "times": Time.objects.all(),
    "appointments": Appointment.objects.all(),
}


def index(request):
    return render(request, 'patient/index.html', context=data)

def about(request):
    return render(request, 'patient/about.html', context=data)

def service(request):
    return render(request, 'patient/service.html', context=data)

def price(request):
    return render(request, 'patient/price.html', context=data)

def team(request):
    return render(request, 'patient/team.html', context=data)

def testimonial(request):
    return render(request, 'patient/testimonial.html', context=data)

def appointment(request):
    return render(request, 'patient/appointment.html', context=data)

def login(request):
    return render(request, 'patient/login.html', context=data)

def contact(request):
    return render(request, 'patient/contact.html', context=data)

def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            if user is not None and user.is_active:
                auth_login(request,user)
                messages.success(request, ("You are now logged in successfully!"))
                return HttpResponseRedirect(reverse('patient:index'))
    data['form'] = form
    return render(request, 'patient/login.html', context=data)

def user_logout(request):
    logout(request)
    messages.success(request, ("You are now logged out successfully!"))
    return HttpResponseRedirect(reverse('patient:login'))

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(reverse('patient:login'))
    data['form'] = form
    return render(request, 'patient/register.html', context=data)

class ProfileUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileForm
    template_name = 'patient/profile.html'

    def get_success_url(self):
        return reverse_lazy('patient:index')

    def get_object(self):
        return self.request.user


@login_required(login_url="patient:login")
def make_appointment(request):
    try:
        if request.method == 'POST':
            print(request.POST)
            exist_app = Appointment.objects.filter(
                doctor = get_object_or_404(Doctor, pk=request.POST.get('doctor')),
                app_date = get_object_or_404(Date, pk=request.POST.get('weekday')),
                app_time = get_object_or_404(Time, pk=request.POST.get('time'))
            )
            if exist_app.exists():
                messages.success(request, ("Bu vaqtda belgilagan doktor uchun joy oldin band qilingan. Boshqa vaqtda yoki boshqa doktorimiz tomonidan sizga xizmat ko'rsatsak mamnun bo'lamiz!"))
                return HttpResponseRedirect(reverse('patient:index'))
                
            Appointment.objects.create(
                user_name = get_object_or_404(User, pk=request.user.id),
                service = get_object_or_404(Service, pk=request.POST.get('service')),
                doctor = get_object_or_404(Doctor, pk=request.POST.get('doctor')),
                name = request.POST.get('name'),      
                email = request.POST.get('email'),
                app_date = get_object_or_404(Date, pk=request.POST.get('weekday')),
                app_time = get_object_or_404(Time, pk=request.POST.get('time'))
            )
            messages.success(request, ("Berilgan vaqtda joy band qildingiz. Sizga xizmat ko'rsatishdan xursandmiz!"))
            return HttpResponseRedirect(reverse('patient:index'))
        return render(request, 'patient/index.html', context=data)
    
    except Exception as e:
        messages.success(request, (f"Occured error: {e}!"))
            

def appointment_history(request):
    data['appointments'] = Appointment.objects.filter(user_name=request.user)
    return render(request, 'patient/history.html', context=data)
