from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone
from accounts.models import User
from products.models import Product


class Basket(models.Model):
    id = models.AutoField(primary_key=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Basket #{self.id} - {self.user.username}'


class BasketItem(models.Model):
    id = models.AutoField(primary_key=True)
    basket = models.ForeignKey(Basket, on_delete=models.PROTECT)
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    added_time = models.DateTimeField(auto_now_add=True)

    def total_price_for_product(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'BasketItem #{self.id} - {self.product.name} - Quantity: {self.quantity}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('WAITING_PAYMENT', 'Waiting Payment'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Success'),
        ('PAID', 'Paid'),
        ('ERROR', 'Error'),
        ('CANCELED', 'Canceled'),
        ('REFUNDED', 'Refunded'),
        ('PARTIALLY_SHIPPED', 'Partially shipped'),
        ('ON_HOLD', 'On hold'),
        ('SHIPPED', 'Shipped')
    ]

    id = models.AutoField(primary_key=True)
    total_price = models.PositiveIntegerField()
    basket_item = models.OneToOneField(BasketItem, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Waiting Payment')
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f'Order #{self.id} - Status: {self.status}'