from django.urls import path
from flask_login import login_user
from accounts.views import *

urlpatterns = [
    path('', index, name='index'),
    path('signup/', Account.as_view(), name='signup'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('edit_profile/', EditView.as_view(), name='edit_profile'),
    path('delete_user/', DeleteView.as_view(), name='delete_user'),
    path('profile/', ProfileView.as_view(), name='profile'),


]


