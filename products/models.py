from django.db import models
from django.db.models import Sum
from django.core.validators import MaxValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import datetime
from mptt.models import MPTTModel
from products.models import *


STATUS_CHOICES = [
    ("ON_REVIEW", "On review"),
    ("IN_STOCK", "In stock"),
    ("UNAVILABLE", "Unavailable"),
    ("SOLD", "Sold"),
]

MEASUREMENT_UNIT = [
    ("GRAM", 'Грамм'),
    ("KG", 'Килограмм '),
    ("UNIT", 'Штук'),
]


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category_image = models.ImageField(upload_to="category_images/")
    level = models.IntegerField(default=0, editable=False)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        blank=True,
        null=True
    )

    @property
    def get_number_of_products(self):
        return self.category_products.filter(details__status="IN_STOCK").count()

    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("category", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    product_category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, related_name="category_products"
    )

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])

    # def average_rating(self):
    #     return self.product_info.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']


class ProductDetails(models.Model):
    description = models.CharField(max_length=500, blank=True, null=True)
    prod_date = models.DateField(default=now, null=False, blank=False)
    exp_date = models.DateField(null=True, blank=True)
    total_views = models.PositiveIntegerField(default=0, blank=False, null=False)
    total_items_sold = models.PositiveIntegerField(default=0, blank=True, null=True)    
    total_available = models.IntegerField(default=0, blank=False, null=False)
    measurement_unit = models.CharField(
        max_length=20, choices=MEASUREMENT_UNIT, default="Штук"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="On review"
    )
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, null=False, blank=False
    )

    # reviews = models.ManyToManyField(Review, related_name="product_reviews")

    def days_until_expiration(self):
        remaining_days = (self.exp_date - datetime.now().date()).days
        return max(remaining_days, 0)



class SellerProductInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_money_earned = models.DecimalField(default=0, decimal_places=2, max_digits=9, blank=False, null=False)
    product_details = models.OneToOneField(
        ProductDetails, on_delete=models.CASCADE, null=False, blank=False
    )
    # pavilion = models.OneToOneField(Pavilion,  related_name="pavilion_product")


    def total_profit_in_period(self, start_date, end_date):
        return self.sales.filter(sold_time__range=(start_date, end_date)).aggregate(
            total_price_sold=Sum("price_sold")
        )["total_price_sold"]



class Sales(models.Model):
    sale_time = models.DateTimeField()
    total_items_sold = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=9, decimal_places=2)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sold_product"
    )




# class Review(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=False, blank=False)
#     text = models.TextField(blank=False, null=False)
#     creation_date = models.DateTimeField(null=False, blank=False)
#     photo = models.ImageField(upload_to="review_photos/", blank=True, null=True)
#     rating = models.DecimalField(
#         max_digits=2,
#         decimal_places=1,
#         validators=[MinValueValidator(1), MaxValueValidator(5)],
#     )


# class Pavilion(models.Model):
#     name = models.TextField(blank=False, null=False)
#     descritpion = models.TextField(blank=False, null=False)
#     address = models.CharField(max_length=30, blank=False, null=False)
#     rating = models.DecimalField(
#         max_digits=2,
#         decimal_places=1,
#         validators=[MinValueValidator(1), MaxValueValidator(5)],
#     )
#     photo = models.ImageField(upload_to="pavilion_photos/", blank=True, null=True)
#     # reviews = models.ManyToManyField(Review, related_name="pavilion_reviews")
#     main_phone_number = models.CharField(max_length=15, blank=True, null=True)
#     additional_phone_number = models.CharField(max_length=15, blank=True, null=True)
#     owners = models.ManyToManyField(CustomUser, related_name="owned_pavilions")
#     employees = models.ManyToManyField(CustomUser, related_name="pavilion_employees")
#     products = models.ManyToManyField(Product, related_name="pavilion_products")
#     categories = models.ManyToManyField(Category, related_name="pavilion_categories")