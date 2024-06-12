from django.urls import path, re_path
from .views import *
from products import *

urlpatterns = [
    path("create/", CreateProductView.as_view(), name="create-product"),
    path('', ProductListView.as_view(), name='product-list'),
    re_path(r'^(?P<category_path>[-\w]+(?:/[-\w]+)*)', ProductListView.as_view(), name='products_list'),
    #path('<slug:category_slug>/<slug:product_slug>/', ProductDetailsView.as_view(), name='product_detail'),
]