from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import AuthorManager
from main_app.mixins import BaseModelMixin


# Create your models here.

class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3)
        ]
    )

    email = models.EmailField(unique=True)

    is_banned = models.BooleanField(default=False)

    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2005),
        ]
    )

    website = models.URLField(null=True, blank=True)

    objects = AuthorManager()

    def __str__(self):
        return self.full_name


class Article(BaseModelMixin):
    class CategoryChoices(models.TextChoices):
        TECHNOLOGY = "Technology", "Technology"
        SCIENCE = "Science", "Science"
        EDUCATION = "Education", "Education"

    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(5)
        ]
    )

    category = models.CharField(
        max_length=10,
        choices=CategoryChoices.choices,
        default=CategoryChoices.TECHNOLOGY,
    )

    authors = models.ManyToManyField(
        Author,
        related_name="authors_articles",
    )

    def __str__(self):
        return self.title


class Review(BaseModelMixin):

    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ]
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="author_reviews",
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="article_reviews",
    )
