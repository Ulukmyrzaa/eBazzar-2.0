from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)


class Role(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='roles')


class Busket(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Products', related_name='baskets')
    categories = models.ManyToManyField('Categories', related_name='baskets')


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.CharField(max_length=255)
    busket = models.OneToOneField(Busket, on_delete=models.CASCADE, related_name='photo')
    employee = models.OneToOneField('Employee', on_delete=models.CASCADE, related_name='photo')
    categories = models.ManyToManyField('Categories', related_name='photos')


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField('Categories', related_name='category_products')
    roles = models.ManyToManyField('Role', related_name='role_products')


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Products, related_name='categories')
    photos = models.ManyToManyField(Photo, related_name='categories')


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, related_name='employee')


def __str__(self):
    return self.name
