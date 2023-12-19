from django.urls import path
from myapp.views import index
from myapp import *

urlpatterns = [
    path("", index, name='index')
]