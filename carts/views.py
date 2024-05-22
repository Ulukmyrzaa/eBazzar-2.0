from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .forms import OrderForm
from .models import Order


@login_required
def create_order(request):
    user = request.user
    user_profile = User.objects.get(user=user)

    if request.method == 'POST':
        form = OrderForm(request.POST, user_profile=user_profile)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']

            if first_name != user_profile.first_name:
                user_profile.first_name = first_name
                user_profile.save()
            if phone_number != user_profile.phone_number:
                user_profile.phone_number = phone_number
                user_profile.save()
            if address != user_profile.address:
                user_profile.address = address
                user_profile.save()

            order = Order.objects.create(user_profile=user_profile, first_name=first_name, phone_number=phone_number,
                                         address=address)
            # Другая обработка заказа
            return redirect('order_confirmation')
    else:
        form = OrderForm(user_profile=user_profile)

    context = {
        'form': form
    }

    return render(request, 'create_order.html', context)
