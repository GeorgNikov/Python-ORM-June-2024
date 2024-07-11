from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from .managers import ProfileManager


# Create your models here.
class CreationDateMixin(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Profile(CreationDateMixin):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)],
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=15,
        validators=[MaxLengthValidator(15)],
    )
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    objects = ProfileManager()

    def __str__(self):
        return self.full_name


class Product(CreationDateMixin):
    name = models.CharField(
        max_length=100,
        validators=[MaxLengthValidator(100)],
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(10)],
    )
    in_stock = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
    )
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(CreationDateMixin):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_orders')
    products = models.ManyToManyField(Product, related_name='products_orders',)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(10)],
    )
    is_completed = models.BooleanField(default=False)
