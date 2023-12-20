
from products.models import *

def create_product(name, total_price, quantity, category_id, product_info_data):
    category = Category.objects.get(id=category_id)

    
    product = Product.objects.create(
        name=name,
        total_price=total_price,
        quantity=quantity,
        product_category=category
    )


    product_info = ProductInfo.objects.create(
        product=product,
        price=product_info_data['price'],
        arrived_date=product_info_data['arrived_date'],
        prod_date=product_info_data['prod_date'],
        exp_date=product_info_data['exp_date'],
        status=product_info_data['status'],
        rating=product_info_data['rating']
    )

    product.product_info = product_info

    return product