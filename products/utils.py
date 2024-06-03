from django.conf import settings
from django.urls import reverse
from products.models import Product, Category

def get_product_urls():
    """
    Возвращает список полных URL-адресов для всех продуктов в базе данных.
    """
    product_urls = []
    for product in Product.objects.all():
        category = product.product_category
        all_categories = get_all_categories(category)
        category_slug = '/'.join(all_categories)
        url = reverse('product_detail', kwargs={'category_slug': category_slug, 'product_slug': product.slug})
        url = f"{settings.SITE_URL}/product/{url}"
        product_urls.append(url)
    return product_urls

def get_all_categories(category):
    """
    Рекурсивно собирает все категории, начиная с данной.
    """
    categories = [category.slug]
    if category.parent:  # Используем parent вместо parent_category
        categories.extend(get_all_categories(category.parent))
    return categories