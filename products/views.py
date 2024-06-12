from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from products.models import *
from .utils import *
from .form import *
from django.views.generic.edit import CreateView
from django.db import transaction
from django.db.models import Q


class ProductDetailsView(DetailView):
    model = ProductDetails
    template_name = "products/product_details.html"
    context_object_name = "product_details"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        product_slug = self.kwargs.get('product_slug')
        categories = category_slug.split('/')
        product = get_object_or_404(Product, slug=product_slug, product_category__slug__in=categories)
        return ProductDetails.objects.filter(product=product)


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
        category_slugs = self.kwargs.get('category_path')

        # Если получен путь с категориями, то проверка на иерархию
        if category_slugs:
            category_slugs = category_slugs.split('/')
            parent_category = get_object_or_404(Category, slug=category_slugs[0])
            # Сверяемся с иерархией из полученного списка категорий 
            for i in range(1, len(category_slugs)):
                current_slug = category_slugs[i]
                child_category = get_object_or_404(Category, slug=current_slug, parent=parent_category)
                parent_category = child_category

            return parent_category.get_products()
        # Иначе выдача всех продуктов
        else:
            return Product.objects.all().filter(productdetails__status = "IN_STOCK")


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
