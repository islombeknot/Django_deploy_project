from django import forms
from .models import *
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username','email','password','password2', 'first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Kiritilgan passwordlar bir-biriga mos kelmadi!")
        return cd['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Oldin bunday email bilan ro'yhatdan o'tilgan!")
        return email


class ProfileForm(forms.ModelForm):
    username = forms.CharField(label="Username", disabled=True)
    email = forms.EmailField(label="Email", disabled=True)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email')

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'doctor', 'name', 'email', 'app_date', 'app_time']

