from django import forms
from accounts.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['appartmentAddress', 'street_address']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'phone_number', 'photo', 'gender']

    # Используйте AddressForm как форму для отображения и редактирования данных адреса
    address_form = AddressForm()

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # Если у пользователя уже есть адрес, используем его значения в форме
        if self.instance.address:
            self.address_form = AddressForm(instance=self.instance.address)

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        
        # Обработка данных формы адреса
        address_form = AddressForm(self.data, instance=self.instance.address)
        
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.save()
            user.address = address

        if commit:
            user.save()

        return user 
        

class RegisterForm(UserCreationForm):
    appartmentAddress = forms.IntegerField(
        label='Apartment Address',
        required=False,
        validators=[MinValueValidator(1)]
    )
    street_address = forms.CharField(
        label='Street Address',
        max_length=90,
        required=False
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'surname', 'phone_number', 'gender']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)

        appartment_address = self.cleaned_data.get('appartmentAddress')
        street_address = self.cleaned_data.get('street_address')

        if appartment_address or street_address:
            # Если введены данные для адреса
            address = Address.objects.create(
                appartmentAddress=appartment_address,
                street_address=street_address
            )
            user.address = address

        if commit:
            user.save()

        return user    
    
    
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email'] 
    
        
class EditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'phone_number', 'photo', 'gender']

    address_form = AddressForm()

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)

        # Если у пользователя уже есть адрес, используем его значения в форме
        if self.instance.address:
            self.address_form = AddressForm(instance=self.instance.address)

    def save(self, commit=True):
        user = super(EditForm, self).save(commit=False)
        
        # Обработка данных формы адреса
        address_form = AddressForm(self.data, instance=self.instance.address)
        
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.save()
            user.address = address

        if commit:
            user.save()

        return user 
    
        
class DeleteForm(forms.ModelForm):
    address =  Address()
    class Meta:
        model = User
        fields = []  # Пустой список полей, так как мы не редактируем существующие поля пользователя

    confirm_deletion = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Подтвердите удаление пользователя'
    ) 