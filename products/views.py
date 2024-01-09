from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views import View
from products.models import *
from .utils import *
from .form import *


class CreateProductView(CreateView):
    model = Product
    form_class = CombinedProductForm
    template_name = 'create_product.html'
    success_url = '/product-list/'

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, 'create_product.html', {'form': form})
    
    def get(self, request):
        form = ProductForm()
        return render(request, 'create_product.html', {'form': form})


# Классовое представление для чтения списка продуктов
class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})

# Классовое представление для обновления продукта
class UpdateProductView(View):
    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        form = ProductForm(instance=product)
        return render(request, 'update_product.html', {'form': form})

    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, 'update_product.html', {'form': form})

# Классовое представление для удаления продукта
class DeleteProductView(View):
    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        product.delete()
        return redirect('product_list')
    



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