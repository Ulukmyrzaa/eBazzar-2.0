from django import forms
from accounts.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'address', 'phone_number', 'photo', 'gender']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'address', 'phone_number', 'email', 'gender']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email'] 
        
class EditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'address', 'phone_number', 'photo', 'email', 'gender']
        
class DeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []  # Пустой список полей, так как мы не редактируем существующие поля пользователя

    confirm_deletion = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Подтвердите удаление пользователя'
    ) 