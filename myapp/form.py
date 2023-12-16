from django import forms
from myapp.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','address', 'birth_date', 'phone_number', 'email']
