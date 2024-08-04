from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator
from django.db import models

from main_app.managers import AstronautManager


# Create your models here.

class Base(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class LaunchedMixin(models.Model):
    launch_date = models.DateField()

    class Meta:
        abstract = True


class Astronaut(Base):
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(regex='^\d+$')
        ]
    )

    is_active = models.BooleanField(
        default=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    spacewalks = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    objects = AstronautManager()


class Spacecraft(Base, LaunchedMixin):
    manufacturer = models.CharField(
        max_length=100
    )

    capacity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    weight = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ]
    )


class Mission(Base, LaunchedMixin):
    class StatusChoices(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    description = models.TextField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=9,
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED
    )

    spacecraft = models.ForeignKey(
        Spacecraft,  # Many-to-One
        on_delete=models.CASCADE,
        related_name='spacecraft_missions'
    )

    astronauts = models.ManyToManyField(
        Astronaut,
        related_name='astronauts_missions'
    )

    commander = models.ForeignKey(
        Astronaut,  # Many-to-Ona
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commanded_missions'
    )
