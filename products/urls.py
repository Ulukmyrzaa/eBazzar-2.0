from django.urls import path
from .views import *
from products import *

urlpatterns = [
    path("create/", CreateProductView.as_view(), name="create-product"),
    path('', ProductListView.as_view(), name='product-list'),
    path('<slug:category_slug>/', ProductListView.as_view(), name='product-list-category'),
    path('<str:category_slug>/<slug:slug>/', ProductDetailsView.as_view(), name='product_detail'),
]
