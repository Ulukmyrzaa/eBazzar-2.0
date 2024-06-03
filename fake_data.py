from random import randint, uniform, choice
from faker import Faker
from django.utils.text import slugify
from django.db import connection, transaction
import random
import os
import django
import decimal

fake = Faker()
# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Initialize Django
django.setup()

from products.models import *
from accounts.models import *
from django.utils import timezone


def create_fake_product_data(
    num_users,
    num_products,
    num_addresses,
    num_categories,
    categories_depth,
    categories_width,
    max_num_items,
    num_max_total_sales,
    num_max_total_sold,
):
    # Удаление существующих данныз в БД
    truncate_tables()

    # Создание данных
    sub_subcategories = create_categories(
        num_categories, categories_depth, categories_width
    )
    create_products(sub_subcategories, num_products)
    addresses = create_addresses(num_addresses)
    create_users(num_users, addresses)
    create_wishList_items(max_num_items)
    create_products_sales_and_info(num_max_total_sales, num_max_total_sold)


def truncate_tables():
    cursor = connection.cursor()
    tables = [
        "accounts_user",
        "accounts_address",
        "accounts_userdetails",
        "products_product",
        "products_productdetails",
        "products_sales",
        "products_sellerproductinfo",
        "products_category",
    ]
    for table in tables:
        cursor.execute(f"TRUNCATE TABLE {table} CASCADE")
    cursor.close()


def create_addresses(num_addresses):
    addresses = []
    for _ in range(num_addresses):
        apartment_number = fake.building_number()
        street_address = fake.street_address()
        address = Address.objects.create(
            apartment_number=apartment_number,
            street_address=street_address,
        )
        addresses.append(address)
    return addresses


def create_users(num_users, addresses):
    # Создание основных данных юзеров
    users = []
    for _ in range(num_users):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        username = email.split("@")[0]
        password = fake.password()
        last_login = timezone.make_aware(fake.date_time_this_year())
        update_at = timezone.make_aware(fake.date_time_this_year())
        is_active = fake.boolean()
        photo = fake.image_url(width=200, height=200)
        address = random.choice(addresses)
        phone_number = fake.phone_number()[:13]
        gender = random.choice(["M", "F", "O"])

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            last_login=last_login,
            update_at=update_at,
            is_active=is_active,
            photo=photo,
            address=address,
            phone_number=phone_number,
            gender=gender,
        )
        users.append(user)
     
        user_details = []
        user_detail = UserDetails.objects.create(
            user=user,
            # credit_card=fake.credit_card_number()[:16],
            total_item_purchased=random.randint(0, 100),
            total_spend=round(uniform(0.0, 9999.99), 2),
            
        )
        user_details.append(user_detail)

    return users


def create_wishList_items(max_num_items):
        # Создание списка желаний для юзера
    for user in User.objects.all():
        for _ in range(random.randint(0, max_num_items)):
            product = random.choice(Product.objects.all())
            WishList.objects.create(
                user = user,
                product=product,
                added_time=timezone.make_aware(fake.date_time_this_year()),
            )


def create_categories(num_categories, categories_depth, categories_width):
    categories = []

    # Создаем случайное количество главных категорий
    num_main_categories = random.randint(3, num_categories)  # Случайное число от 3 до num_categories
    for _ in range(num_main_categories):
        name = fake.word() + " " + fake.word()
        slug = slugify(name)
        category, created = Category.objects.get_or_create(
            name=name, defaults={"slug": slug, "category_image": fake.image_url(width=200, height=200), "parent": None}
        )
        if created:
            categories.append(category)

    # Создаем подкатегории всех уровней
    for _ in range(random.randint(2, categories_depth)):  # Случайная глубина от 2 до categories_depth
        new_categories = []
        for category in categories:
            width = random.randint(1, categories_width) # Случайная ширина для каждой категории от 1 до categories_width
            for _ in range(width):  
                name = fake.word() + " " + fake.word()
                slug = slugify(name)
                subcategory, created = Category.objects.get_or_create(
                    name=name, defaults={"slug": slug, "category_image": fake.image_url(width=200, height=200), "parent": category}
                )
                if created:
                    new_categories.append(subcategory)
        categories = new_categories

    return categories


def create_products(sub_subcategories, num_products):
    # Создание продуктов для каждой категории
    for sub_subcategory in sub_subcategories:
        for _ in range(num_products):
            name = fake.word() + (" " + fake.word() if random.randint(0, 1) else "")
            prod_date = fake.date_this_decade()
            exp_date = fake.date_between_dates(date_start=prod_date, date_end="+2y")
            measurement_unit = choice(["GRAM", "KG", "UNIT"])
            slug = slugify(
                name + prod_date.strftime("%Y%m%d") + exp_date.strftime("%Y%m%d")
            )
            price = round(uniform(0.99, 999.99), 2)
            image = fake.image_url(width=200, height=200)
            product = Product.objects.create(
                name=name,
                slug=slug,
                price=price,
                image=image,
                product_category=sub_subcategory,
            )

            description = fake.text(max_nb_chars=500)

            total_views = randint(0, 1000)
            total_available = randint(0, 1000)

            status = choice(["ON_REVIEW", "IN_STOCK", "UNAVAILABLE", "SOLD"])
            ProductDetails.objects.create(
                description=description,
                prod_date=prod_date,
                exp_date=exp_date,
                total_views=total_views,
                total_items_sold=0,
                total_available=total_available,
                measurement_unit=measurement_unit,
                status=status,
                product=product,
            )


def create_products_sales_and_info(max_total_sales, max_total_sold):
    with transaction.atomic():
        for product in Product.objects.all():
            total_sales = randint(1, max_total_sales)
            for _ in range(total_sales):
                total_items_sold = randint(1, max_total_sold)

                sale_time = timezone.make_aware(fake.date_time_this_year())
                total_cost = decimal.Decimal(total_items_sold * product.price).quantize(
                    decimal.Decimal("0.01")
                )

                Sales.objects.create(
                    sale_time=sale_time,
                    total_cost=total_cost,
                    total_items_sold=total_items_sold,
                    product=product,
                )

                # Обновляем ProductDetails
                product_details = product.productdetails
                product_details.total_items_sold += total_items_sold
                product_details.save()  # Сохраняем изменения в ProductDetails

                # Обновляем SellerProductInfo
                spi_object, created = SellerProductInfo.objects.get_or_create(
                    product_details=product_details
                )
                spi_object.total_money_earned += total_cost
                spi_object.sale_time = timezone.make_aware(fake.date_time_this_year())
                spi_object.save()  # Сохраняем изменения в SellerProductInfo


# Вызов функции для создания фейковых данных
create_fake_product_data(
    num_users=10,
    num_products=5,
    num_addresses=30,
    num_categories=8,
    categories_depth=3,
    categories_width=3,
    max_num_items=20, 
    num_max_total_sales=10,
    num_max_total_sold=10,
)
