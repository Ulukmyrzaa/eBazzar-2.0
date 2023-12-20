from django.urls import path
from django.contrib.auth.views import LoginView
from .views import *

urlpatterns = [
    path('signup/', registration, name='signup'),
    path('signin/', user_login, name='signin'),
]
