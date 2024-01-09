from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price"]


class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = ProductDetails
        fields = ["slug", "description", "prod_date", "exp_date", "product_category"]


ProductDetailsFormSet = forms.inlineformset_factory(
    Product, ProductDetails, form=ProductDetailsForm, extra=1
)


class CombinedProductForm(forms.ModelForm):
    name = forms.CharField(required=True)
    price = forms.DecimalField(required=True)

    slug = forms.CharField(required=True)
    description = forms.CharField(required=True)
    prod_date = forms.DateField(required=True)
    exp_date = forms.DateField(required=True)
    product_category = forms.CharField(required=True)

    class Meta:
        model = Product
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.update(ProductForm().fields)
        self.fields.update(ProductDetailsForm().fields)
        self.product_details_formset = ProductDetailsFormSet(
            *args, instance=self.instance, prefix="product_details"
        )

    def is_valid(self):
        return super().is_valid() and self.product_details_formset.is_valid()

    def save(self, commit=True):
        product = super().save(commit=commit)

        if commit:
            self.product_details_formset.instance = product
            self.product_details_formset.save()

        return product

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
