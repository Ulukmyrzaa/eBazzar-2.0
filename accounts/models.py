from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import pre_save
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=30)
    
class CustomUser(AbstractUser):
    username = models.CharField(max_length=90, blank=True, null=True, unique=True)
    address = models.CharField(max_length=90, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    update_time = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    credit_card = models.IntegerField(blank=True, null=True)
    
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)
    
    
    basket = models.ForeignKey(
          'myapp.Basket', on_delete=models.CASCADE, related_name='user_basket', null=True
    )
    photo = models.ImageField(upload_to="user_photos/", blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_users", blank=True
    )


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


 