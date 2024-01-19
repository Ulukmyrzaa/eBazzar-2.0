from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import TemplateView, LogoutView
from accounts.form import *
from django.urls import reverse


def index(request):
    return render(request, 'index.html')


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        form = ProfileForm(instance=user)
        context = {'user': user, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        context = {'user': user, 'form': form}
        return render(request, self.template_name, context)

class Account(TemplateView):
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
    
    
class WishListItemView(TemplateView):
    template_name = 'accounts/wishlist.html'
    form_class = WishListItemForm
    
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            wishlist_item = get_object_or_404(WishListItem, pk=pk)
            form = self.form_class(instance=wishlist_item)
        else:
            form = self.form_class()    
        return render(request, self.template_name, {'form': form})
        
    def post(self, request, pk=None, *args, **kwargs):
        if pk:
            wishlist_item = get_object_or_404(WishListItem, pk=pk)
            form = self.form_class(request.POST, instance=wishlist_item)
        else:
            form = self.form_class(request.POST)
        form = self.form_class(request.POST)
                
        if form.is_valid(): 
            existing_item = None    
            
            if form.cleaned_data.get('product'):
                existing_item = WishListItem.objects.filter(
                    product=form.cleaned_data['product']
                ).first()    
            
            if existing_item:
                quantity_change = int(request.POST.get('increase', 0)) - int(request.POST.get('decrease', 0))                
                existing_item.quantity += quantity_change
                new_quantity = existing_item.quantity                
                if existing_item.quantity < 1:
                    existing_item.delete()  
                else:
                    existing_item.save()
            
            return render(request, self.template_name, {'form': form}, {'new_quantity': new_quantity} )
              
                                   
             
        return render(request, self.template_name, {'form': form}, )
    

   