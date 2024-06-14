from django.urls import path, re_path
from .views import *
from products import *

urlpatterns = [
    path("create/", CreateProductView.as_view(), name="create-product"),
    path('<category>/', CategoryListView.as_view(), name='category_list'),
    path('<category>/<sub_category>', CategoryListView.as_view(), name='category_list'),
    path('<category>/<sub_category>/', CategoryListView.as_view(), name='category_list'),
    re_path(r'^(?P<category_path>[-\w]+/(?:[-\w]+/)*[-\w]+/?)$', ProductListView.as_view(), name='product_list'),
    path('', ProductListView.as_view(), name='product-list'),
    # Обрабатываем пути с товарами (более точный путь)
    #re_path(r'^(?P<category_path>[-\w]+/(?:[-\w]+/)+[-\w]+/?)$', ProductListView.as_view(), name='product_list'),
    # Обрабатываем пути с категориями (более общий путь)
   # re_path(r'^(?P<category_path>[-\w]+(?:/[-\w]+)?)$', CategoryListView.as_view(), name='category_list'),
    #path('<slug:category_slug>/<slug:product_slug>/', ProductDetailsView.as_view(), name='product_detail'),
]

