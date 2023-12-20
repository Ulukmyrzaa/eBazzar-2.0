from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from accounts.form import *
from django.contrib import messages


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get("email")

            # Аутентификация только что зарегистрированного пользователя
            authenticated_user = authenticate(request, email=email, password=form.cleaned_data['password1'])

            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('index')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'core/signup.html', context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'core/signin.html', context)