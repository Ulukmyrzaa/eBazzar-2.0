from datetime import timezone
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import MinValueValidator
from products.models import Product


class Role(models.Model):
    name = models.CharField(max_length=90, blank=True, null=True)
    user_profile = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    group = models.ManyToManyField(Group, related_name="roles_group", blank=True)
    

class Address(models.Model):
    appartmentAddress = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    street_address = models.CharField(max_length=90, blank=True, null=True)
    updateTime = models.DateTimeField(auto_now=True)
    
    
class User(AbstractUser):   
    name = models.CharField(max_length=90, blank=True, null=True)
    surname =  models.CharField(max_length=90, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    photo = models.ImageField(upload_to="user_photos/", blank=True, null=True)
    role_user = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)
    email = models.EmailField(max_length=60, unique=True)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    
    def __str__(self):
        full_name = f"{self.name} {self.surname}" if self.name and self.surname else "Unnamed User"
        return f"{full_name} - {self.email}"
          
              
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    credit_card = models.IntegerField(blank=True, null=True)  
    total_item_purchased = models.IntegerField(default=0)
    total_spend = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    orders_user = models.OneToOneField('carts.Order', on_delete=models.SET_NULL, null=True, blank=True)
    basket = models.ForeignKey(
          'carts.Basket', on_delete=models.CASCADE, related_name='user_basket', null=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_users", blank=True
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
class WishListItem(models.Model):
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    added_time = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)  
    
    
class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    wishList_item = models.ManyToManyField(WishListItem, related_name="wishList_item")    
    final_price = models.IntegerField(blank=True, null=True)
    
    
  

