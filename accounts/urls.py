from django.urls import path
from accounts.views import *

urlpatterns = [
    path('', index, name='index'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('edit_profile/', EditView.as_view(), name='edit_profile'),
    path('delete_user/', DeleteView.as_view(), name='delete_user'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('wishlist/', WishListView.as_view(), name='wishlist'), 
    path('wish/add/<int:product_id>', WishAddView.as_view(), name='wish'), 
    # path('error/', error_page, name='error_page'),

]

# handler404 = 'error_page'