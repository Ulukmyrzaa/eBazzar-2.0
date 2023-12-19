from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from accounts.form import RegisterForm

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        print(form)
        if form.is_valid():
            form.save()       
            return redirect('index')
    else:
        form = RegisterForm()
        
    context = {'form': form}
    return render(request, 'core/signup.html', context )