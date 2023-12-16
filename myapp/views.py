from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from myapp.form import RegisterForm


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hey {username} your account was created succesfully")
            
            
            new_user = authenticate(username=form.cleaned_data['email'],
                                password=form.cleaned_data['password1'])
            login(request, new_user)
            
            return redirect('index')
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'core/signup.html', context )

def index(request):
    return render(request, 'core/index.html')

