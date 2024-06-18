from django.urls import path, re_path
from .views import *
from products import *

urlpatterns = [
    path("create/", CreateProductView.as_view(), name="create-product"),
    path('details/<slug:slug>/', ProductDetailsView.as_view(), name='product_details'),
    re_path(r'^(?P<category>[-\w]+)(?:/(?P<sub_category>[-\w]+))?/?$', CategoryListView.as_view(), name='category_list'),
    re_path(r'^(?P<category_path>[-\w]+/(?:[-\w]+/)*[-\w]+/?)$', ProductListView.as_view(), name='product_list'),
    path('', ProductListView.as_view(), name='product-list'),
]

