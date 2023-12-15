from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Bucket(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name="buckets")
    products = models.ManyToManyField("Product", related_name="baskets")
    categories = models.ManyToManyField("Category", related_name="buckets")


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
    user_bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to="user_photos/", blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_users", blank=True
    )


class Role(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(CustomUser, related_name="roles")


class Photo(models.Model):
    link = models.CharField(max_length=255)
    bucket = models.OneToOneField(
        Bucket, on_delete=models.CASCADE, related_name="photo"
    )
    employee = models.OneToOneField(
        "Employee", on_delete=models.CASCADE, related_name="photo"
    )
    photo_categories = models.ManyToManyField("Category", related_name="photos")


class Product(models.Model):
    name = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_categories = models.ManyToManyField("Category", related_name="products")
    roles = models.ManyToManyField(Role, related_name="products")


class Category(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    category_products = models.ManyToManyField(Product, related_name="categories")
    category_photos = models.ManyToManyField(Photo, related_name="categories")


class Employee(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="employee_profile"
    )
    employee_photo = models.OneToOneField(
        Photo, on_delete=models.CASCADE, related_name="employee_profile"
    )

    def __str__(self):
        return self.name
