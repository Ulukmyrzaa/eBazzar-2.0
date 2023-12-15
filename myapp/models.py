from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Basket(models.Model):
    user = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE, related_name="user_Basket"
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField("Product", related_name="basket_products")
    categories = models.ManyToManyField("Category", related_name="basket_category")


class Role(models.Model):
    name = models.CharField(max_length=30)


class CustomUser(AbstractUser):
    address = models.CharField(max_length=90, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    user_creation_time = models.DateTimeField(null=False, blank=False)
    user_update_time = models.DateTimeField(null=False, blank=False)
    phone_number = models.CharField(unique=True, max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=90, unique=False, null=False)
    credit_card = models.IntegerField(max_length=16, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=False, blank=False)
    user_basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, null=True, blank=True
    )
    photo = models.ImageField(upload_to="user_photos/", blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_users", blank=True
    )


class Category(models.Model):
    quantity = models.IntegerField(blank=False, null=False)
    category_photo = models.ImageField(
        upload_to="category_photos/", blank=True, null=True
    )


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=False, blank=False)
    text = models.TextField(blank=False, null=False)
    creation_date = models.DateTimeField(null=False, blank=False)
    photo = models.ImageField(upload_to="review_photos/", blank=True, null=True)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )


class Product(models.Model):
    name = models.TextField(blank=False, null=False)
    add_to_basket_time = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to="product_photos/", blank=True, null=True)
    quantity = models.IntegerField(
        validators=[MaxValueValidator(999)], blank=False, null=False
    )
    product_category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="category_products"
    )
    product_info = models.OneToOneField(
        "ProductInfo", on_delete=models.CASCADE, null=False, blank=False
    )


class ProductInfo(models.Model):
    descritpion = models.CharField(max_length=500, blank=True, null=True)
    quantity_available = models.IntegerField(
        validators=[MaxValueValidator(9999)], blank=False, null=False
    )
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    arrived_date = models.DateField(null=False, blank=False)
    prod_date = models.DateField(null=False, blank=False)
    exp_date = models.DateField(null=False, blank=False)
    status = models.BooleanField(null=False, blank=False)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    reviews = models.ManyToManyField(Review, related_name="product_reviews")
    sold = models.IntegerField(
        validators=[MaxValueValidator(99999)], blank=True, null=True
    )


class Pavilion(models.Model):
    name = models.TextField(blank=False, null=False)
    descritpion = models.TextField(blank=False, null=False)
    address = models.CharField(max_length=30, blank=False, null=False)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    photo = models.ImageField(upload_to="pavilion_photos/", blank=True, null=True)
    reviews = models.ManyToManyField(Review, related_name="pavilion_reviews")
    main_phone_number = models.CharField(max_length=15, blank=True, null=True)
    additional_phone_number = models.CharField(max_length=15, blank=True, null=True)
    owners = models.ManyToManyField(CustomUser, related_name="owned_pavilions")
    employees = models.ManyToManyField(CustomUser, related_name="pavilion_employees")
    products = models.ManyToManyField(Product, related_name="pavilion_products")
    categories = models.ManyToManyField(Category, related_name="pavilion_categories")


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=False, blank=False)
    products = models.ManyToManyField(Product, related_name="wishlist_products")
    update_date = models.DateField(null=False, blank=False)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=False, blank=False)
    products = models.ManyToManyField(Product, related_name="order_products")
    creation_date = models.DateTimeField(null=False, blank=False)
    payment_date = models.DateTimeField(null=False, blank=False)
    total_price = models.DecimalField(
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(99999)],
    )
