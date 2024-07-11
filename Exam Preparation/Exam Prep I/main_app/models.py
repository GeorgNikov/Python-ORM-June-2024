from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import DirectorManager, ActorManager


# Create your models here.
class BasePerson(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2), MaxLengthValidator(120)],
    )
    birth_date = models.DateField(
        default='1900-01-01',
    )
    nationality = models.CharField(
        max_length=50,
        validators=[MaxLengthValidator(50)],
        default='Unknown',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.full_name


class IsAwarded(models.Model):
    is_awarded = models.BooleanField(default=False)

    class Meta:
        abstract = True


class LastUpdated(models.Model):
    last_updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class Director(BasePerson):
    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
    )

    objects = DirectorManager()


class Actor(BasePerson, IsAwarded, LastUpdated):
    objects = ActorManager()


class Movie(IsAwarded, LastUpdated):
    class GenreChoices(models.TextChoices):
        ACTION = 'Action', 'Action'
        COMEDY = 'Comedy', 'Comedy'
        DRAMA = 'Drama', 'Drama'
        OTHER = 'Other', 'Other'

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5), MaxLengthValidator(150)],
    )
    release_date = models.DateField()
    storyline = models.TextField(
        null=True,
        blank=True,
    )
    genre = models.CharField(
        max_length=6,
        validators=[MaxLengthValidator(6)],
        choices=GenreChoices.choices,
        default=GenreChoices.OTHER,
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0,
    )
    is_classic = models.BooleanField(default=False)
    director = models.ForeignKey(
        Director,
        on_delete=models.CASCADE,
        related_name='movies_directed',
    )
    starring_actor = models.ForeignKey(
        Actor,
        on_delete=models.SET_NULL,
        related_name='movies_starring',
        null=True,
        blank=True,
    )
    actors = models.ManyToManyField(
        Actor,
        related_name='movies_actor',
    )

    def __str__(self):
        return self.title
