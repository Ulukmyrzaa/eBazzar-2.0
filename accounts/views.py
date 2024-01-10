from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import TemplateView, LogoutView
from accounts.form import *
from django.urls import reverse
from django.db import transaction


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

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  

        context = {'form': form}
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