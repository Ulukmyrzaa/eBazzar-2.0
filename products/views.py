from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
    TemplateView,
)
from products.models import *
from .utils import *
from .form import *
from django.views.generic.edit import CreateView
from django.db import transaction
from django.db.models import Q


class ProductDetailsView(DetailView):
    model = Product
    template_name = "products/product_details.html"
    context_object_name = "product_details"
    slug_url_kwarg = "slug"

    def get_object(self):
        product_slug = self.kwargs.get("slug")
        product = get_object_or_404(Product, slug=product_slug)
        productDetails = get_object_or_404(ProductDetails, product=product)

        return productDetails


class CreateProductView(CreateView):
    model = Product
    form_class = CombinedProductForm
    template_name = "products/create_product.html"
    success_url = "/product/"

    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save(commit=True)

        product_details = ProductDetailsForm(self.request.POST).save(commit=False)
        product_details.product = self.object
        product_details.save()

        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    template_name = "products/products_list.html"
    context_object_name = "products"

    def get_queryset(self):
        category_path = self.kwargs.get("category_path")

        category = (
            Category.check_category_path_hierarchy(category_path)
            if category_path
            else None
        )
        return category.get_products() if category else Product.objects.all()


class CategoryListView(TemplateView):
    template_name = "products/category_list.html"

    def get_queryset(self):
        category_slug = self.kwargs.get("category")
        sub_category_slug = self.kwargs.get("sub_category")

        category = (
            Category.check_category_path_hierarchy(
                category_slug + "/" + sub_category_slug
            )
            if sub_category_slug
            else get_object_or_404(Category, slug=category_slug)
        )

        return category.get_children()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_category"] = self.kwargs.get(
            "sub_category"
        ) or self.kwargs.get("category")
        context["categories"] = self.get_queryset()  # Передайте все категории
        return context


class UpdateProductView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "update_product.html"
    context_object_name = "product"
    success_url = "/product-list/"


class DeleteProductView(DeleteView):
    model = Product
    template_name = "delete_product.html"
    context_object_name = "product"
    success_url = "/product-list/"
