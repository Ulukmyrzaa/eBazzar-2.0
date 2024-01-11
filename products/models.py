import datetime
from django.db.models.signals import pre_save
from django.db import models
from django.db.models import Sum
from django.core.validators import MaxValueValidator
from django.dispatch import receiver
from django.forms import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

STATUS_CHOICES = [
    ("ON_CREATION", "On creation"),
    ("ON_REVIEW", "On review"),
    ("IN_STOCK", "In stock"),
    ("UNAVILABLE", "Unavailable"),
    ("SOLD", "Sold"),
]


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category_image = models.ImageField(upload_to="category_images/")

    @property
    def get_number_of_products(self):
        return self.product_set.filter(details__status="IN_STOCK").count()

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", args=[self.slug])


class Product(models.Model):
    name = models.TextField()
    price = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    product_details = models.OneToOneField(
        "ProductDetails",
        on_delete=models.CASCADE,
        related_name="product_details",
        null=False,
        blank=False,
    )

    # def average_rating(self):
    #     return self.product_info.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']


class ProductDetails(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    prod_date = models.DateField(
        default=now, null=False, blank=False
    )
    exp_date = models.DateField(null=False, blank=False)
    total_views = models.PositiveIntegerField(default=0, blank=False, null=False)
    total_items_sold = models.PositiveIntegerField(default=0, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="On creation"
    )
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    product_category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, related_name="category_products"
    )
    # reviews = models.ManyToManyField(Review, related_name="product_reviews")

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])

    def days_until_expiration(self):

        remaining_days = (self.exp_date - now).days
        return remaining_days if remaining_days >= 0 else 0

    def clean(self):
        if self.prod_date and self.exp_date:
            if self.prod_date >= self.exp_date - datetime.timedelta(days=2):
                raise ValidationError(
                    "Дата производства должна быть не ранее, чем на 2 дня, чем дата просрочки."
                )


class SellerProductDetails(models.Model):
  #  created_by = models.ForeignKey()
    update_at = models.DateTimeField(auto_now=True)
    arrived_date = models.DateField(null=False, blank=False)
    total_available = models.IntegerField(default=0, blank=False, null=False)
    total_unique_views = models.PositiveIntegerField(default=0, blank=False, null=False)
    total_money_earned = models.FloatField(default=0, blank=False, null=False)

    def total_profit(self):
        return self.total_money_earned - (
            self.sales.aggregate(total_price_sold=Sum("price_sold"))["total_price_sold"]
            or 0
        )

    def total_profit_in_period(self, start_date, end_date):
        return self.sales.filter(sold_time__range=(start_date, end_date)).aggregate(
            total_price_sold=Sum("price_sold")
        )["total_price_sold"]

    def average_price_sold(self):
        total_sales = self.sales.count()
        total_price_sold = self.sales.aggregate(total=Sum("price_sold"))["total"] or 0
        if total_sales > 0:
            return total_price_sold / total_sales
        else:
            return 0

    # pavilion = models.OneToOneField(Pavilion,  related_name="pavilion_product")


class Sales(models.Model):
    sold_time = models.DateTimeField()
    price_sold = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    seller_product_details = models.ForeignKey(
        SellerProductDetails, on_delete=models.CASCADE, related_name="sales"
    )


# @receiver(pre_save, sender=ProductDetails)
# def validate_product_details(sender, instance, **kwargs):
#     # Проверка срока годности
#     if instance.prod_date > instance.arrived_date:
#         raise ValidationError(
#             "Дата производства не может быть раньше, чем дата привоза."
#         )


# @receiver(pre_save, sender=Product)
# def validate_product(sender, instance, **kwargs):
#     # Проверка цены
#     if instance.price is not None and (instance.price < 0 or instance.price > 99999):
#         raise ValidationError("Цена должна быть в диапазоне от 0 до 99999.")


@receiver(pre_save, sender=Sales)
def validate_sold_price(sender, instance, **kwargs):
    # Проверка проданной цены
    if instance.price_sold < 0 or instance.price_sold > 99999:
        raise ValidationError("Проданная цена должна быть в диапазоне от 0 до 99999.")


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


# class Wishlist(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=False, blank=False)
#     products = models.ManyToManyField(Product, related_name="wishlist_products")
#     update_date = models.DateField(null=False, blank=False)

#     STATUS_CHOICES = [
#         ('WAITING_PAYMENT', 'Waiting Payment'),
#         ('PROCESSING', 'Processing'),
#         ('SHIPPED', 'Success'),
#         ('PAID', 'Paid'),
#         ('ERROR', 'Error'),
#         ('CANCELED', 'Canceled'),
#         ('REFUNDED', 'Refunded'),
#         ('PARTIALLY_SHIPPED', 'Partially shipped'),
#         ('ON_HOLD', 'On hold'),
#         ('SHIPPED', 'Shipped')
#     ]
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WAITING_PAYMENT')
