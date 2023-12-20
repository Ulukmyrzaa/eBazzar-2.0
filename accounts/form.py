from accounts.models import *
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'user','name', 'surname', 'address', 'phone_number', 'email', 'gender']
