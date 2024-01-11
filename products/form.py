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

    
class SellerProductDetailsForm(forms.ModelForm):
    class Meta:
        model = SellerProductDetails
        fields = "__all__"


class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = "__all__"
