from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from myapp.form import RegisterForm


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save()       
            return redirect('index')
    else:
        form = RegisterForm()
        
    context = {'form': form}
    return render(request, 'core/signup.html', context )

def index(request):
    return render(request, 'core/index.html')

