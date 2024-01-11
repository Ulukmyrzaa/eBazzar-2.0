from django.urls import path
from .views import *
from products import *

urlpatterns = [
    path("create/", CreateProductView.as_view(), name="create-product"),
]
