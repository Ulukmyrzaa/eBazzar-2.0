from django.urls import path
from .views import *
from products import *

urlpatterns = [
    path("create/", CreateProductView.as_view(), name="create-product"),
    path('<slug:slug>/', ProductDetailsView.as_view(), name='product_detail'),
    path('all/', ProductListView.as_view(), name='all_products'),
]
