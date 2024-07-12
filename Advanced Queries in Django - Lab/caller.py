import os
from decimal import Decimal

import django
from django.db.models import Sum, Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
# 02. Product Quantity Ordered
from main_app.models import Product, Order


def product_quantity_ordered():
    orders = (Product.objects
              .annotate(total=Sum('orderproduct__quantity'))
              .exclude(total=None)
              .values('name', 'total')
              .order_by('-total')
              )

    result = []
    for order in orders:
        result.append(f"Quantity ordered of {order['name']}: {order['total']}")

    return '\n'.join(result)


# 03. Ordered Products Per Customer
def ordered_products_per_customer():
    orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')

    result = []
    for order in orders:
        result.append(f"Order ID: {order.id}, Customer: {order.customer.username}")
        for ordered_product in order.orderproduct_set.all():
            result.append(f"- Product: {ordered_product.product.name}, "
                          f"Category: {ordered_product.product.category.name}")

    return '\n'.join(result)

# print(ordered_products_per_customer())


# 04. Available Products Prices
def filter_products():
    query = Q(is_available=True) & Q(price__gt=3)
    products = Product.objects.filter(query).values('name', 'price').order_by('-price', 'name')

    return '\n'.join(f"{product['name']}: {product['price']}lv." for product in products)

# print(filter_products())


# 05. Give Discounts
def give_discount():
    query = Q(price__gt=3.00) & Q(is_available=True)
    Product.objects.filter(query).update(price=F('price') * 0.7)

    all_available_products = Product.objects.filter(is_available=True).order_by('-price', 'name')
    return '\n'.join(f"{product.name}: {product.price}lv." for product in all_available_products)


# print(give_discount())