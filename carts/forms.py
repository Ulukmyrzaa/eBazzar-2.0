from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if user_profile:
            self.fields['name'].initial = user_profile.name
            self.fields['phone_number'].initial = user_profile.phone_number
            self.fields['address'].initial = user_profile.address

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Добавьте здесь необходимую валидацию для номера телефона
        return phone_number