from django import forms


class OrderForm(forms.Form):
    name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if user_profile:
            self.fields['name'].initial = user_profile.name
            self.fields['phone_number'].initial = user_profile.phone_number
            self.fields['address'].initial = user_profile.address
