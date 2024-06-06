from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import TemplateView, LogoutView
from django.views import View
from accounts.form import *
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from products.models import Product
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, 'index.html')


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        form = ProfileForm(instance=user)
        context = {'user': user, 'form': form}
        return render(request, self.template_name, context)

    # def post(self, request, *args, **kwargs):
    #     user = request.user
    #     form = ProfileForm(request.POST, request.FILES, instance=user)
    #     if form.is_valid():
    #         form.save()
    #     context = {'user': user, 'form': form}
    #     return render(request, self.template_name, context)

class RegisterView(TemplateView):
    template_name = 'accounts/signup.html'
    form_class = RegisterForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # Записываем email в поле username
            user.save()
            email = form.cleaned_data.get("email")

            # Аутентификация только что зарегистрированного пользователя
            authenticated_user = authenticate(request, email=email, password=form.cleaned_data['password1'])

            if authenticated_user is not None:
                login(request, authenticated_user)
                WishList.objects.create(user=user)
                return redirect('/')

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

  
class LoginView(TemplateView):
    template_name = 'accounts/signin.html'
    
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('profile'))
        
        context = {'form': form}
        return render(request, 'profile', context)        


class LogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return redirect('/')


class EditView(TemplateView):
    template_name = 'accounts/edit_profile.html'
    form_class = EditForm
    addres_form_class = AddressForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        address_form = self.addres_form_class(instance=request.user.address)
        context = {'form': form, 'address_form': address_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        address_form = self.addres_form_class(request.POST, instance=request.user.address)        
        if form.is_valid() and address_form.is_valid():
            form.save()
            address_form.save()
            return redirect('profile')  

        context = {'form': form, 'address_form': address_form}
        return render(request, self.template_name, context)
    
    
class DeleteView(TemplateView):
    template_name = 'accounts/delete_user.html' 
    form_class = DeleteForm  

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)

        if form.is_valid() and form.cleaned_data['confirm_deletion']:
            user = request.user
            
            if user.address:
                user.address.delete()
                
            user.delete()
            return redirect('/')  
        return render(request, self.template_name, {'form': form})    
    

# class WishListItemView(TemplateView):
#     template_name = 'accounts/wishlist.html'
#     form_class = WishListItemForm
   
#     def get(self, request,*args, **kwargs):
#         user = request.user
#         form = self.form_class()    
#         return render(request, self.template_name, {'user':user, 'form': form})
        
#     def post(self, request, *args, **kwargs):
    #     user = request.user
    #     form = self.form_class(request.POST)

    #     if form.is_valid():
    # # Связать wishlist_item с пользователем
    #         wishlist_item = form.save(commit=False)
    #         wishlist_item.user = user
    #         wishlist_item.save()

    #         return redirect('wish')

    #     return render(request, self.template_name, {'user': user, 'form': form})
 

        
# class WishListView(TemplateView):
#     template_name = 'accounts/wishlist.html'
#     form_class = WishListForm()
    
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         form = self.form_class(user=user)
#         # context = {'form': form}
#         return render(request, self.template_name, {'user': user,'form' : form})
    
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         form = self.form_class(user=user, data=request.POST)
        
#         wishlist, _ = WishList.objects.get_or_create(user=user)
#         if form.is_valid():
#     # Связать wishlist_item с пользователем
#             wishlist= form.save(commit=False)
#             wishlist.wishlist = wishlist
#             wishlist.save()

#             return redirect('wish')

#         return render(request, self.template_name, {'user': user, 'form': form})

        
class WishListView(View):
    def post(self, request, *args, **kwargs):
        
        product_id = kwargs.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        user = User.objects.get(email='example@mail.com')
        WishList.objects.create(user=user, product=product)
       # messages.success(request, "Продукт добавлен в список желаний.")
        return redirect(product.get_absolute_url())  # Перенаправление на страницу продукта
