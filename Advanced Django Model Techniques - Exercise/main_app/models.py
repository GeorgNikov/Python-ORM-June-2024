from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, URLValidator, EmailValidator, MinLengthValidator


# Create your models here.
# 01. Customer
def validate_letters_and_spaces(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError("Name can only contain letters and spaces")


def validate_phone(value):
    if not value.startswith('+359') or not len(value[4:]) == 9 or not value[4:].isdigit():
        raise ValidationError("Phone number must start with '+359' followed by 9 digits")


class Customer(models.Model):
    name = models.CharField(max_length=100, validators=[validate_letters_and_spaces])
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18, message="Age must be greater than or equal to 18")]
    )
    email = models.EmailField(EmailValidator, error_messages={'invalid': 'Enter a valid email address'})
    phone_number = models.CharField(max_length=13, validators=[validate_phone])
    website_url = models.URLField(URLValidator, error_messages={'invalid': 'Enter a valid URL'})


# 02. Media
class BaseMedia(models.Model):
    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']

    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class Book(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Book'
        verbose_name_plural = 'Models of type - Book'

    author = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(5, message="Author must be at least 5 characters long")],
    )
    isbn = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(6, message="ISBN must be at least 6 characters long")],
    )


class Movie(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Movie'
        verbose_name_plural = 'Models of type - Movie'

    director = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(8, message="Director must be at least 8 characters long")],
    )


class Music(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Music'
        verbose_name_plural = 'Models of type - Music'

    artist = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(9, message="Artist must be at least 9 characters long")],
    )


# 03. Tax-Inclusive Pricing
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_tax(self):
        return self.price / 100 * 8

    def calculate_shipping_cost(self, weight: Decimal):
        return weight * 2

    def format_product_name(self):
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    class Meta:
        proxy = True

    def calculate_price_without_discount(self):
        return float(self.price) * 1.2

    def calculate_tax(self):
        return self.price / 100 * 5

    def calculate_shipping_cost(self, weight: Decimal):
        return float(weight) * 1.5

    def format_product_name(self):
        return f"Discounted Product: {self.name}"


# 04. Superhero Universe
class RechargeEnergyMixin:

    def recharge_energy(self, amount: int):
        self.energy = min(self.energy + amount, 100)
        self.save()


class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.energy < 1:
            self.energy = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - ({self.hero_title})"


class SpiderHero(Hero):
    class Meta:
        proxy = True

    def swing_from_buildings(self):
        if self.energy < 80:
            return f"{self.name} as Spider Hero is out of web shooter fluid"

        self.energy -= 80
        if self.energy == 0:
            self.energy = 1

        self.save()

        return f"{self.name} as Spider Hero swings from buildings using web shooters"


class FlashHero(Hero):
    class Meta:
        proxy = True

    def run_at_super_speed(self):
        if self.energy < 65:
            return f"{self.name} as Flash Hero needs to recharge the speed force"

        self.energy -= 65
        if self.energy == 0:
            self.energy = 1

        self.save()

        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"
