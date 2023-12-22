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

    # Метод для добавления элемента в корзину с указанным товаром и количеством
    def add_item(self, product, quantity):
        basket_item, created = BasketItem.objects.get_or_create(basket=self, product=product)
        basket_item.quantity += quantity
        basket_item.save()

    # Метод для удаления элемента из корзины для указанного товара:

    def remove_item(self, product):
        BasketItem.objects.filter(basket=self, product=product).delete()

    # Метод получения общей стоимости конкретного товара в корзине
    def get_item_total_price(self, basket_item_id):
        try:
            basket_item = BasketItem.objects.get(id=basket_item_id, basket=self)
            return basket_item.total_price_for_product()
        except BasketItem.DoesNotExist:
            return 0

    def __str__(self):
        return f'BasketItem #{self.id} - {self.product.name} - Quantity: {self.quantity}'

    # Метод очистки корзины путем удаления всех элементов
    def clear(self):
        BasketItem.objects.filter(basket=self).delete()


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    total_price = models.PositiveIntegerField()
    basket_item = models.ForeignKey(BasketItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Waiting Payment')
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f'Order #{self.id} - Status: {self.status}'

    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def get_total_price(self):
        return self.total_price

    def is_paid(self):
        return self.status == 'PAID'

    def mark_as_paid(self):
        self.status = 'PAID'
        self.save()

    def cancel(self):
        self.status = 'CANCELED'
        self.save()

    def refund(self):
        self.status = 'REFUNDED'
        self.save()

    def is_shipped(self):
        return self.status == 'SHIPPED'

    def mark_as_shipped(self):
        self.status = 'SHIPPED'
        self.save()

    def is_waiting_payment(self):
        return self.status == 'WAITING_PAYMENT'

    def is_processing(self):
        return self.status == 'PROCESSING'

    def is_error(self):
        return self.status == 'ERROR'

    def is_canceled(self):
        return self.status == 'CANCELED'

    def is_partially_shipped(self):
        return self.status == 'PARTIALLY_SHIPPED'

    def is_on_hold(self):
        return self.status == 'ON_HOLD'
