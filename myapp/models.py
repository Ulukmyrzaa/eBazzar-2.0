from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models


class Busket(models.Model):
    # Модель корзины покупок
    name = models.CharField(max_length=255)
    # Другие поля корзины


class CustomUser(AbstractUser):
    # Дополнительные поля для регистрации
    name = models.CharField(max_length=30, blank=True, null=True)
    firstname = models.CharField(max_length=30, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    user_creation_date = models.DateField(null=True, blank=True)
    user_update_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=90, unique=True)
    credit_card = models.CharField(max_length=16, blank=True, null=True)
    role = models.CharField(max_length=30, blank=True, null=True)
    busket = models.ForeignKey(Busket, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)


    def __str__(self):
        return self.username
