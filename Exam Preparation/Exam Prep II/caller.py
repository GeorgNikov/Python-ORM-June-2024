import os

import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order


# Create queries within functions
def get_profiles(search_string=None):
    result = []
    if search_string is None:
        return ""

    query = (
        Q(full_name__icontains=search_string) |
        Q(email__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    )

    profiles = Profile.objects.filter(query).order_by('full_name')

    if not profiles.exists():
        return ""

    for profile in profiles:
        result.append(f"Profile: {profile.full_name}, "
                      f"email: {profile.email}, "
                      f"phone number: {profile.phone_number}, "
                      f"orders: {profile.profile_orders.count()}")

    return '\n'.join(result)


def get_loyal_profiles():
    result = []
    loyal_profiles = Profile.objects.get_regular_customers()

    if not loyal_profiles.exists():
        return ""

    for profile in loyal_profiles:
        result.append(f"Profile: {profile.full_name}, "
                      f"orders: {profile.order_count}")

    return '\n'.join(result)


def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').last()

    if not last_order or not last_order.products.exists():
        return ''

    sold_products = ', '.join(product.name for product in last_order.products.all())

    return f"Last sold products: {sold_products}"


def get_top_products():
    top_products = Product.objects.annotate(
        total_sales=Count('products_orders')
    ).filter(
        total_sales__gt=0
    ).order_by(
        '-total_sales',
        'name'
    )[:5]

    if not top_products.exists():
        return ""

    result = '\n'.join(f"{product.name}, sold {product.total_sales} times" for product in top_products)

    return f"Top products:\n{result}"


def apply_discounts() -> str:
    orders = Order.objects.annotate(
        num_products=Count('products')
    ).filter(
        num_products__gt=2,
        is_completed=False,
    )

    updated_orders = orders.update(total_price=F('total_price') * 0.9)

    return f"Discount applied to {updated_orders} orders."


def complete_order() -> str:
    order = Order.objects.prefetch_related('products').filter(
        is_completed=False
    ).order_by(
        'creation_date'
    ).first()

    if not order:
        return ''

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock <= 0:
            product.is_available = False

        product.save()

    order.is_completed = True
    order.save()

    return "Order has been completed!"
