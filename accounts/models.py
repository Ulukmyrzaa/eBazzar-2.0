from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import pre_save
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=90, blank=True, null=True)
    user_profile = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    
    
class User(AbstractUser):   
    name = models.CharField(max_length=90, blank=True, null=True)
    surname =  models.CharField(max_length=90, blank=True, null=True)
    address = models.CharField(max_length=90, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    photo = models.ImageField(upload_to="user_photos/", blank=True, null=True)
    role_user = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)
    email = models.EmailField(max_length=60, unique=True)
    groups = models.ManyToManyField(Group, related_name="user_groups", blank=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"    
          
              
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    credit_card = models.IntegerField(blank=True, null=True)  
    total_item_purchased = models.IntegerField(default=0)
    total_spend = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    orders_user = models.OneToOneField('myapp.Order', on_delete=models.SET_NULL, null=True, blank=True)
    basket = models.ForeignKey(
          'myapp.Basket', on_delete=models.CASCADE, related_name='user_basket', null=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_users", blank=True
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    product_addes_ids = models.IntegerField(blank=True, null=True) 
    pavilion = models.CharField(max_length=90, blank=True, null=True)   
    is_active = models.BooleanField(default=True)
    last_active = models.DateTimeField(auto_now=True)