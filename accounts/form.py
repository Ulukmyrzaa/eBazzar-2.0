from django import forms
from accounts.models import *
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
)
from products.models import Product


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["apartment_number", "street_address"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "photo", "gender"]

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
    apartment_number = forms.IntegerField(
        label="Apartment Address", required=False, validators=[MinValueValidator(1)]
    )
    street_address = forms.CharField(
        label="Street Address", max_length=90, required=False
    )

    class Meta:
        model = User
        fields = ["first_name", "email", "last_name", "phone_number", "gender"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)

        appartment_address = self.cleaned_data.get("apartment_number")
        street_address = self.cleaned_data.get("street_address")

        if appartment_address or street_address:
            # Если введены данные для адреса
            address = Address.objects.create(
                apartment_number=appartment_address, street_address=street_address
            )
            user.address = address

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["email"]


class EditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "photo", "gender"]

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
    class Meta:
        model = User
        fields = ["confirm_deletion"]

    confirm_deletion = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        help_text="Подтвердите удаление пользователя",
    )


class WishListItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Product",
        to_field_name="name",
        required=True,
    )

    class Meta:
        model = WishListItem
        fields = ["product"]


# class WishListForm(forms.ModelForm):
#     wishList_item = forms.ModelMultipleChoiceField(queryset=WishListItem.objects.all(),
#                                                    widget=forms.Select, label='Любимые товары',
#                                                    to_field_name='product')
class WishListForm(forms.ModelForm):
    wishList_item = forms.ModelMultipleChoiceField(
        queryset=WishListItem.objects.values_list("product__name", flat=True),
        widget=forms.Select,
        label="Любимые товары",
    )

    class Meta:
        model = WishList
        fields = ["wishList_item"]

    #     wishlist_item_form = WishListItemForm()

    # def __init__(self, *args, **kwargs):
    #     super(WishListForm, self).__init__(*args, **kwargs)

    #     if self.instance.wishlist:
    #         self.wishlist_item_form = WishListItemForm(instance=self.instance.wishlist)

    # def save(self, commit=True):
    #     user = super(WishListForm, self).save(commit=False)
