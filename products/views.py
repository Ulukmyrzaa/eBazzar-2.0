from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from products.models import *
from .utils import *
from .form import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.db import transaction


class CreateProductView(CreateView):
    model = Product
    form_class = CombinedProductForm
    template_name = "products/create_product.html"
    success_url = reverse_lazy("product-list")


    def form_valid(self, form):
        product_form = ProductForm(self.request.POST)
        product_details_form = ProductDetailsForm(self.request.POST)

        if product_form.is_valid() and product_details_form.is_valid():
            product = form.save(commit=False)
            product.slug = product.name
            product.save()

            product_details = product_details_form.save(commit=False)
            product_details.product = product
            product_details.save()

            return super().form_valid(form)

        else:
            return self.form_invalid(form)


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"


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


# def add_product(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         total_price = float(request.POST.get('total_price'))
#         quantity = int(request.POST.get('quantity'))
#         category_id = int(request.POST.get('category_id'))

#         product_info_data = {
#             'price': float(request.POST.get('price')),
#             'arrived_date': request.POST.get('arrived_date'),
#             'prod_date': request.POST.get('prod_date'),
#             'exp_date': request.POST.get('exp_date'),
#             'status': request.POST.get('status'),
#             'rating': float(request.POST.get('rating'))
#         }

#         product = create_product(name, total_price, quantity, category_id, product_info_data)
#         return render(request, 'success.html', {'product': product})

#     else:
#         # Если не POST-запрос, отобразить форму для добавления товара
#         return render(request, 'add_product.html')


# def all_products(request):
#     products = Product.objects.all()
#     return render(request, 'all_products.html', {'products': products})


# def product_detail(request, product_id):
#     try:
#         product = Product.objects.get(id=product_id)
#         return render(request, 'product_detail.html', {'product': product})
#     except Product.DoesNotExist:
#         error_message = 'Такого товара не существует.'
#         return render(request, 'error.html', {'error_message': error_message})


# def get_products_by_category(request, category_id):
#     try:
#         category = Category.objects.get(id=category_id)
#         products = Product.objects.filter(product_category=category)
#         return render(request, 'products_by_category.html', {'products': products})
#     except Category.DoesNotExist:
#         error_message = 'Категория не существует.'
#         return render(request, 'error.html', {'error_message': error_message})
#     except Product.DoesNotExist:
#         error_message = 'Товаров в данной категории не существует.'
#         return render(request, 'error.html', {'error_message': error_message})
