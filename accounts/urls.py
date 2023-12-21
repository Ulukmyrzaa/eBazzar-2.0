from django.urls import path
from accounts.views import *

urlpatterns = [
    path('signup/', registration, name='signup'),
    path('signin/', user_login, name='signin'),
]


