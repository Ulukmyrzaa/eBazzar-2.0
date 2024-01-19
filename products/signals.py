from django.utils.text import slugify
from django.dispatch import receiver
from django.forms import ValidationError
from django.db.models.signals import pre_save, post_save
from products.models import *


@receiver(pre_save, sender=Product)
def validate_product(sender, instance, **kwargs):
    # Проверка цены
    if instance.price is not None and (instance.price < 0 or instance.price > 99999):
        raise ValidationError("Цена должна быть в диапазоне от 0 до 99999.")


@receiver(pre_save, sender=ProductDetails)
def validate_product_details(sender, instance, **kwargs):
    # Проверка срока годности
    if instance.prod_date > instance.exp_date:
        raise ValidationError(
            "Дата производства не может быть позже, чем дата истечения срока или  ."
        )


@receiver(pre_save, sender=Product)
def product_creation(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)


@receiver(post_save, sender=ProductDetails)
def seller_product_info_creation(sender, instance, created, **kwargs):
    if created:
        SellerProductInfo.objects.create(product_details=instance)
