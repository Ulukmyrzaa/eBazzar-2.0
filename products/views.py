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
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category_slugs = category_slug.split('/')
            if len(category_slugs) == 1:
                category = get_object_or_404(Category, slug=category_slugs[0])
                return category.category_products.all()
            else:
                parent_category = get_object_or_404(Category, slug=category_slugs[0])
                return Product.objects.filter(product_category__in=parent_category.get_descendants(include_self=True))
        else:
            return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category_slugs = category_slug.split('/')
            if len(category_slugs) == 1:
                context['current_category'] = get_object_or_404(Category, slug=category_slugs[0])
            else:
                context['current_category'] = get_object_or_404(Category, slug=category_slugs[0])
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