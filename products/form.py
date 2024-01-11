from django import forms
from .models import *
from django import forms
from django.db import transaction
from .models import Product, ProductDetails


class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = ProductDetails
        fields = ["description", "prod_date", "exp_date", "product_category"]


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price']



class CombinedProductForm(forms.ModelForm):
    product_form = ProductForm(prefix="product")
    product_details_form = ProductDetailsForm(prefix="details")

    class Meta:
        model = Product
        fields = ['name', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.update(self.product_details_form.fields)


    def save(self, commit=True):
        product = super().save(commit=False)
        product_details = ProductDetails(
            slug=self.cleaned_data['name'],  # Используем имя продукта в качестве slug
            description=self.cleaned_data['description'],
            prod_date=self.cleaned_data['prod_date'],
            exp_date=self.cleaned_data['exp_date'],
            product=product,
            product_category=self.cleaned_data['product_category']
        )
        if commit:
            with transaction.atomic():
                product.save()
                product_details.product = product
                product_details.save()
        return product
    
class SellerProductDetailsForm(forms.ModelForm):
    class Meta:
        model = SellerProductDetails
        fields = "__all__"


class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = "__all__"
