from django.core.validators import MinLengthValidator
from django.db import models


class BaseModelMixin(models.Model):
    class Meta:
        abstract = True

    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    content = models.TextField(
        validators=[
            MinLengthValidator(10)
        ]
    )
