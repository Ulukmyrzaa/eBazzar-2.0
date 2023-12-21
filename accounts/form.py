from accounts.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','name', 'surname', 'address', 'phone_number', 'email', 'gender']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email'] 