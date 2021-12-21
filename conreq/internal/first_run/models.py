from django.db import models
from solo.models import SingletonModel


class Initialization(SingletonModel):
    def __str__(self):
        return "Initialization"

    class Meta:
        verbose_name = "Initialization"
        verbose_name_plural = verbose_name

    initialized = models.BooleanField(default=False)
