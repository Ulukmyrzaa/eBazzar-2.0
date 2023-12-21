from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import TemplateView
from accounts.form import *


def index(request):
    return render(request, 'index.html')

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
                return redirect('index')

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

# def registration(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST or None)
#         if form.is_valid():
#             user = form.save()
#             email = form.cleaned_data.get("email")

#             # Аутентификация только что зарегистрированного пользователя
#             authenticated_user = authenticate(request, email=email, password=form.cleaned_data['password1'])

#             if authenticated_user is not None:
#                 login(request, authenticated_user)
#                 return redirect('index')
#     else:
#         form = RegisterForm()

#     context = {'form': form}
#     return render(request, 'accounts/signup.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'accounts/signin.html', context)


def user_logout(request):
    logout(request)
    return render(request, 'accounts/signin.html')