from django.urls import path
from myapp.views import index
from myapp import *
from . import views

urlpatterns = [
    path("", index)
]