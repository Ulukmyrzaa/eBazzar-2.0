from django.urls import path
from accounts.views import *

urlpatterns = [
    path('', index, name='index'),
    path('signup/', Account.as_view(), name='signup'),
    path('signin/', user_login, name='signin'),
    path('signout/', user_logout, name='signout'),

]


