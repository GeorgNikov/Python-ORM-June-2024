import os
from decimal import Decimal

import django
from django.core.exceptions import ValidationError



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Product, DiscountedProduct

# Create a Product instance
