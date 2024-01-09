from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    class createProduct:
        model = Product
        fields = "name, price"


class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = ProductDetails
        fields = "__all__"

    class createProductDetails:
        model = Product
        fields = "description, prod_date, exp_date, product_category, quanity_available"


class CombinedProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_form = ProductForm(*args, **kwargs)
        self.product_details_form = ProductDetailsForm(*args, **kwargs)

    def is_valid(self):
        return self.product_form.is_valid() and self.product_details_form.is_valid()


    # class Meta:
    #     model = ProductDetails 
    #     fields = [
    #         "name",
    #         "price",
    #         "photo",
    #         "description",
    #         "prod_date",
    #         "exp_date",
    #         "views",
    #         "total_items_sold",
    #         "product_category",
    #         "quantity_available",
    #         "status",
    #     ]


class SellerProductDetailsForm(forms.ModelForm):
    class Meta:
        model = SellerProductDetails
        fields = "__all__"


class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = "__all__"
