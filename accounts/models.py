from datetime import timezone
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import MinValueValidator
from products.models import Product


class Address(models.Model):
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    street_address = models.CharField(max_length=90, blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True)


class User(AbstractUser):
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    photo = models.ImageField(upload_to="user_photos/", blank=True, null=True)
    email = models.EmailField(max_length=60, unique=True)
    update_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(Group, related_name="roles_group", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True
    )

    def __str__(self):
        full_name = (
            f"{self.name} {self.last_name}"
            if self.name and self.last_name
            else "Unnamed User"
        )
        return f"{full_name} - {self.email}"


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    # credit_card = models.CharField(max_length=16, blank=True, null=True)
    total_item_purchased = models.IntegerField(default=0)
    total_spend = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # orders_user = models.OneToOneField('carts.Order', on_delete=models.SET_NULL, null=True, blank=True)
    # basket = models.ForeignKey(
    #       'carts.Basket', on_delete=models.CASCADE, related_name='user_basket', null=True
    # )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_time = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} ({self.added_time})"


    # def add_to_wishlist(self, product):
    #     wish_list_item, created = WishListItem.objects.get_or_create(product=product)
    #     self.wishList_item.add(wish_list_item)
