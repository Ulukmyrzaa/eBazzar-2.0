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
            categories = category_slug.split('/')
            return Product.objects.filter(product_category__slug__in=categories)
        else:
            return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            categories = category_slug.split('/')
            context['current_category'] = Category.objects.filter(slug__in=categories).first()
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


# def product_detail(request, product_id):
#     try:
#         product = Product.objects.get(id=product_id)
#         return render(request, 'product_detail.html', {'product': product})
#     except Product.DoesNotExist:
#         error_message = 'Такого товара не существует.'
#         return render(request, 'error.html', {'error_message': error_message})
